import json, os, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
m=json.load(open(S+'/tasks_in/M01.json'))
kind=sys.argv[1]; maxh=int(sys.argv[2])
items=[]
for r in m['real']:
    p=f"{S}/crops/real2/{r['id']}_{kind}.png"
    if os.path.exists(p): items.append((r['id'],p))
W=1500
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
sheets=[]; cur=[]; curh=0
def flush():
    global cur,curh
    if not cur: return
    H=sum(i.height for _,i in cur)+10*len(cur)
    c=Image.new('L',(W,H),255); y=0
    for _,i in cur: c.paste(i,(0,y)); y+=i.height+10
    out=f"{S}/bp_M01_work/sheets/{kind}h_{len(sheets):02d}.png"; c.save(out)
    sheets.append((out,c.size,[q for q,_ in cur if q]))
    cur=[]; curh=0
for qid,p in items:
    im=Image.open(p).convert('L')
    if im.width!=W: im=im.resize((W,int(im.height*W/im.width)))
    lab=Image.new('L',(W,40),200); ImageDraw.Draw(lab).text((10,4),qid,fill=0,font=font)
    if curh+im.height+50>maxh: flush()
    cur+=[(None,lab),(qid,im)]; curh+=im.height+50
flush()
for s in sheets: print(s)
