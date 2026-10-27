from PIL import Image
import numpy as np, math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2728X-Z122_q.png').convert('L')
a = np.array(im).astype(float)
H, W = a.shape
print(a.shape)
# find pies via non-white pixels in x range 100..430
nonwhite = a < 200
rows = nonwhite[:, 100:430].sum(axis=1)
blocks = []; inb = False
for y in range(H):
    if rows[y] > 0 and not inb: s = y; inb = True
    elif rows[y] == 0 and inb: blocks.append((s, y-1)); inb = False
if inb: blocks.append((s, H-1))
blocks = [b for b in blocks if b[1]-b[0] > 150]
print(blocks)
def classify(v):
    if v < 60: return 'K'      # black
    if v < 170: return 'G'     # dark gray
    if v < 240: return 'L'     # light gray
    return 'W'                 # white
for label, (y0, y1) in zip("ABCD", blocks):
    sub = nonwhite[y0:y1+1, 100:430]
    xs = np.where(sub.any(axis=0))[0]
    x0, x1 = xs.min()+100, xs.max()+100
    cx, cy = (x0+x1)/2, (y0+y1)/2
    R = ((x1-x0)+(y1-y0))/4
    seq = []
    for d10 in range(3600):
        th = math.radians(d10/10)
        vals = []
        for rr in (0.5, 0.6, 0.7, 0.8):
            x = cx + R*rr*math.sin(th); y = cy - R*rr*math.cos(th)
            vals.append(a[int(round(y)), int(round(x))])
        seq.append(classify(np.median(vals)))
    # count fraction for each class
    from collections import Counter
    c = Counter(seq)
    print(label, "center", (cx, cy), "R", R, {k: round(v/3600*100, 2) for k, v in sorted(c.items())})
    # transitions
    trans = []
    for i in range(3600):
        if seq[i] != seq[i-1]:
            trans.append((i/10, seq[i-1] + '->' + seq[i]))
    print("   transitions", trans)
