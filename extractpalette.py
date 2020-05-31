from wand.image import Image
import requests
from sys import argv
import numpy as np
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from collections import Counter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

resp=requests.get(argv[1])
if resp:
    args={"blob": resp.content}
else:
    args={"filename": argv[1]}

with Image(**args) as img:
    img.colorspace="rgb"
    a=np.array(img).reshape(-1,4)
    a=a[:,:-1]
counts=Counter(map(tuple,a))
print(counts.most_common(5))
m=max(counts.values())
total=sum(counts.values())
l,a,b,s,c=[],[],[],[],[]
good=0
show=8
for i in counts.most_common():
    if (i[1]/m<0.005):
        break
    good+=i[1]
    temp=convert_color(sRGBColor(*i[0],is_upscaled=True),LabColor).get_value_tuple()
    l.append(temp[0])
    a.append(temp[1])
    b.append(temp[2])
    s.append(i[1]/m*100)
    c.append(sRGBColor(*i[0],is_upscaled=True).get_rgb_hex())
    if show:
        print(f"\033[{30 if l[-1]>50 else 37};48;2;{i[0][0]};{i[0][1]};{i[0][2]}m{c[-1]}\033[0m ({i[1]}, {i[1]/total*100}%)")
        show-=1

#print(l,a,b,s,c)
print(f"Image is {good/total*100}% accounted for")
print(*c[:8])
ax.scatter(a,b,l,s=s,c=c,depthshade=False)

plt.show()
