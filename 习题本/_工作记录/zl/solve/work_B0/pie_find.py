import sys
import numpy as np
from PIL import Image

path = sys.argv[1]
im = np.array(Image.open(path).convert('L')).astype(int)
H, W = im.shape
print('size', W, H)
# find rows/cols with dark pixels in x range 105..W
x0 = 105
sub = im[:, x0:]
dark = sub < 128
rows = np.where(dark.any(axis=1))[0]
# group rows into contiguous blocks
blocks = []
start = rows[0]
prev = rows[0]
for r in rows[1:]:
    if r != prev + 1:
        blocks.append((start, prev))
        start = r
    prev = r
blocks.append((start, prev))
for b in blocks:
    if b[1] - b[0] > 100:
        cols = np.where(dark[b[0]:b[1] + 1].any(axis=0))[0]
        print('block rows', b, 'cols', cols.min() + x0, cols.max() + x0, 'h', b[1] - b[0] + 1, 'w', cols.max() - cols.min() + 1)
