a=2
#import sys
f=open("alternate.py")
f.readline()
s=f.read()
s="a={}\n".format((int(a)+1)%10)+s
open("alternate.py","w").write(s)
print(a)
