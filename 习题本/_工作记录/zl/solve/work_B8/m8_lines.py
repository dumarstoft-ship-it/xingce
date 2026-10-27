# trace the four polylines in the Q4 option image: for each panel, find the dark-pixel y (mean) at the 4 vertex x positions
from PIL import Image
import numpy as np
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2705X-Z124_q.png').convert('L'))
panels = {'A':(70,190),'B':(240,360),'C':(410,535),'D':(580,677)}
for k,(y0,y1) in panels.items():
    sub = im[y0:y1, 105:410]
    cols = []
    for x in range(0, sub.shape[1]):
        ys = np.where(sub[:,x] < 100)[0]
        if len(ys): cols.append((x+105, ys.mean()+y0))
    xs = [c[0] for c in cols]
    print(k, "x range", min(xs), max(xs))
    # sample at vertices ~ x=115, 208, 303, 398
    for xv in (min(xs), 208, 304, max(xs)):
        best = min(cols, key=lambda c: abs(c[0]-xv))
        print("   x", best[0], "y", round(best[1],1))
