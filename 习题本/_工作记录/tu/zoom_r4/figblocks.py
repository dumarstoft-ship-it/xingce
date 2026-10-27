import json, re, sys
import numpy as np
from PIL import Image
spans=json.load(open('tu/zoom_r4/spans.json'))
def figblocks(fn, page, y0, y1, d):
    base=fn[:-5]
    im=Image.open(f'pagecache/{base}__p{page}_200.png').convert('L')
    a=np.array(im); s=im.size[0]/d['pages'][page-1]['width']
    H=d['pages'][page-1]['height']
    lines=[l for l in d['pages'][page-1]['lines'] if l['top']>=y0-1 and l['bottom']<=y1+1]
    mask=np.zeros(a.shape[0],bool)
    for l in lines:
        mask[int((l['top']-1)*s):int((l['bottom']+1)*s)+1]=True
    ink=(a<160).sum(axis=1)>2
    rows=[r for r in range(int(y0*s),min(int(y1*s),a.shape[0])) if ink[r] and not mask[r]]
    blocks=[]
    for r in rows:
        if blocks and r-blocks[-1][1]<=12: blocks[-1][1]=r
        else: blocks.append([r,r])
    return [(round(b0/s,1),round(b1/s,1)) for b0,b1 in blocks if b1-b0>8], len(lines)
for k,(fn,start,end) in spans.items():
    d=json.load(open('lines/'+fn))
    sp,si,st=start; ep,ei,et=end
    out=[]
    for pg in range(sp,ep+1):
        y0 = st if pg==sp else 40
        y1 = et if pg==ep else d['pages'][pg-1]['height']-35
        fb,nl=figblocks(fn,pg,y0,y1,d)
        out.append(f'p{pg}[{y0:.0f}-{y1:.0f}] lines={nl} figs={fb}')
    print(k, ' | '.join(out))
