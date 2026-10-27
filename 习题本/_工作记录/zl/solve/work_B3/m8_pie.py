from PIL import Image
import numpy as np, math
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2732X-Z120_q.png').convert('L')).astype(int)
H, W = im.shape
print("size", W, H)
# locate pies: find dark outline pixels in x range 100-430, group by y bands
bands = [(100,430),(450,770),(795,1115),(1145,1460)]
for label,(y0,y1) in zip("ABCD", bands):
    sub = im[y0:y1, 90:440]
    ys, xs = np.where(sub < 60)
    # bounding box of the circle outline (dark pixels incl. black wedge) -> use extreme points
    top, bot = ys.min()+y0, ys.max()+y0
    left, right = xs.min()+90, xs.max()+90
    cx, cy = (left+right)/2, (top+bot)/2
    R = (right-left)/2
    counts = {}
    seq = []
    N = 3600
    for i in range(N):
        ang = 2*math.pi*i/N  # clockwise from 12 o'clock
        vals = []
        for rr in (0.45, 0.6, 0.75):
            x = cx + rr*R*math.sin(ang); y = cy - rr*R*math.cos(ang)
            vals.append(im[int(round(y)), int(round(x))])
        v = int(np.median(vals))
        if v < 50: c = "black"
        elif v < 150: c = "dark"
        elif v < 215: c = "light"
        else: c = "white"
        seq.append(c)
        counts[c] = counts.get(c,0)+1
    print(label, "center", (cx,cy), "R", R, {k: round(v/N*100,1) for k,v in counts.items()})
