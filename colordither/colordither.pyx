import websockets
import requests
import wand.image
import re
import sys
import numpy as np
cimport numpy as np
cimport cython
from cython.parallel cimport prange

cdef double delinearize(double c) nogil except? -1:
    if c<=0.04045:
        return c/12.92
    else:
        return ((c+0.055)/(1.055))**2.4

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double distance(double[:] a, double[:] b) except? -1:
    return (a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2

@cython.boundscheck(False)
@cython.wraparound(False)
cdef Py_ssize_t closest(double[:] color, double[:,:] palette, int pallen) except? -1:
    cdef Py_ssize_t mincolor
    cdef double mindist,coldist
    mincolor=0
    mindist=distance(color,palette[0])
#    print(np.array(palette), np.array(color), np.array(palette[0]), mindist,file=sys.stderr)
    for ind in range(1,pallen):
        coldist=distance(color,palette[ind])
        if coldist<mindist:
#            print(coldist,mindist,ind,file=sys.stderr)
            mindist=coldist
            mincolor=ind
    return mincolor

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double[:] srgbtoxyz(double[:] srgb) nogil:
    #cdef np.ndarray mat
    cdef double r,g,b
    r=delinearize(srgb[0])
    g=delinearize(srgb[1])
    b=delinearize(srgb[2])
    srgb[0]=0.4124564*r+0.3575761*g+0.1804375*b
    srgb[1]=0.2126729*r+0.7151522*g+0.0721750*b
    srgb[2]=0.0193339*r+0.1191920*g+0.9503041*b
    return srgb


cdef double f(double t) nogil:
    if t>(6/29)**3:
        return t**(1/3)
    else:
        return (24389/27*t+16)/116

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double[:] xyztolab(double[:] xyz) nogil:
    cdef double x,y,z,l,a,b
    x=xyz[0]
    y=xyz[1]
    z=xyz[2]
    l=116*f(y)-16
    a=500*(f(x/0.95047)-f(y))
    b=200*(f(y)-f(z/1.08883))
    xyz[0]=l
    xyz[1]=a
    xyz[2]=b
    return xyz

@cython.boundscheck(False)
@cython.wraparound(False)
def dither_color(dither, origpalette, bgcolor, imgexec=None):
    cdef Py_ssize_t x,y,j,i,c,n
    cdef int di,dj
    cdef double colarr[3]
    cdef double [:,:,:] a,errmap
    cdef double [:,:] palette
    cdef double [:] closepal,col=colarr
    cdef Py_ssize_t [:,:] b
    cdef double err0,err1,err2
    cdef Py_ssize_t close
    cdef bytes blob
    cdef long long[:] arrblob

    palette=np.array(origpalette,dtype=np.double)
    pallen=len(origpalette)
    print("Loading image",file=sys.stderr)
    if re.match("^https?://",dither):
        props=dict(blob=requests.get(dither).content,resolution=400)
    else:
        props=dict(filename=dither,resolution=400)
    with wand.image.Image(**props) as img:
        if imgexec:
            state={"img":img}
            exec(imgexec,state)
            img=state["img"]
        img.format="RGB"
        img.depth=32
        x=img.width
        y=img.height
        img.background_color=wand.color.Color(bgcolor)
        img.alpha_channel="remove"
        wand.api.library.MagickSetImageEndian(img.wand,1)
        blob=img.make_blob()
    arrblob=np.array(tuple(blob),dtype=np.longlong)
    a=np.zeros((y,x,3),dtype=np.double)
    for j in range(y):
        for i in range(x):
            for c in range(3):
                col[c]=0
                for n in range(4):
                    col[c]+=arrblob[n+c*4+i*4*3+j*4*3*x]*256**(n)
                col[c]/=256**4-1
#            print(np.array(col),file=sys.stderr)
            a[j][i]=col
    #arr=[tuple(sum(a[n+c*4+i*4*3+j*4*3*x]*256**(3-n) for n in range(4))/(256**4-1) for c in range(3)) for j in range(y) for i in range(x)]
    #print(arr,file=sys.stderr)
    #mat=np.array([[0.49, 0.31, 0.2],[0.17697,0.8134, 0.01063],[0, 0.01, 0.99]])/0.17697

#    print("P3")
#    print(x,y)
#    print("255")
#    for j in range(y):
#        for i in range(x):
#            for c in range(3):
#                print(int(a[j][i][c]*255),end=" ")
#    return

    print("Generating XYZ",file=sys.stderr)
    with nogil:
        for i in prange(y):
            for j in range(x):
    #            print(a[i][j],file=sys.stderr)
                a[i][j]=srgbtoxyz(a[i][j])
            #print("\rRow {}/{}".format(i+1,y),file=sys.stderr,end="")

    for i in range(pallen):
        palette[i]=srgbtoxyz(palette[i])

    print("Generating LAB",file=sys.stderr)
    with nogil:
        for i in prange(y):
            for j in range(x):
                a[i][j]=xyztolab(a[i][j])
            #print("\rRow {}/{}".format(i+1,y),file=sys.stderr,end="")

    for i in range(pallen):
        palette[i]=xyztolab(palette[i])

    #dist=lambda c: lambda x,c=c: sqrt(sum((c[i]-x[i])**2 for i in range(3)))
    #closest=lambda c: palette.index(min(palette,key=dist(c)))

    #a=np.array(lab, dtype=np.double).reshape(y,x,3)
    #errmap=np.zeros( (y+2,x+2,3), dtype=np.double)
    cdef int thresh=128
    b=np.zeros((y,x),dtype=np.int)
    print("Dithering:",file=sys.stderr)
    for di in range(y):
        for dj in range(x):
            close=closest(a[di,dj], palette,pallen)
            b[di,dj]=close
            closepal=palette[close]
            err0=a[di,dj,0]-closepal[0]
            err1=a[di,dj,1]-closepal[1]
            err2=a[di,dj,2]-closepal[2]
            if err0>thresh or err0<-thresh:
                err0*=0.9
            if err1>thresh or err1<-thresh:
                err1*=0.9
            if err2>thresh or err2<-thresh:
                err2*=0.9
            if dj+1<x:
                a[di  ,dj+1,0]+=err0*7/16
                a[di  ,dj+1,1]+=err1*7/16
                a[di  ,dj+1,2]+=err2*7/16
            if di+1<y and dj-1>0:
                a[di+1,dj-1,0]+=err0*3/16
                a[di+1,dj-1,1]+=err1*3/16
                a[di+1,dj-1,2]+=err2*3/16
            if di+1<y:
                a[di+1,dj  ,0]+=err0*5/16
                a[di+1,dj  ,1]+=err1*5/16
                a[di+1,dj  ,2]+=err2*5/16
            if di+1<y and dj+1<x:
                a[di+1,dj+1,0]+=err0*1/16
                a[di+1,dj+1,1]+=err1*1/16
                a[di+1,dj+1,2]+=err2*1/16

        print("\rRow {}/{}".format(di+1,y),file=sys.stderr,end="")
    print(file=sys.stderr)
    print("File output",file=sys.stderr)
    return bytes("P6\n{} {}\n255\n".format(x,y),"ascii")+bytes(int(z*256-(1 if z==1 else 0)) for i in b for j in i for z in origpalette[j])
#    print(" ".join(map(lambda x: " ".join(map(lambda y:" ".join(map(lambda z: str(int(z*256-(1 if z==1 else 0))),origpalette[y])),x)),list(b))))
    #print(np.array(b),file=sys.stderr)

