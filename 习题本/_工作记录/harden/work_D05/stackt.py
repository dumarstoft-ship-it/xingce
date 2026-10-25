import sys
from PIL import Image, ImageDraw, ImageFont
base='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/teacher/crops/'
out=sys.argv[1]; ids=sys.argv[2:]
ims=[]
try:
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except Exception:
    f=None
for i in ids:
    im=Image.open(base+i+'.png').convert('RGB')
    lab=Image.new('RGB',(im.width,30),(200,200,200))
    ImageDraw.Draw(lab).text((6,3),i,fill=(0,0,0),font=f)
    ims+= [lab, im]
W=max(x.width for x in ims); H=sum(x.height for x in ims)
c=Image.new('RGB',(W,H),(255,255,255)); y=0
for x in ims: c.paste(x,(0,y)); y+=x.height
c.save(out); print(out,c.size)
