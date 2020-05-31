#!/data/data/com.termux/files/usr/bin/env python3
from sys import argv,stdout,stderr
import hsluv
stdout.buffer.write(b"P6\n1 256\n255\n")
h,s,luv=hsluv.hex_to_hsluv(argv[1])
print("\n\n\n",h,s,luv,"\n\n",file=stderr)
for i in range(256):
    stdout.buffer.write(bytes(map(lambda x: int(x*255+0.5),hsluv.hsluv_to_rgb((h,s,((i/255)*100+((luv-50)/3 if s==0 else 0)))))))
