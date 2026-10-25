import json, os, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
m=json.load(open(S+'/tasks_in/M01.json'))
kind=sys.argv[1]  # q or j
per=int(sys.argv[2]) if len(sys.argv)>2 else 5
items=[]
for r in m['real']:
    p=f"{S}/crops/real2/{r['id']}_{kind}.png"
    if os.path.exists(p): items.append((r['id'],p))
W=1500
try:
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
except Exception:
    font=ImageFont.load_default()
sheets=[]
for k in range(0,len(items),per):
    chunk=items[k:k+per]
    ims=[]
    for qid,p in chunk:
        im=Image.open(p).convert('L')
        if im.width>W: im=im.resize((W,int(im.height*W/im.width)))
        lab=Image.new('L',(W,40),200)
        ImageDraw.Draw(lab).text((10,4),qid,fill=0,font=font)
        ims+= [lab, im]
    H=sum(i.height for i in ims)+10*len(ims)
    c=Image.new('L',(W,H),255); y=0
    for i in ims:
        c.paste(i,(0,y)); y+=i.height+10
    out=f"{S}/bp_M01_work/sheets/{kind}_{k//per:02d}.png"
    c.save(out); sheets.append((out,c.size,[q for q,_ in chunk]))
for s in sheets: print(s)
