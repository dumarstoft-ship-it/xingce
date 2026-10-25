import json, os, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
m=json.load(open(S+'/tasks_in/M01.json'))
kind=sys.argv[1]; per=int(sys.argv[2])
items=[]
for r in m['real']:
    p=r[{'q':'q_crop','j':'j_crop','s':'s_crop'}[kind]]
    if p and os.path.exists(p): items.append((r['id'],p))
W=1400
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except Exception: font=ImageFont.load_default()
for k in range(0,len(items),per):
    chunk=items[k:k+per]; ims=[]
    for qid,p in chunk:
        im=Image.open(p).convert('L')
        if im.width>W: im=im.resize((W,int(im.height*W/im.width)))
        lab=Image.new('L',(W,36),170); ImageDraw.Draw(lab).text((10,3),qid+'  '+str(Image.open(p).size),fill=0,font=font)
        # border box to make crop edges visible
        bx=Image.new('L',(im.width+4,im.height+4),0); bx.paste(im,(2,2))
        ims+=[lab,bx]
    H=sum(i.height for i in ims)+8*len(ims)
    c=Image.new('L',(W+4,H),255); y=0
    for i in ims: c.paste(i,(0,y)); y+=i.height+8
    out=f"{S}/bp_M01_work/sheets2/{kind}_{k//per:02d}.png"; c.save(out); print(out,c.size,[q for q,_ in chunk])
