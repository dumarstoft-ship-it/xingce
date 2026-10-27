# Measure pie sector fractions in MK2706X-Z115_q.png
import numpy as np
from PIL import Image
import math

path = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2706X-Z115_q.png'
a = np.array(Image.open(path).convert('L')).astype(int)
H, W = a.shape

# locate pies: within x in [95, 320], find row bands with non-white pixels
xs0, xs1 = 95, 320
mask = a[:, xs0:xs1] < 200
rowhas = mask.sum(axis=1) > 0
bands = []
inb = False
for y in range(H):
    if rowhas[y] and not inb:
        start = y; inb = True
    elif not rowhas[y] and inb:
        bands.append((start, y - 1)); inb = False
if inb:
    bands.append((start, H - 1))
bands = [b for b in bands if b[1] - b[0] > 100]
print('bands', bands)

labels = 'ABCD'
for lab, (y0, y1) in zip(labels, bands):
    sub = mask[y0:y1 + 1]
    cols = np.where(sub.sum(axis=0) > 0)[0]
    x0, x1 = cols.min() + xs0, cols.max() + xs0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(x1 - x0, y1 - y0) / 2
    # classify sectors by sampling radial segments
    cls = []
    for k in range(3600):
        ang = k / 10.0  # degrees clockwise from 12 o'clock
        th = math.radians(ang)
        vals = []
        for rr in np.linspace(0.35 * R, 0.85 * R, 40):
            x = cx + rr * math.sin(th)
            y = cy - rr * math.cos(th)
            vals.append(a[int(round(y)), int(round(x))])
        vals = np.array(vals)
        mean = vals.mean(); std = vals.std()
        dark = (vals < 70).mean(); light = (vals > 200).mean(); mid = ((vals >= 70) & (vals <= 200)).mean()
        if std > 50 and dark > 0.1 and light > 0.1:
            c = 'H'  # hatched
        elif mid > 0.6:
            c = 'G'
        elif light > 0.8:
            c = 'W'
        elif dark > 0.8:
            c = 'K'
        else:
            c = '?'
        cls.append(c)
    from collections import Counter
    cnt = Counter(cls)
    tot = sum(cnt.values())
    print(lab, 'center', (cx, cy), 'R', R, {k: round(v / tot * 100, 1) for k, v in sorted(cnt.items())})
