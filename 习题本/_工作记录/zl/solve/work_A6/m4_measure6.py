from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p1.png').convert('L')
a = np.array(im).astype(int)
H, W = a.shape
# left axis
for x in range(100, 170):
    n = (a[40:400, x] < 128).sum()
    if n > 200: print("axis col", x, n)
