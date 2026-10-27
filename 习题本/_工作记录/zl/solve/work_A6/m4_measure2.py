from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L')
a = np.array(im).astype(int)
# tick marks to the left of axis at x=125..130
for y in range(40, 400):
    seg = a[y, 124:131]
    if (seg < 160).sum() >= 4:
        print("tick y", y, seg.tolist())
# bottom axis line: row with many dark pixels
for y in range(300, 420):
    n = (a[y, 132:800] < 128).sum()
    if n > 400:
        print("x-axis row", y, n)
