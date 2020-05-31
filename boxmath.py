import numpy as np
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from itertools import product
from scipy.special import expit
from os import system
from math import log
flag="""
FFF433
FFFFFF
9B59D0
000000""".split()

flag="""
FF0000
FFFF00
00FF00
00FFFF
0000FF
FF00FF
""".split()

#flag="""
#f9c547
#fef0cf
#8a638b
#3b3b3b""".split()
print("start!")
#flag="#fdeeb2 #9e4365 #291051 #ffd06c".split()

gamut=[convert_color(sRGBColor(*i),LabColor).get_value_tuple() for i in list(product([0,1],repeat=3))]

print("gamut'd")

labs=[convert_color(sRGBColor.new_from_rgb_hex(i),LabColor).get_value_tuple() for i in flag]
l=[]
a=[]
b=[]
for i in range(len(labs)):
    l.extend(np.linspace(labs[i-1][0],labs[i][0],256))
    a.extend(np.linspace(labs[i-1][1],labs[i][1],256))
    b.extend(np.linspace(labs[i-1][2],labs[i][2],256))

print("labbed")
    
height=255

def mangle(a,b,expon):
    def f(i,pos):
        x=(abs(pos-0.5)*2)**expon
        return i*(1-x)+(a if pos<0.5 else b)*x
    return f
#   return pos*120-10
#   return 50+((pos-0.5)*0.75+(i-50)/100*0.25)*100

lf=mangle(0,100,1.1)
cf=mangle(0,0,1.1)

with open("clut.pnm","bw") as f:
    f.write(b"P6\n")
    f.write(b"%d %d\n255\n" % (len(l),height))
    for j in range(height):
        print(f"\rwrote {j}",end="")
        for i in range(len(l)):
            c=convert_color(LabColor(lf(l[i],j/height),
                                     cf(a[i],j/height),
                                     cf(b[i],j/height),
                                     observer="2", illuminant="d65"), sRGBColor)
            f.write(bytes([int(c.clamped_rgb_r*255.99),
                           int(c.clamped_rgb_g*255.99),
                           int(c.clamped_rgb_b*255.99)]))
print()
system("convert -verbose clut.pnm clut.png")
system("termux-open clut.png")

