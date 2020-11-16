import sys
import re
import requests
import wand.image
import wand.api
if sys.argv[2:]:
    inp=sys.argv[2]
else:
    inp=input()
if re.match("^https?://",inp):
    props=dict(blob=requests.get(inp).content,resolution=400)
else:
    props=dict(filename=inp,resolution=400)
with wand.image.Image(**props) as img:
    img.format="RGB"
    img.depth=8
    x=img.width
    y=img.height
    img.background_color=wand.color.Color("#000000")
    img.alpha_channel="remove"
    wand.api.library.MagickSetImageEndian(img.wand,1)
    blob=img.make_blob()
arrblob=tuple(blob)

def delinearize(c):
    if c<=0.04045:
        return c/12.92
    else:
        return ((c+0.055)/(1.055))**2.4


def distance(a,b):
    return (a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2

def srgbtoxyz(srgb):
    #cdef np.ndarray mat
    r=delinearize(srgb[0])
    g=delinearize(srgb[1])
    b=delinearize(srgb[2])
    srgb[0]=0.4124564*r+0.3575761*g+0.1804375*b
    srgb[1]=0.2126729*r+0.7151522*g+0.0721750*b
    srgb[2]=0.0193339*r+0.1191920*g+0.9503041*b
    return srgb


def f(t):
    if t>(6/29)**3:
        return t**(1/3)
    else:
        return (24389/27*t+16)/116

def xyztolab(xyz):
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

a={}
labs={}
for j in range(y):
    for i in range(x):
        col=arrblob[i*3+j*3*x:i*3+j*3*x+3]
        if col in a.keys():
            a[col]+=1
        else:
            a[col]=1
            labs[col]=xyztolab(srgbtoxyz(list(map(lambda x: x/255,col))))
b=sorted(a.keys(),key=a.get,reverse=True)
total=sum(a.values())
c=[]
c2=[]
categories=[]
thresh=int(sys.argv[1])**2
#thresh=20**2
for j in range(16):
    c.append(b[0])
    c2.append(sum(a[i] for i in b if distance(labs[c[j]],labs[i])<=thresh))
    categories.append([i for i in b if distance(labs[c[j]],labs[i])<=thresh][:13])
    b=[i for i in b if distance(labs[c[j]],labs[i])>thresh]
    if not b:
        break
render=lambda x: "\033[38;2;{0};{1};{2}m#{0:02X}{1:02X}{2:02X} \033[0m\033[48;2;{0};{1};{2}m       \033[0m".format(*x)
percent=lambda x,y,z: "{0} ({1}/{2} {3}%)".format(x,y,z,int((y/z)*100+0.5))
render2=lambda x,y,z: percent(render(x),y,z)
hexify=lambda x: "#{0:02X}{1:02X}{2:02X}".format(*x)

for i in range(len(categories)):
    print(render(categories[i][0]))
    for j in range(1,len(categories[i]),3):
        print(render(categories[i][j]),end="  ")
        if j+1<len(categories[i]):
            print(render(categories[i][j+1]),end="  ")
        if j+2<len(categories[i]):
            print(render(categories[i][j+2]),end="  ")
        print()
    print()

print(percent("Others:",sum(map(a.get,b)),total))
print()
print(*map(render2,c,map(a.get,c),c2),sep="\n")
print()

print(*map(hexify,c))
