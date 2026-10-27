import sys, math
from PIL import Image
import numpy as np
from collections import Counter
# usage: pie_auto.py img x0 x1 "lab,y0,y1;lab,y0,y1..."  -> find circle bbox in region, measure sector colors
path = sys.argv[1]; x0, x1 = int(sys.argv[2]), int(sys.argv[3])
im = np.array(Image.open(path).convert('L')).astype(float)
for spec in sys.argv[4].split(';'):
    lab, y0, y1 = spec.split(','); y0, y1 = int(y0), int(y1)
    reg = im[y0:y1, x0:x1] < 200
    ys = np.where(reg.any(axis=1))[0]; xs = np.where(reg.any(axis=0))[0]
    top, bot = y0+ys.min(), y0+ys.max(); lef, rig = x0+xs.min(), x0+xs.max()
    cx, cy = (lef+rig)/2, (top+bot)/2; r = ((rig-lef)+(bot-top))/4
    seq = []
    for k in range(3600):
        a = math.radians(k/10)
        vals = []
        for rr in np.linspace(0.3*r, 0.85*r, 12):
            x = cx + rr*math.sin(a); y = cy - rr*math.cos(a)
            vals.append(im[int(round(y)), int(round(x))])
        m = np.median(vals)
        c = 'K' if m < 70 else ('W' if m > 220 else 'G')
        seq.append(c)
    cnt = Counter(seq)
    print(lab, 'center', (cx, cy), 'r', r, {k: f"{v/36:.1f}%" for k, v in sorted(cnt.items())})
