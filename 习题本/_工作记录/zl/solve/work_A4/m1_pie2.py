import math
from PIL import Image
import numpy as np

p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2736F-Z130_q.png'
im = np.array(Image.open(p).convert('L')).astype(float)

def bilinear(x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    dx, dy = x - x0, y - y0
    v = (im[y0, x0] * (1 - dx) * (1 - dy) + im[y0, x0 + 1] * dx * (1 - dy)
         + im[y0 + 1, x0] * (1 - dx) * dy + im[y0 + 1, x0 + 1] * dx * dy)
    return v

def find_center(y0, y1):
    sub = im[y0:y1, 100:380]
    ys, xs = np.where(sub < 128)
    cx = (xs.min() + xs.max()) / 2.0 + 100
    cy = (ys.min() + ys.max()) / 2.0 + y0
    r = ((xs.max() - xs.min()) + (ys.max() - ys.min())) / 4.0
    return cx, cy, r

bands = {'A': (105, 365), 'D': (990, 1254), 'B': (400, 665), 'C': (695, 960)}
for k, (y0, y1) in bands.items():
    cx, cy, r = find_center(y0, y1)
    print('pie', k, 'center', cx, cy, 'r', r)
    for f in (0.5, 0.7, 0.85):
        R = f * r
        N = 7200
        vals = []
        for i in range(N):
            a = 2 * math.pi * i / N
            x = cx + R * math.sin(a)
            y = cy - R * math.cos(a)
            vals.append(bilinear(x, y))
        vals = np.array(vals)
        # classify with thresholds; print transitions
        def cls(v):
            if v < 50: return 'K'
            if v < 170: return 'G'
            return 'W'
        labs = [cls(v) for v in vals]
        trans = []
        for i in range(N):
            if labs[i] != labs[i - 1]:
                trans.append((i / 20.0, labs[i - 1] + '>' + labs[i]))
        print('  f=%.2f R=%.1f transitions:' % (f, R), ' '.join('%.2f:%s' % t for t in trans))
