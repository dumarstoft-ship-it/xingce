import math
from collections import Counter
from PIL import Image
import numpy as np

p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2733X-Z118_q.png'
img = Image.open(p).convert('L')
im = np.array(img).astype(float)
H, W = im.shape
print('size', W, H)
# column/row profile to locate pies: dark pixels in x range 100..430
mask = im < 200
# find pies by vertical bands
rows = mask[:, 100:440].sum(axis=1)
inpie = rows > 5
bands = []
start = None
for y in range(H):
    if inpie[y] and start is None:
        start = y
    if not inpie[y] and start is not None:
        if y - start > 100:
            bands.append((start, y))
        start = None
if start is not None and H - start > 100:
    bands.append((start, H))
print('bands', bands)

def classify_window(x, y):
    xi, yi = int(round(x)), int(round(y))
    win = im[yi - 3:yi + 4, xi - 3:xi + 4]
    m, s = win.mean(), win.std()
    if s > 45:
        return 'X'  # checkered
    if m > 215:
        return 'W'
    if m < 60:
        return 'K'
    if 70 <= m <= 130:
        return 'G'
    return '?'

for label, (y0, y1) in zip('ABCD', bands):
    sub = mask[y0:y1, 100:440]
    ys, xs = np.where(sub)
    cx = (xs.min() + xs.max()) / 2.0 + 100
    cy = (ys.min() + ys.max()) / 2.0 + y0
    r = ((xs.max() - xs.min()) + (ys.max() - ys.min())) / 4.0
    N = 3600
    labs = []
    for i in range(N):
        a = 2 * math.pi * i / N
        votes = Counter()
        for f in (0.45, 0.6, 0.75):
            votes[classify_window(cx + f * r * math.sin(a), cy - f * r * math.cos(a))] += 1
        labs.append(votes.most_common(1)[0][0])
    runs = []
    cur, s0 = labs[0], 0
    for i in range(1, N):
        if labs[i] != cur:
            runs.append((cur, s0, i)); cur, s0 = labs[i], i
    runs.append((cur, s0, N))
    cnt = Counter(labs)
    print(label, 'center (%.1f, %.1f) r %.1f' % (cx, cy, r))
    print('   runs:', ' '.join('%s[%.1f-%.1f]' % (c, s / 10, e / 10) for c, s, e in runs if e - s >= 3))
    print('   shares %:', {c: round(v / N * 100, 2) for c, v in sorted(cnt.items())})
