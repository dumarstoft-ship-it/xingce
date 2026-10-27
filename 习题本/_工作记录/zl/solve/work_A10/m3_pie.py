from PIL import Image
import numpy as np, math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2718X-Z120_q.png').convert('L')
a = np.array(im).astype(float)
print(a.shape)
# find circle bounding boxes in x range 100..450
H, W = a.shape
dark = a < 100
cols = dark[:, 100:460]
rows_dark = cols.sum(axis=1)
# segment rows into blocks
blocks = []
inb = False
for y in range(H):
    if rows_dark[y] > 0 and not inb:
        start = y; inb = True
    elif rows_dark[y] == 0 and inb:
        blocks.append((start, y-1)); inb = False
if inb: blocks.append((start, H-1))
blocks = [b for b in blocks if b[1]-b[0] > 100]
print(blocks)
res = {}
for label, (y0, y1) in zip("ABCD", blocks):
    sub = dark[y0:y1+1, 100:460]
    xs = np.where(sub.any(axis=0))[0]
    x0, x1 = xs.min()+100, xs.max()+100
    cx, cy = (x0+x1)/2, (y0+y1)/2
    R = ((x1-x0)+(y1-y0))/4
    print(label, "bbox", x0, x1, y0, y1, "center", cx, cy, "R", R)
    # sample along circle at several radii, classify mean intensity in small patch
    prof = []
    for deg10 in range(0, 3600):
        th = math.radians(deg10/10)
        vals = []
        for rr in np.linspace(0.35, 0.85, 11):
            x = cx + R*rr*math.sin(th); y = cy - R*rr*math.cos(th)
            vals.append(a[int(round(y)), int(round(x))])
        prof.append(np.mean(vals))
    res[label] = (cx, cy, R, np.array(prof))
np.save('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/work_A10/pie_prof.npy', np.array([res[k][3] for k in "ABCD"]))
# Find boundary lines: angles where the profile is very dark across all radii (a radial line)
for label in "ABCD":
    cx, cy, R, prof = res[label]
    # radial line detection: check pixels along ray at many radii are dark
    lines = []
    for deg10 in range(0, 3600):
        th = math.radians(deg10/10)
        cnt = 0; tot = 0
        for rr in np.linspace(0.2, 0.9, 30):
            x = cx + R*rr*math.sin(th); y = cy - R*rr*math.cos(th)
            tot += 1
            if a[int(round(y)), int(round(x))] < 90: cnt += 1
        lines.append(cnt/tot)
    lines = np.array(lines)
    # report angle ranges where lines > 0.8
    ranges = []
    inr = False
    for i, v in enumerate(lines):
        if v > 0.8 and not inr: s = i; inr = True
        elif v <= 0.8 and inr: ranges.append((s/10, (i-1)/10)); inr = False
    if inr: ranges.append((s/10, 359.9))
    print(label, "dark-ray ranges (deg clockwise from 12):", ranges)
