from PIL import Image
import numpy as np, math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2723X-Z125_q.png').convert('L')
a = np.array(im).astype(int)
H,W = a.shape
print(W,H)
# find pies: dark pixels in columns 100-400
# Column profile of non-white
mask = a < 200
rows = np.where(mask[:, 100:400].any(axis=1))[0]
# group rows into blocks
blocks=[]
start=rows[0]; prev=rows[0]
for r in rows[1:]:
    if r-prev>3:
        blocks.append((start,prev)); start=r
    prev=r
blocks.append((start,prev))
print(blocks)

labels = ['A','B','C','D']
for lab,(r0,r1) in zip(labels, blocks[1:]):
    sub = mask[r0:r1+1, 100:420]
    cols = np.where(sub.any(axis=0))[0] + 100
    c0, c1 = cols[0], cols[-1]
    cy = (r0+r1)/2; cx = (c0+c1)/2
    R = ((r1-r0)+(c1-c0))/4
    # sample around circle at radius 0.6R, angle from 12 o'clock clockwise
    cls=[]
    for k in range(3600):
        th = math.radians(k/10)
        x = cx + 0.6*R*math.sin(th); y = cy - 0.6*R*math.cos(th)
        v = a[int(round(y)), int(round(x))]
        if v < 60: c='K'
        elif v < 200: c='G'
        else: c='W'
        cls.append(c)
    # find transitions
    trans=[]
    for k in range(3600):
        if cls[k]!=cls[k-1]:
            trans.append((k/10, cls[k-1], cls[k]))
    # fraction of each class
    from collections import Counter
    cnt = Counter(cls)
    print(lab, 'center', (cx,cy), 'R', R, {c: round(cnt[c]/36,2) for c in cnt}, trans)
