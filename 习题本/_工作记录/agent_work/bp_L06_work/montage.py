import json, sys
from PIL import Image, ImageDraw
base='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
d=json.load(open(base+'/tasks_in/L06.json'))
key=sys.argv[1]  # q_crop or j_crop
ids=sys.argv[2].split(',')
out=sys.argv[3]
recs={r['id']:r for r in d['real']}
ims=[]
for i in ids:
    p=recs[i][key]
    if not p: continue
    im=Image.open(p).convert('RGB')
    ims.append((i,im))
W=max(im.size[0] for _,im in ims)
H=sum(im.size[1]+30 for _,im in ims)
canvas=Image.new('RGB',(W,H),'white')
dr=ImageDraw.Draw(canvas)
y=0
for i,im in ims:
    dr.rectangle([0,y,W,y+28],fill=(255,230,180))
    dr.text((5,y+5),i,fill='black')
    y+=30
    canvas.paste(im,(0,y)); y+=im.size[1]
canvas.save(out)
print(out,canvas.size)
