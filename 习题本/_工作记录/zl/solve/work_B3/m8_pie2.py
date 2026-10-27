from PIL import Image
import numpy as np, math
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2732X-Z120_q.png').convert('L')).astype(int)
bands = [(100,430),(450,770),(795,1115),(1145,1460)]
X0 = 105
for label,(y0,y1) in zip("ABCD", bands):
    sub = im[y0:y1, X0:440]
    ys, xs = np.where(sub < 60)
    top, bot = ys.min()+y0, ys.max()+y0
    left, right = xs.min()+X0, xs.max()+X0
    cx, cy = (left+right)/2, (top+bot)/2
    R = min(right-left, bot-top)/2
    counts = {}; N = 7200
    for i in range(N):
        ang = 2*math.pi*(i+0.5)/N
        vals = []
        for rr in (0.4, 0.55, 0.7, 0.85):
            x = cx + rr*R*math.sin(ang); y = cy - rr*R*math.cos(ang)
            vals.append(im[int(round(y)), int(round(x))])
        v = int(np.median(vals))
        c = "black" if v < 50 else "dark" if v < 150 else "light" if v < 215 else "white"
        counts[c] = counts.get(c,0)+1
    print(label, "bbox x", left, right, "y", top, bot, "center", (cx,cy), "R", R, {k: round(v/N*100,1) for k,v in sorted(counts.items())})
