import sys
import numpy as np
from PIL import Image

path = sys.argv[1]
im = np.array(Image.open(path).convert('L')).astype(float)
h, w = im.shape
print('size', w, h)
dark = im < 160
# restrict to x in [100, 430]
sub = dark[:, 100:430]
rows = sub.sum(axis=1)
# find vertical runs of rows with dark pixels
runs = []
inrun = False
for y in range(h):
    if rows[y] > 0 and not inrun:
        start = y; inrun = True
    elif rows[y] == 0 and inrun:
        runs.append((start, y)); inrun = False
if inrun: runs.append((start, h))
for a, b in runs:
    if b - a > 100:
        blk = sub[a:b]
        cols = np.where(blk.sum(axis=0) > 0)[0]
        x0, x1 = cols.min() + 100, cols.max() + 100
        print('pie rows', a, b - 1, 'cols', x0, x1, 'center', (x0 + x1) / 2, (a + b - 1) / 2, 'r', (x1 - x0) / 2, (b - 1 - a) / 2)
