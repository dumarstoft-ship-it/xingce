import sys, math
from PIL import Image
import numpy as np
path = sys.argv[1]
im = np.array(Image.open(path).convert('L')).astype(float)
H, W = im.shape
print('size', W, H)
# centers given as args: cx,cy,r;...
specs = sys.argv[2].split(';')
for spec in specs:
    lab, cx, cy, r = spec.split(',')
    cx, cy, r = float(cx), float(cy), float(r)
    seq = []
    for deg10 in range(0, 3600, 5):
        a = math.radians(deg10/10.0)
        # clockwise from 12 o'clock
        vals = []
        for rr in np.linspace(0.35*r, 0.8*r, 10):
            x = cx + rr*math.sin(a); y = cy - rr*math.cos(a)
            xi, yi = int(round(x)), int(round(y))
            patch = im[yi-2:yi+3, xi-2:xi+3]
            vals.append(patch)
        p = np.concatenate([v.ravel() for v in vals])
        m, sd = p.mean(), p.std()
        if sd > 45: c = 'H'   # hatched
        elif m < 60: c = 'K'  # black
        elif m > 225: c = 'W' # white
        else: c = 'G'         # gray
        seq.append(c)
    # count
    from collections import Counter
    cnt = Counter(seq)
    tot = len(seq)
    print(lab, {k: f"{v/tot*100:.1f}%" for k, v in sorted(cnt.items())})
