from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2702X-Z125_q.png').convert('L')
a = np.array(im)
print(a.shape)
# find dark columns region between x=80..620, y=100..380
for xc in (172, 350, 527):
    col = a[90:390, xc]
    d = np.nonzero(col < 100)[0]
    print("x", xc, "dark rows from", d.min()+90, "to", d.max()+90)
# baseline: find the horizontal axis row
for y in range(360, 390):
    row = a[y, 85:615]
    if (row < 128).mean() > 0.8: print("axis row", y)
