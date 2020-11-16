import discord
import colordither
import subprocess
import traceback
from matplotlib.colors import to_rgb,to_hex

TOKEN=open("token").read()

client = discord.Client()

dehexcode=lambda x: to_rgb("#{1}{1}{2}{2}{3}{3}".format(*x) if (x[0]=="#" and len(x)==4) else x)
#dehexcode=lambda x: tuple(map(lambda y: int(y,16)/255, (x[1:3],x[3:5],x[5:7])))

metapalette=dict(
vaporwave=tuple(map(dehexcode,["#94D0FF","#8795E8","#966bff","#AD8CFF","#C774E8","#c774a9","#FF6AD5","#ff6a8b","#ff8b8b","#ffa58b","#ffde8b","#cdde8b","#8bde8b","#20de8b"])),
cool=tuple(map(dehexcode,["#FF6AD5","#C774E8","#AD8CFF","#8795E8","#532e57"])),
crystal_pepsi=tuple(map(dehexcode,["#FFCCFF","#F1DAFF","#E3E8FF","#CCFFFF"])),
mallsoft=tuple(map(dehexcode,["#fbcff3","#f7c0bb","#acd0f4","#8690ff","#30bfdd","#7fd4c1"])),
jazzcup=tuple(map(dehexcode,["#392682","#7a3a9a","#3f86bc","#28ada8","#83dde0"])),
sunset=tuple(map(dehexcode,["#661246","#ae1357","#f9247e","#d7509f","#f9897b"])),
macplus=tuple(map(dehexcode,["#1b4247","#09979b","#75d8d5","#ffc0cb","#fe7f9d","#65323e"])),
seapunk=tuple(map(dehexcode,["#532e57","#a997ab","#7ec488","#569874","#296656"])),
matplotlib=tuple(map(dehexcode,
             ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf'])),
threebit=(
(0,0,0),
(1,0,0),
(0,1,0),
(0,0,1),
(1,1,0),
(1,0,1),
(0,1,1),
(1,1,1),),
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
133 153   0""".split("\n"))),
cga0=tuple(map(dehexcode,"""
#000000 #55FF55 #FF5555 #FFFF55
""".split())),
cga1=tuple(map(dehexcode,"""
#000000	#55FFFF #FF55FF #FFFFFF
""".split())),
alpha=tuple(map(dehexcode,"""
#00d5f2 #ff6ff2 #f2a400 #1f9400
""".split())),
beta=tuple(map(dehexcode,"""
#0715cd #b536da #e00707 #4ac925
""".split())),
davepeta=tuple(map(dehexcode,"""
#4ac925 #f2a400
""".split())),
gameboy=tuple(map(dehexcode,"""
#0f380f #306230 #8bac0f #9bbc0f
""".split())),
warm=tuple(map(dehexcode,"""
#C11D1D #D28231 #DFC45D #606C38 #230007
""".split())),
hexes=tuple(map(dehexcode,"""
#171314 #FFFFFF #FFFF58
""".split())),
)


fileid=0
users={}
defaulthexes=tuple(map(dehexcode,"""
#171314 #FFFFFF #FFFF58
""".split()))

def ensure_dict(whomst):
    if whomst not in users:
        users[whomst]={}


@client.event
async def on_message(message):
    global hexes, fileid, pixsize
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    try:
        if message.content.startswith('!help'):
            msg="""
This is a janky, thin shell of bot around the color ditherer script. Commands:

!help: shows this

!setpalette: sets the current palette
usage: !setpalette #dabbed #c0fefe #000000 #ffffff
supports anything that matplotlib's color parser does, plus three digit hexcodes

!palettize: applies the palette to an image
usage: !palettize [url or attachment]
takes either an url or an attachment (an image uploaded alongside the message)

!repalette: like !setpalette but then immediately redoes your last !pallettize

!pixsize: changes the chonkyness of the pixels
usage: !pixsize 1
only takes an integer
"""
            await client.send_message(message.channel, msg)
    
        if message.content.startswith('!palettize'):
            await client.send_typing(message.channel)
            whomst=message.server.id
            ensure_dict(whomst)
            hexes=users[whomst].get("dicthexes", defaulthexes)
            pixsize=users[whomst].get("pixsize",1)
            if message.attachments:
                img=message.attachments[0]["url"]
            else:
                img=message.content[len("!palettize "):]
            users[whomst]["lastimg"]=img
            print(message.attachments)
            print(hexes)
            if pixsize<0:
                downscale=-100*pixsize
                upscale=100
            else:
                downscale=100/pixsize
                upscale=100*pixsize #*6
            f=open("{:06}.pnm".format(fileid),"bw")
            f.write(colordither.dither_color(img,hexes,"#000000","img.transform('','{}%x{}%')".format(downscale,downscale)))
            f.close()
            subprocess.run(["convert", "{0:06}.pnm".format(fileid), "-filter", "point", "-resize", "{}x{}%".format(upscale,upscale), "{0:06}.png".format(fileid)])
#            subprocess.run(["convert", "{0:06}.pnm".format(fileid), "{0:06}.png".format(fileid)])
            await client.send_file(message.channel, "{0:06}.png".format(fileid))

        if message.content.startswith('!c64'):
            await client.send_typing(message.channel)
            wscale=2 #1.8+0.1/3
            downscale=100/pixsize
            upscale=100*pixsize #*6
            h=tuple(map(dehexcode,"#000000 #626262 #898989 #adadad #ffffff #9f4e44 #cb7e75 #6d5412 #a1683c #c9d487 #9ae29b #5cab5e #6abfc6 #887ecb #50459b #a057a3".split()))
            f=open("{:06}.pnm".format(fileid),"bw")
            f.write(colordither.dither_color(message.content[len("!c64 "):],h,"#000000","img.transform('','{}%x{}%')".format(downscale/wscale,downscale)))
            f.close()
            subprocess.run(["convert", "{0:06}.pnm".format(fileid), "-filter", "point", "-resize", "{}x{}%".format(upscale*wscale,upscale), "{0:06}.png".format(fileid)])
            await client.send_file(message.channel, "{0:06}.png".format(fileid))


        if message.content.startswith('!setpalette'):
            m = message.content[len("!setpalette "):]
            whomst=message.server.id
            if m.split()[0] in metapalette.keys():
                hexes=metapalette[m.split()[0]]+tuple(map(dehexcode,m.split()[1:]))
            else:
                hexes=tuple(map(dehexcode,m.split()))
            ensure_dict(whomst)
            users[whomst]["dicthexes"]=hexes
            msg = 'Palette set to {}'.format(" ".join(map(to_hex,hexes)))
            print(hexes)
            await client.send_message(message.channel, msg)

        if message.content.startswith('!repalette'):
            await client.send_typing(message.channel)
            m = message.content[len("!repalette "):]
            whomst=message.server.id
            if m.split()[0] in metapalette.keys():
                hexes=metapalette[m.split()[0]]+tuple(map(dehexcode,m.split()[1:]))
            else:
                hexes=tuple(map(dehexcode,m.split()))
            ensure_dict(whomst)
            users[whomst]["dicthexes"]=hexes
            msg = 'Palette set to {}'.format(" ".join(map(to_hex,hexes)))
            print(hexes)

            pixsize=users[whomst].get("pixsize",1)
            if pixsize<0:
                downscale=-100*pixsize
                upscale=100
            else:
                downscale=100/pixsize
                upscale=100*pixsize #*6
            img=users[whomst].get("lastimg","https://cdn.pixabay.com/photo/2016/10/29/14/24/why-1780726_960_720.png")
            f=open("{:06}.pnm".format(fileid),"bw")
            f.write(colordither.dither_color(img,hexes,"#000000","img.transform('','{}%x{}%')".format(downscale,downscale)))
            f.close()
            subprocess.run(["convert", "{0:06}.pnm".format(fileid), "-filter", "point", "-resize", "{}x{}%".format(upscale,upscale), "{0:06}.png".format(fileid)])
#            subprocess.run(["convert", "{0:06}.pnm".format(fileid), "{0:06}.png".format(fileid)])
            await client.send_file(message.channel, "{0:06}.png".format(fileid), content=msg)


        if message.content.startswith('!pixsize'):
            m = message.content[len("!pixsize "):]
            whomst=message.server.id
            ensure_dict(whomst)
            users[whomst]["pixsize"]=int(m)
            msg = 'Pixel size set to {}'.format(m)
            await client.send_message(message.channel, msg)
    except Exception:
        await client.send_message(message.channel, "```\n{}```".format(traceback.format_exc()))
        raise

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
