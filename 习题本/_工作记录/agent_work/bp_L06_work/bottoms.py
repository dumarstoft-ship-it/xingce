import json, sys
from PIL import Image, ImageDraw
base='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
d=json.load(open(base+'/tasks_in/L06.json'))
ids=[r['id'] for r in d['real'] if r.get('j_crop')]
strips=[]
for r in d['real']:
    p=r.get('j_crop')
    if not p: continue
    im=Image.open(p).convert('RGB')
    w,h=im.size
    top=im.crop((0,0,w,min(120,h)))
    bot=im.crop((0,max(0,h-200),w,h))
    strips.append((r['id'],top,bot))
def build(chunk,out):
    W=max(max(t.size[0],b.size[0]) for _,t,b in chunk)
    H=sum(t.size[1]+b.size[1]+40 for _,t,b in chunk)
    c=Image.new('RGB',(W,H),'white'); dr=ImageDraw.Draw(c); y=0
    for i,t,b in chunk:
        dr.rectangle([0,y,W,y+18],fill=(255,220,160)); dr.text((4,y+3),i+'  (top / bottom)',fill='black'); y+=20
        c.paste(t,(0,y)); y+=t.size[1]
        dr.rectangle([0,y,W,y+18],fill=(200,200,255)); y+=20
        c.paste(b,(0,y)); y+=b.size[1]
    c.save(out); print(out,c.size)
for k in range(0,len(strips),5):
    build(strips[k:k+5], f'mont/jb{k//5}.png')
