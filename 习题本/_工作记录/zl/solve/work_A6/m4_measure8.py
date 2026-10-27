from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p1.png').convert('L')
a = np.array(im).astype(int)
y0, y7 = 390.2, 56.8
scale = (y0-y7)/7
res = []
for y in range(60, 385):
    row = a[y, 137:820] < 140
    run = 0; start=None
    for i, v in enumerate(row):
        if v:
            if run == 0: start = i
            run += 1
        else:
            if run >= 25: res.append((y, 137+start, 137+start+run-1, run))
            run = 0
for y, s, e, r in res:
    print("row %d x %d-%d len %d value=%.3f" % (y, s, e, r, (y0-y)/scale))
