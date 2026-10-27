import re, json
import numpy as np
import cv2
from PIL import Image
SP='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
h=open(SP+'zl/out/zl_d15-21.html',encoding='utf-8').read()
files=[]
for m in re.finditer(r'src="file://([^"]+\.png)"', h):
    if m.group(1) not in files: files.append(m.group(1))
res=[]
k=np.ones((9,9),np.uint8)
for p in files:
    a=np.array(Image.open(p).convert('L'))
    light=((a>=228)&(a<=249)).astype(np.uint8)
    dark=(a<215).astype(np.uint8)
    dd=cv2.dilate(dark,k)
    m=(light&(1-dd)).astype(np.uint8)
    mc=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    n,lab,stats,cent=cv2.connectedComponentsWithStats(mc,8)
    boxes=[]
    for i in range(1,n):
        x,y,w,hh,area=stats[i]
        cnt=int(m[y:y+hh,x:x+w].sum())
        if cnt>=120: boxes.append((int(x),int(y),int(w),int(hh),cnt))
    if boxes: res.append((p.split('/')[-1],a.shape,boxes))
for r in res:
    print(r[0], r[1], r[2][:6], len(r[2]))
print(len(res))
