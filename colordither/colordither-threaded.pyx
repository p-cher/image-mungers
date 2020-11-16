import websockets
import requests
import wand.image
import re
import sys
import numpy as np
from math import sqrt
from multiprocessing import Pool

cimport numpy as np

cdef double delinearize(double c) except? -1:
    if c<=0.04045:
        return c/12.92
    else:
        return ((c+0.055)/(1.055))**2.4

cdef double distance(double[:] a, double[:] b) except? -1:
    return (a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2

cdef Py_ssize_t closest(double[:] color, double[:,:] palette) except? -1:
    cdef Py_ssize_t mincolor
    cdef double mindist,coldist
    mincolor=0
    mindist=distance(color,palette[0])
    for ind in range(1,len(palette)):
        coldist=distance(color,palette[ind])
        if coldist<mindist:
            mindist=coldist
            mincolor=ind
    return mincolor

def srgbtoxyz(srgb):
    cdef np.ndarray mat
    cdef tuple rgb
    mat=np.array(
    ((0.4124564, 0.3575761, 0.1804375),
     (0.2126729, 0.7151522, 0.0721750),
     (0.0193339, 0.1191920, 0.9503041)))
    rgb=tuple(map(delinearize,srgb))
    #rgb=srgb
    return tuple(mat @ rgb)


cdef double f(double t):
    if t>(6/29)**3:
        return t**(1/3)
    else:
        return (24389/27*t+16)/116

def xyztolab(xyz):
    cdef double x,y,z,l,a,b
    x,y,z=xyz
    l=116*f(y)-16
    a=500*(f(x/0.95047)-f(y))
    b=200*(f(y)-f(z/1.08883))
    return (l, a, b)

def dither_color(dither):
    cdef tuple palette,origpalette,lab
    cdef Py_ssize_t x,y,j,i,c,n
    cdef int di,dj
    cdef double [:,:,:] a,errmap
    cdef double [:,:] memviewpal
    cdef double [:] closepal
    cdef Py_ssize_t [:,:] b
    cdef double err0,err1,err2
    cdef Py_ssize_t close
    cdef double[3] col
    cdef bytes blob

    palette=(
    (0,0,0),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (0,1,1),
    (1,1,1),)
    origpalette=palette[:]
    print("Loading image",file=sys.stderr)
    if re.match("^https?://",dither):
        props=dict(blob=requests.get(dither).content,resolution=400)
    else:
        props=dict(filename=dither,resolution=400)
    with wand.image.Image(**props) as img:
        img.format="RGB"
        img.depth=32
        x=img.width
        y=img.height
        img.background_color=wand.color.Color("#000000")
        img.alpha_channel="remove"
        blob=img.make_blob()
    arr=[]
    for j in range(y):
        for i in range(x):
            col=np.zeros((3),dtype=np.double)
            for c in range(3):
                for n in range(4):
                    col[c]+=blob[n+c*4+i*4*3+j*4*3*x]*256**(3-n)
                col[c]/=256**4-1
            arr.append(tuple(col))
    #arr=[tuple(sum(a[n+c*4+i*4*3+j*4*3*x]*256**(3-n) for n in range(4))/(256**4-1) for c in range(3)) for j in range(y) for i in range(x)]
    #print(arr,file=sys.stderr)
    #mat=np.array([[0.49, 0.31, 0.2],[0.17697,0.8134, 0.01063],[0, 0.01, 0.99]])/0.17697
    print("Generating XYZ",file=sys.stderr)
    with Pool(8) as p:
        xyz=tuple(p.map(srgbtoxyz,arr))
        palette=tuple(p.map(srgbtoxyz,palette))

    print("Generating LAB",file=sys.stderr)
    with Pool(8) as p:
        lab=tuple(p.map(xyztolab, xyz))
        palette=tuple(p.map(xyztolab, palette))

    #dist=lambda c: lambda x,c=c: sqrt(sum((c[i]-x[i])**2 for i in range(3)))
    #closest=lambda c: palette.index(min(palette,key=dist(c)))

    a=np.array(lab, dtype=np.double).reshape(y,x,3)
    #errmap=np.zeros( (y+2,x+2,3), dtype=np.double)
    b=np.zeros((y,x),dtype=np.int)
    memviewpal=np.array(palette,dtype=np.double)
    print("Dithering:",file=sys.stderr)
    for di in range(y):
        for dj in range(x):
            close=closest(a[di,dj], memviewpal)
            b[di,dj]=close
            closepal=memviewpal[close]
            err0=a[di,dj,0]-closepal[0]
            err1=a[di,dj,1]-closepal[1]
            err2=a[di,dj,2]-closepal[2]
#            diff=(7,3,5,1) #floyd-steinberg, temporary
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

    print("P3")
    print(x,y)
    print(1)

    print(" ".join(map(lambda x: " ".join(map(lambda y:" ".join(map(str,origpalette[y])),x)),b)))
    print("File output",file=sys.stderr)


