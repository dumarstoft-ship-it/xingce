import re, json
import numpy as np
from PIL import Image
HTML='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/out/zl_d15-21.html'
h=open(HTML,encoding='utf-8').read()
body=h[h.find('<body'):]
sets=re.split(r'<section class="set">', body)[1:]
items=[]
for s in sets:
    t=re.search(r'<span class="t">第 (\d+) 套', s).group(1)
    sec=None
    for m in re.finditer(r'<div class="mat-h">(.*?)</div>|<img class="chunk" src="file://([^"]+)"|<div class="q"><span class="no">(\d+)</span><img class="qi" src="file://([^"]+)"', s):
        if m.group(1): sec=m.group(1)[:3]
        elif m.group(2): items.append((t,sec,'M',None,m.group(2)))
        else: items.append((t,sec,'Q',m.group(3),m.group(4)))
def edge_stats(p):
    a=np.array(Image.open(p).convert('L')).astype(int)
    H,W=a.shape
    d=a<170
    def cnt(x): return int(x.sum())
    top=cnt(d[0:2,:]); bot=cnt(d[H-2:H,:]); left=cnt(d[:,0:2]); right=cnt(d[:,W-2:W])
    # first/last ink rows
    rows=np.where(d.any(axis=1))[0]; cols=np.where(d.any(axis=0))[0]
    return dict(H=H,W=W,top=top,bot=bot,left=left,right=right,
                ink_top=int(rows[0]) if len(rows) else -1, ink_bot=int(H-1-rows[-1]) if len(rows) else -1,
                ink_left=int(cols[0]) if len(cols) else -1, ink_right=int(W-1-cols[-1]) if len(cols) else -1)
out=[]
for it in items:
    st=edge_stats(it[4])
    out.append(dict(set=it[0],sec=it[1],kind=it[2],no=it[3],file=it[4].split('/')[-1],**st))
json.dump(out,open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/qa1521/zoom/edges.json','w'),ensure_ascii=False)
for o in out:
    flag=[]
    if o['top']>0: flag.append('TOP%d'%o['top'])
    if o['bot']>0: flag.append('BOT%d'%o['bot'])
    if o['left']>0: flag.append('L%d'%o['left'])
    if o['right']>0: flag.append('R%d'%o['right'])
    if flag:
        print(o['set'],o['sec'],o['kind'],o['no'],o['file'],o['W'],o['H'],' '.join(flag),'margins t/b/l/r',o['ink_top'],o['ink_bot'],o['ink_left'],o['ink_right'])
print(len(out))
