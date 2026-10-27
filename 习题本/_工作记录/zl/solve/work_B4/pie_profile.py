import sys, math
from PIL import Image
import numpy as np
path = sys.argv[1]; xlo, xhi = int(sys.argv[2]), int(sys.argv[3])
im = Image.open(path).convert('L'); a = np.array(im).astype(int)
H, W = a.shape
dark_rows = (a[:, xlo:xhi] < 200).sum(axis=1)
segs = []; inseg = False
for y in range(H):
    if dark_rows[y] > 5 and not inseg: start = y; inseg = True
    elif dark_rows[y] <= 5 and inseg: segs.append((start, y)); inseg = False
if inseg: segs.append((start, H))
segs = [s for s in segs if s[1]-s[0] > 100]
print(segs)
out = {}
for label, (y0, y1) in zip('ABCD', segs):
    sub = a[y0:y1, xlo:xhi]
    ys, xs = np.where(sub < 200)
    cx = (xs.min()+xs.max())/2 + xlo; cy = (ys.min()+ys.max())/2 + y0
    R = ((xs.max()-xs.min()) + (ys.max()-ys.min()))/4
    N = 1440
    prof = []
    for k in range(N):
        th = 2*math.pi*k/N
        vals = []
        for rr in np.linspace(0.15, 0.9, 150):
            x = cx + rr*R*math.sin(th); y = cy - rr*R*math.cos(th)
            vals.append(a[int(round(y)), int(round(x))])
        vals = np.array(vals)
        prof.append(((vals<90).mean(), ((vals>=90)&(vals<215)).mean(), (vals>=215).mean()))
    out[label] = (cx, cy, R, prof)
    print(label, 'center', cx, cy, 'R', R)
import pickle; pickle.dump(out, open(sys.argv[4], 'wb'))
