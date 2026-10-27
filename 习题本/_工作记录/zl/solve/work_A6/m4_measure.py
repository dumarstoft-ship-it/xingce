from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L')
a = np.array(im)
h, w = a.shape
# find left axis vertical line: column with many dark pixels between x=100 and 160
for x in range(100, 170):
    col = a[40:400, x]
    n = (col < 128).sum()
    if n > 200:
        print("axis col", x, n)
# find tick marks: rows where pixels just left of axis are dark
