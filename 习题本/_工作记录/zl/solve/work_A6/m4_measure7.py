from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p1.png').convert('L')
a = np.array(im).astype(int)
for y in range(40, 400):
    seg = a[y, 137:143]
    if (seg < 180).sum() >= 3:
        print("inner tick y", y, seg.tolist())
for y in range(300, 420):
    n = (a[y, 137:800] < 128).sum()
    if n > 400: print("x-axis row", y, n)
