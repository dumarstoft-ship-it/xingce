from PIL import Image
import numpy as np, math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2733X-Z118_q.png').convert('L')
a = np.array(im).astype(int)
print(a.shape)
# pies in x range 100..430; find y-ranges of each pie by looking at dark pixel rows in x 100..430
H, W = a.shape
cols = slice(100, 440)
dark_rows = (a[:, cols] < 200).sum(axis=1)
# segments
segs = []
inseg = False
for y in range(H):
    if dark_rows[y] > 5 and not inseg:
        start = y; inseg = True
    elif dark_rows[y] <= 5 and inseg:
        segs.append((start, y)); inseg = False
if inseg: segs.append((start, H))
segs = [s for s in segs if s[1]-s[0] > 100]
print(segs)
for label, (y0, y1) in zip('ABCD', segs):
    sub = a[y0:y1, 100:440]
    ys, xs = np.where(sub < 200)
    cx = (xs.min()+xs.max())/2 + 100; cy = (ys.min()+ys.max())/2 + y0
    R = ((xs.max()-xs.min()) + (ys.max()-ys.min()))/4
    # sample angles, clockwise from 12 o'clock
    counts = {}
    seq = []
    N = 3600
    for k in range(N):
        th = 2*math.pi*k/N
        vals = []
        for rr in np.linspace(0.35, 0.85, 12):
            x = cx + rr*R*math.sin(th); y = cy - rr*R*math.cos(th)
            vals.append(a[int(round(y)), int(round(x))])
        vals = np.array(vals)
        # classify
        m = vals.mean(); sd = vals.std()
        if sd > 60: c = 'check'
        elif m > 200: c = 'white'
        elif m < 60: c = 'black'
        else: c = 'gray'
        seq.append(c)
    from collections import Counter
    cnt = Counter(seq)
    print(label, 'center', cx, cy, 'R', R, {k: round(v/N*100,1) for k, v in cnt.items()})
