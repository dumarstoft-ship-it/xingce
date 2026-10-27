import math
from PIL import Image
import numpy as np

p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2736F-Z130_q.png'
im = np.array(Image.open(p).convert('L')).astype(int)
H, W = im.shape
# pies are roughly in x 100..380; y bands
bands = {'A': (105, 365), 'B': (400, 665), 'C': (695, 960), 'D': (990, 1254)}
for k, (y0, y1) in bands.items():
    sub = im[y0:y1, 100:380]
    ys, xs = np.where(sub < 128)
    # circle bounding box from dark pixels
    xmin, xmax, ymin, ymax = xs.min(), xs.max(), ys.min(), ys.max()
    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0
    r = ((xmax - xmin) + (ymax - ymin)) / 4.0
    print(k, 'bbox', xmin + 100, xmax + 100, ymin + y0, ymax + y0, 'center', cx + 100, cy + y0, 'r', r)
    # sample along angles, at several radii; classify gray level
    res = []
    N = 3600
    for i in range(N):
        a = 2 * math.pi * i / N  # clockwise from 12 o'clock
        vals = []
        for f in (0.45, 0.55, 0.65, 0.75, 0.85):
            x = cx + f * r * math.sin(a)
            y = cy - f * r * math.cos(a)
            vals.append(sub[int(round(y)), int(round(x))])
        v = int(np.median(vals))
        if v < 60:
            c = 'K'
        elif v < 160:
            c = 'G'
        elif v < 230:
            c = 'L'
        else:
            c = 'W'
        res.append(c)
    # run-length
    runs = []
    cur = res[0]; start = 0
    for i in range(1, N):
        if res[i] != cur:
            runs.append((cur, start, i))
            cur = res[i]; start = i
    runs.append((cur, start, N))
    for c, s, e in runs:
        print('   ', c, 'deg %.1f-%.1f' % (s / 10, e / 10), 'span %.1f deg = %.2f%%' % ((e - s) / 10, (e - s) / N * 100))
    from collections import Counter
    cnt = Counter(res)
    print('  totals', {c: round(v / N * 100, 2) for c, v in cnt.items()})
