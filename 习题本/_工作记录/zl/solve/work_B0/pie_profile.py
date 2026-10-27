import sys
import math
import numpy as np
from PIL import Image

path = sys.argv[1]
# boxes: list of (r0, r1, c0, c1)
boxes = eval(sys.argv[2])
im = np.array(Image.open(path).convert('L')).astype(float)


def sample(cx, cy, r, th):
    x = cx + r * math.sin(math.radians(th))
    y = cy - r * math.cos(math.radians(th))
    # bilinear
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    dx, dy = x - x0, y - y0
    v = (im[y0, x0] * (1 - dx) * (1 - dy) + im[y0, x0 + 1] * dx * (1 - dy)
         + im[y0 + 1, x0] * (1 - dx) * dy + im[y0 + 1, x0 + 1] * dx * dy)
    return v


def cls(v):
    if v < 90:
        return 'K'
    if v > 235:
        return 'W'
    if 150 <= v <= 215:
        return 'G'
    return 'M'


for idx, (r0, r1, c0, c1) in enumerate(boxes):
    cx = (c0 + c1) / 2.0
    cy = (r0 + r1) / 2.0
    R = ((c1 - c0) + (r1 - r0)) / 4.0
    print('pie', 'ABCD'[idx], 'center', cx, cy, 'R', R)
    for frac in (0.45, 0.6, 0.75, 0.88):
        r = R * frac
        step = 0.1
        ths = np.arange(0, 360, step)
        cl = [cls(sample(cx, cy, r, t)) for t in ths]
        # run length
        runs = []
        s = 0
        for i in range(1, len(cl) + 1):
            if i == len(cl) or cl[i] != cl[s]:
                runs.append((cl[s], ths[s], ths[i - 1]))
                s = i
        # compress: print runs longer than 0.5 deg or dark runs
        out = []
        for c, a, b in runs:
            if (b - a) >= 1.0 or c == 'K':
                out.append('%s[%.1f-%.1f]' % (c, a, b))
        print('  frac', frac, ' '.join(out))
