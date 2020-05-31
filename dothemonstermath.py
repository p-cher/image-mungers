import numpy as np
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from scipy.interpolate import splprep, splev
from itertools import product
from os import system
#flag="""
#FFF433
#FFFFFF
#9B59D0
#000000""".split()

#flag="""
#f9c547
#fef0cf
#8a638b
#3b3b3b""".split()

flag="#fdeeb2 #9e4365 #291051 #ffd06c".split()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

gamut=[convert_color(sRGBColor(*i),LabColor).get_value_tuple() for i in list(product([0,1],repeat=3))]

labs=[convert_color(sRGBColor.new_from_rgb_hex(i),LabColor).get_value_tuple() for i in flag]
l=[]
a=[]
b=[]
spl_l=[]
spl_a=[]
spl_b=[]
for i in range(len(labs)):
    l.extend(np.linspace(labs[i-1][0],labs[i][0],256))
    a.extend(np.linspace(labs[i-1][1],labs[i][1],256))
    b.extend(np.linspace(labs[i-1][2],labs[i][2],256))
    spl_l.append(labs[i][0])
    spl_a.append(labs[i][1])
    spl_b.append(labs[i][2])
#    l.extend([labs[i][0]]*10)
#    a.extend([labs[i][1]]*10)
#    b.extend([labs[i][2]]*10)

spl_l=[spl_l[-1]]+spl_l
spl_a=[spl_a[-1]]+spl_a
spl_b=[spl_b[-1]]+spl_b
tck,u=splprep([spl_l,spl_a,spl_b],s=0,per=True)
print(tck)
print(u)

spline=splev(np.linspace(0,1,1024),tck)

rgbs=[convert_color(LabColor(l[i],a[i],b[i],observer="2",illuminant="d65"),sRGBColor) for i in range(len(l))]
spl_rgbs=[convert_color(LabColor(spline[0][i],spline[1][i],spline[2][i],observer="2",illuminant="d65"),sRGBColor) for i in range(len(spline[0]))]
hexes=[(i.clamped_rgb_r,i.clamped_rgb_g,i.clamped_rgb_b) for i in rgbs]
spl_hexes=[(i.clamped_rgb_r,i.clamped_rgb_g,i.clamped_rgb_b) for i in spl_rgbs]

clamped=[convert_color(sRGBColor(*i),LabColor).get_value_tuple() for i in hexes]
spl_clamped=[convert_color(sRGBColor(*i),LabColor).get_value_tuple() for i in spl_hexes]
print(clamped)
lines=[]
for i in range(len(clamped)):
    lines.append([[clamped[i-1][1],
                   clamped[i-1][2],
                   clamped[i-1][0]],
                  [clamped[i][1],
                   clamped[i][2],
                   clamped[i][0]]])



spl_lines=[]
for i in range(len(spl_clamped)):
    spl_lines.append([[spl_clamped[i-1][1],
                   spl_clamped[i-1][2],
                   spl_clamped[i-1][0]],
                  [spl_clamped[i][1],
                   spl_clamped[i][2],
                   spl_clamped[i][0]]])

    
lc=Line3DCollection(lines,colors=hexes)
spl_lc=Line3DCollection(spl_lines,colors=spl_hexes,lw=3)


ax.add_collection3d(lc)

ax.add_collection3d(spl_lc)

ax.scatter([i[1] for i in labs],
           [i[2] for i in labs],
           [i[0] for i in labs],c=flag,edgecolors="#000000")
ax.scatter([i[1] for i in gamut],
           [i[2] for i in gamut],
           [i[0] for i in gamut],c=tuple(product((0,1),repeat=3)),edgecolors="#000000")
#print(gamut,file=stderr)

with open("clut.pnm","bw") as f:
    f.write(b"P6\n")
    f.write(b"%d 1\n255\n" % len(rgbs))
    for i in rgbs:
        f.write(bytes([int(i.clamped_rgb_r*255.99),
                       int(i.clamped_rgb_g*255.99),
                       int(i.clamped_rgb_b*255.99)]))
    
with open("splineclut.pnm","bw") as f:
    f.write(b"P6\n")
    f.write(b"%d 1\n255\n" % len(spl_rgbs))
    for i in spl_rgbs:
        f.write(bytes([int(i.clamped_rgb_r*255.99),
                       int(i.clamped_rgb_g*255.99),
                       int(i.clamped_rgb_b*255.99)]))

system("convert clut.pnm -resize 100%x8000% clut.png")
system("convert splineclut.pnm -resize 100%x8000% splineclut.png")
system("convert clut.png splineclut.png -gravity Center -append compare.png")
plt.show()
system("eom compare.png")
