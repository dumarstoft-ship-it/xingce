from PIL import Image
import numpy as np, math
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2718X-Z120_q.png').convert('L')).astype(float)
H, W = im.shape
# find pies: dark pixels in x range 100-450
regions = {'A':(100,460), 'B':(470,830), 'C':(835,1195), 'D':(1200,1545)}
for k,(y0,y1) in regions.items():
    sub = im[y0:y1, 100:460]
    ys, xs = np.where(sub < 100)
    # bounding of circle outline
    top, bot = ys.min()+y0, ys.max()+y0
    left, right = xs.min()+100, xs.max()+100
    cy, cx = (top+bot)/2, (left+right)/2
    R = ((bot-top)+(right-left))/4
    # sample intensity along angles (clockwise from 12 o'clock) averaged over radii 0.35R..0.9R with patch smoothing
    angs = np.arange(0,360,0.5)
    prof = []
    for a in angs:
        t = math.radians(a)
        vals = []
        for rr in np.linspace(0.35*R, 0.9*R, 40):
            x = cx + rr*math.sin(t); y = cy - rr*math.cos(t)
            xi, yi = int(round(x)), int(round(y))
            vals.append(im[yi-2:yi+3, xi-2:xi+3].mean())
        prof.append(np.mean(vals))
    prof = np.array(prof)
    print(k, "center", cx, cy, "R", R)
    # print compressed profile: label by intensity bucket
    def lab(v):
        if v < 60: return 'K'   # black
        if v < 150: return 'G'  # gray
        if v < 215: return 'H'  # hatched
        if v < 248: return 'D'  # dotted
        return 'W'
    labs = [lab(v) for v in prof]
    # run-length
    runs = []
    cur = labs[0]; start = 0
    for i,l in enumerate(labs):
        if l != cur:
            runs.append((cur, angs[start], angs[i]-angs[start])); cur = l; start = i
    runs.append((cur, angs[start], 360-angs[start]))
    print("  runs (label, start, width deg, pct):")
    for r in runs:
        if r[2] >= 1.0:
            print("   ", r[0], r[1], r[2], round(r[2]/360*100,2))
