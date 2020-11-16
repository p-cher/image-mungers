#!/usr/bin/env python3
import sys
import colordither
import random
dehexcode=lambda x: tuple(map(lambda y: int(y,16)/255, (x[1:3],x[3:5],x[5:7])))

termcolors=tuple(map(dehexcode,"""
#2E3436 #CC0000 #4E9A06 #C4A000 #3465A4 #75507B #06989A #D3D7CF
""".split()))

gay=tuple(map(lambda x:tuple(map(lambda y: int(y)/255,x.split())),[
"254 2 0", "253 140 0", "255 229 0", "20 159 11", "10 68 179", "194 46 220", "120 79 23", "0 0 0",
]))

vaporwave=tuple(map(dehexcode,["#94D0FF","#8795E8","#966bff","#AD8CFF","#C774E8","#c774a9","#FF6AD5","#ff6a8b","#ff8b8b","#ffa58b","#ffde8b","#cdde8b","#8bde8b","#20de8b"]))
cool=tuple(map(dehexcode,["#FF6AD5","#C774E8","#AD8CFF","#8795E8","#532e57"]))
crystal_pepsi=tuple(map(dehexcode,["#FFCCFF","#F1DAFF","#E3E8FF","#CCFFFF"]))
mallsoft=tuple(map(dehexcode,["#fbcff3","#f7c0bb","#acd0f4","#8690ff","#30bfdd","#7fd4c1"]))
jazzcup=tuple(map(dehexcode,["#392682","#7a3a9a","#3f86bc","#28ada8","#83dde0"]))
sunset=tuple(map(dehexcode,["#661246","#ae1357","#f9247e","#d7509f","#f9897b"]))
macplus=tuple(map(dehexcode,["#1b4247","#09979b","#75d8d5","#ffc0cb","#fe7f9d","#65323e"]))
seapunk=tuple(map(dehexcode,["#532e57","#a997ab","#7ec488","#569874","#296656"]))

matplotlib=tuple(map(dehexcode,
             ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']))

threebit=(
(0,0,0),
(1,0,0),
(0,1,0),
(0,0,1),
(1,1,0),
(1,0,1),
(0,1,1),
(1,1,1),)
solarized=tuple(map(lambda x: tuple(map(lambda y: int(y)/255,x.split())),
"""0  43  54
7  54  66
88 110 117
101 123 131
131 148 150
147 161 161
238 232 213
253 246 227
181 137   0
203  75  22
220  50  47
211  54 130
108 113 196
38 139 210
42 161 152
133 153   0""".split("\n")))


cga0=tuple(map(dehexcode,"""
#000000 #55FF55 #FF5555 #FFFF55
""".split()))

cga1=tuple(map(dehexcode,"""
#000000	#55FFFF #FF55FF #FFFFFF
""".split()))

alpha=tuple(map(dehexcode,"""
#00d5f2 #ff6ff2 #f2a400 #1f9400
""".split()))

beta=tuple(map(dehexcode,"""
#0715cd #b536da #e00707 #4ac925
""".split()))

davepeta=tuple(map(dehexcode,"""
#4ac925 #f2a400
""".split()))

def view_palette(*args,names=[]):
    from matplotlib import pyplot as plt
    from math import ceil
    import subprocess
    h=min(len(args),4)
    w=ceil(len(args)/h)
#    print(len(args),w,h,file=sys.stderr)
    f, ax = plt.subplots(h,w,figsize=(3*w,3*h))
    for i, name in enumerate(args):
        x,y=i//w,i%w
        if h==1:
            curax=ax
        elif w==1:
            curax=ax[x]
        else:
            curax=ax[x,y]
#        print(x,y,file=sys.stderr)
        cycle = list(map(lambda x: "#{:02X}{:02X}{:02X}".format(int(x[0]*255),int(x[1]*255),int(x[2]*255)),name))
        for j,c in enumerate(cycle):
            xs=[0,1,1,0]
            ys=[-j,-j,-j+1,-j+1]
            curax.fill(xs,ys,c)#ax[x,y].hlines(j,0,1,colors=c,linewidth=15)
        if i<len(names):
            curax.set_title(str(names[i]))
    for x in range(h):
        for y in range(w):
            if h==1:
                curax=ax
            elif w==1:
                curax=ax[x]
            else:
                curax=ax[x,y]
            for sp in curax.spines:
                curax.spines[sp].set_visible(False)
            curax.get_xaxis().set_visible(False)
            curax.get_yaxis().set_visible(False)
    plt.tight_layout(0)
    fig=plt.figure(1)
    fig.savefig("palette.svg",bbox_inches='tight')
#    subprocess.call(["cairosvg", "palette-temp.svg", "-f", "svg", "-o","palette.svg"])
#    subprocess.call(["rm", "palette-temp.svg"])
    subprocess.call(["convert", "-density", "400", "palette.svg", "palette.png"])
    plt.show()

detriple=lambda x: tuple((x[0][i]/255,x[1][i]/255,x[2][i]/255) for i in range(len(x[0])))

botross=list(map(detriple,[
    [ # 0: The Apple-II Color Palette
        [0, 108,  64, 217, 64, 217, 128, 236, 19,  38, 191,  38, 191, 147, 255],
        [0,  41,  53,  60, 75, 104, 128, 168, 87, 151, 180, 195, 202, 214, 255],
        [0,  64, 120, 240,  7,  15, 128, 191, 64, 240, 248,  15, 135, 191, 255],],
    [ # 1: C64 Color Palette
        [0, 255, 104,  11, 111,  88,  53, 184, 111, 67, 154, 68, 108, 154, 108, 149],
        [0, 255,  55, 164,  61, 141,  40, 199,  79, 57, 103, 68, 108, 210,  94, 149],
        [0, 255,  43, 178, 134,  67, 121, 111,  37,  0,  89, 68, 108, 132, 181, 149],],
    [ # 2: Sierra AGI Color Palette
        [  0,  0,  0,  0,170,170,170,170, 77, 77, 77, 77,255,255,255,255],
        [  0,  0,170,170,  0,  0, 77,170, 77, 77,255,255, 77, 77,255,255],
        [  0,170,  0,170,  0,170,  0,170, 77,255, 77,255, 77,255, 77,255],],
    [ # 3: CGA
        [0, 26, 17, 40, 105, 128, 118, 164, 72, 118, 109, 132, 197, 220, 210, 255],
        [0, 0, 120, 158, 0, 25, 145, 164, 72, 91, 212, 250, 78, 117, 237, 255],
        [0, 166, 0, 118, 26, 171, 0, 164, 72, 255, 65, 210, 118, 255, 70, 255],],
    [ # 4: Pico-8
        [  0, 126, 29, 95, 171, 0, 255, 95, 131, 255, 194, 0, 255, 41, 255, 255],
        [  0, 37, 43, 87, 82, 135, 0, 87, 118, 163, 195, 231, 204, 173, 255, 241],
        [  0, 83, 83, 79, 54, 81, 77, 79, 156, 0, 199, 86, 170, 255, 39, 232],],
    [ # 5: Windows 16
        [0, 128,   0, 128,   0, 128,   0, 192, 128, 255,   0, 255,   0, 255,   0, 255], 
        [0,   0, 128, 128,   0,   0, 128, 192, 128,   0, 255, 255,   0,   0, 255, 255],
        [0,   0,   0,   0, 128, 128, 128, 192, 128,   0,   0,   0, 255, 255, 255, 255],],
    [ # 6: Psygnosia from http://androidarts.com/palette/16pal.htm
        [0, 27, 54, 68, 82, 100, 115, 119, 158, 203, 224, 162,   0,   8,  84,  81], 
        [0, 30, 39, 63, 82, 100,  97, 120, 164, 232, 139,  50,  51,  74, 106, 108],
        [0, 41, 71, 65, 76, 124,  80,  91, 167, 247, 121,  78,   8,  60,   0, 191],],
    [ # 7: Gray Scale
        [0, 51, 102, 153, 204, 255], 
        [0, 51, 102, 153, 204, 255], 
        [0, 51, 102, 153, 204, 255], ],
    [ # 8: Minecraft stained clay colors
        [207, 156, 147, 110, 186, 100, 160, 55, 129, 85, 120, 72, 75, 72, 145, 33], 
        [172,  79,  85, 105, 133, 114,  77, 39, 102, 90,  71, 58, 51, 80,  61, 18], 
        [157,  33, 107, 135,  33,  48,  77, 33,  92, 90,  86, 89, 33, 39,  47, 13], ],
    [ # 9: Minecraft woll colors
        [221, 219, 179, 107, 177, 65, 208, 64, 154, 46, 126, 46, 79, 53, 150, 25], 
        [221, 125, 80, 138, 166, 174, 132, 64, 161, 110, 61, 56, 50, 70, 52, 22], 
        [221, 62, 188, 201, 39, 56, 153, 64, 161, 137, 181, 141, 31, 27, 48, 22], ],
    [ # 10: Minecraft colors (woll and clay)
        [221, 219, 179, 107, 177, 65, 208, 64, 154, 46, 126, 46, 79, 53, 150, 25, 207, 156, 147, 110, 186, 100, 160, 55, 129, 85, 120, 72, 75, 72, 145, 33], 
        [221, 125, 80, 138, 166, 174, 132, 64, 161, 110, 61, 56, 50, 70, 52, 22, 172,  79,  85, 105, 133, 114,  77, 39, 102, 90,  71, 58, 51, 80,  61, 18], 
        [221, 62, 188, 201, 39, 56, 153, 64, 161, 137, 181, 141, 31, 27, 48, 22, 157,  33, 107, 135,  33,  48,  77, 33,  92, 90,  86, 89, 33, 39,  47, 13], ],
    [ # 11: Minecraft map colors
        [127,247,199,255,160,167,  0,255,164,151,112, 64,143,255,216,178,102,229,127,242,76,153, 76,127, 51,102,102,153,25,250, 92, 74,  0,129,112], 
        [178,233,199,  0,160,167,124,255,168,109,112, 64,119,252,127, 76,153,229,104,127,76,153,127, 63, 76, 76,127,51, 25,238,219,128,217, 86,  2], 
        [ 56,163,199,  0,255,167,  0,255,184, 77,112,255, 72,245, 51,216,216, 51, 25,165,76,153,153,178,178, 51, 51,51, 25, 77,213,255, 58, 49,  0], ],
    [ # 12: Gameboy color
        [175,121,34,8], 
        [203,170,111,41], 
        [70,109,95,85], ],
    [ # 13: Dawnbreaker 32
        [0,34,69,102,143,223,217,238,251,153,106,55,75,82,50,63,48,91,99,95,203,255,155,132,105,89,118,172,217,215,143,138], 
        [0,32,40,57,86,113,160,195,242,229,190,148,105,75,60,63,96,110,155,205,219,255,173,126,106,86,66,50,87,123,151,111], 
        [0,52,60,49,59,38,102,154,54,80,48,110,47,36,57,116,130,225,255,228,252,255,183,135,106,82,138,50,99,186,74,48], ],
]))

strategywiki=[
#  0: Pallet Town
"#F8F8F8 #C0AEC7 #75C0C9 #000000",
#  1: Pallet Town indoors
"#F8F8F8 #B888F8 #58B8F8 #181818",
#  2: Routes
"#F8F8F8 #C8DB9C #9ADB00 #000000",
#  3: Viridian City
"#F8F8F8 #A6FF1D #93AECF #000000",
#  4: Viridian Forest
"#F8F8F8 #58B8F8 #80F820 #181818",
#  5: Mount Moon
"#F8F8F8 #AB8366 #AB4800 #000000",
#  6: Cerulean City
"#F8F8F8 #A9A9BE #6D6DBE #000000",
#  7: Vermillon City
"#F8F8F8 #7E95DD #FFD668 #000000",
#  8: Game Corner
"#F8F8F8 #94FF7C #A0CDE6 #000000",
#  9: Pokemon Tower
"#F8F8F8 #CBA2CB #CB38CB #000000",
# 10: Fuchsia City
"#F8F8F8 #FF91AC #93AECF #000000",
# 11: Cinnabar Island
"#F8F8F8 #93AECF #FF282D #000000",
# 12: Seafoam Cave
"#F8F8F8 #70859E #AB4800 #000000",
# 13: Unknown Dungeon
"#F8F8F8 #00C49E #AB4800 #000000",
]

strategywiki=[tuple(map(dehexcode,i.split())) for i in strategywiki]

gameboy=tuple(map(dehexcode,"""
#0f380f #306230 #8bac0f #9bbc0f
""".split()))


warm=tuple(map(dehexcode,"""
#C11D1D #D28231 #DFC45D #606C38 #230007
""".split()))

hexes=tuple(map(dehexcode,"""
#171314 #FFFFFF #FFFF58
""".split()))

rand=tuple((random.random(),random.random(),random.random()) for i in range(15))
render=lambda x: "\033[38;2;{0};{1};{2}m#{0:02X}{1:02X}{2:02X} \033[0m\033[48;2;{0};{1};{2}m       \033[0m".format(int(x[0]*255),int(x[1]*255),int(x[2]*255),x)
hexify=lambda x: "#{0:02X}{1:02X}{2:02X}".format(int(x[0]*255),int(x[1]*255),int(x[2]*255),x)
#print(rand,file=sys.stderr)
#view_palette(rand,names=["Random"])


#colordither.dither_color(sys.argv[1],botross[13],hexify(botross[13][0]),"img.transform('','50%')") #,"img.transform('','50%')"
#colordither.dither_color(sys.argv[1],botross[13]+((0,0,0),),"#000000","img.transform('','50%')")
#colordither.dither_color(sys.argv[1],vaporwave +((0,0,0),(1,1,1)) ,"#000000")
colordither.dither_color(sys.argv[1],hexes ,"#000000","img.transform('','100%')")


#view_palette(*strategywiki,names=range(len(strategywiki)))
#view_palette(*botross,solarized,matplotlib,termcolors,gay,warm,alpha,beta,davepeta,names=["Apple II", "C64", "Sierra AGI", "CGA", "Pico-8", "Windows 16", "Psygnosia", "Grayscale","Minecraft Stained Clay","Minecraft Wool","Wool and Clay","Minecraft Map","Gameboy","Dawnbreaker 32","Solarized","Matplotlib","Terminal Colors","Gay","Warm","Alpha Kids","Beta Kids","Davepeta"])

