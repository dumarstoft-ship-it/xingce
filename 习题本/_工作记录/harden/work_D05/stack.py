import sys, json
from PIL import Image, ImageDraw, ImageFont
# usage: stack.py out.png id1 id2 ... (j images from real2)
base='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/real2/'
out=sys.argv[1]
ids=sys.argv[2:]
ims=[]
for i in ids:
    p=base+i+'_j.png'
    try:
        im=Image.open(p).convert('RGB')
    except Exception as e:
        print('missing',p,e); continue
    W=1200
    if im.width!=W:
        im=im.resize((W,int(im.height*W/im.width)))
    lab=Image.new('RGB',(W,34),(200,200,200))
    d=ImageDraw.Draw(lab)
    try:
        f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
    except Exception:
        f=None
    d.text((8,4),'J '+i,fill=(0,0,0),font=f)
    ims.append(lab); ims.append(im)
H=sum(x.height for x in ims)
canvas=Image.new('RGB',(1200,H),(255,255,255))
y=0
for x in ims:
    canvas.paste(x,(0,y)); y+=x.height
canvas.save(out)
print(out, canvas.size)
