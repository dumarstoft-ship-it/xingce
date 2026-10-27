# Measure pie sector shares for MK2728X Q2 options by gray level along a ring
from PIL import Image
import numpy as np, math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2728X-Z122_q.png').convert('L')
a = np.array(im).astype(float)
print(a.shape)
boxes={'A':(100,100,430,420),'B':(100,440,430,760),'C':(100,785,430,1105),'D':(100,1125,430,1445)}
def cls(v):
    if v > 235: return 'white'
    if v > 180: return 'light'
    if v > 60: return 'dark'
    return 'black'
for k,(x0,y0,x1,y1) in boxes.items():
    sub = a[y0:y1, x0:x1]
    dark = sub < 200
    ys, xs = np.nonzero(dark)
    cx = (xs.min()+xs.max())/2; cy = (ys.min()+ys.max())/2
    R = ((xs.max()-xs.min())+(ys.max()-ys.min()))/4
    counts = {}
    N = 7200
    for i in range(N):
        th = 2*math.pi*i/N
        vals = []
        for rr in (0.55, 0.65, 0.75):
            x = cx + rr*R*math.sin(th); y = cy - rr*R*math.cos(th)
            vals.append(sub[int(round(y)), int(round(x))])
        c = cls(float(np.median(vals)))
        counts[c] = counts.get(c,0)+1
    print(k, 'center', (round(cx+x0,1), round(cy+y0,1)), 'R', R, {c: round(100*n/N,2) for c,n in counts.items()})
