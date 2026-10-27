import json
import numpy as np
from PIL import Image
E=json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/qa1521/zoom/edges.json'))
base='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/'
def bands(mask):
    # return list of (start,end) runs of True
    runs=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if not v and s is not None: runs.append((s,i-1)); s=None
    if s is not None: runs.append((s,len(mask)-1))
    return runs
for o in E:
    a=np.array(Image.open(base+o['file']).convert('L')).astype(int)
    H,W=a.shape
    rowink=(a<230).sum(axis=1)
    r=bands(rowink>0)
    notes=[]
    if r:
        s,e=r[0]
        if s<=1 and (e-s+1)<=8 and len(r)>1 and r[1][0]-e>=4:
            notes.append('TOP-sliver h=%d px=%d'%(e-s+1,int(rowink[s:e+1].sum())))
        s,e=r[-1]
        if e>=H-2 and (e-s+1)<=8 and len(r)>1 and s-r[-2][1]>=4:
            notes.append('BOT-sliver h=%d px=%d'%(e-s+1,int(rowink[s:e+1].sum())))
    colink=(a<230).sum(axis=0)
    c=bands(colink>0)
    if c:
        s,e=c[0]
        if s<=1 and (e-s+1)<=10 and len(c)>1 and c[1][0]-e>=6:
            notes.append('LEFT-sliver w=%d px=%d'%(e-s+1,int(colink[s:e+1].sum())))
        s,e=c[-1]
        if e>=W-2 and (e-s+1)<=10 and len(c)>1 and s-c[-2][1]>=6:
            notes.append('RIGHT-sliver w=%d px=%d'%(e-s+1,int(colink[s:e+1].sum())))
    if notes: print(o['set'],o['sec'],o['kind'],o['no'],o['file'],W,H,'; '.join(notes))
