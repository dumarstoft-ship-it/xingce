from PIL import Image
import numpy as np
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p1.png').convert('L'))
h,w = im.shape
rows = [y for y in range(h) if (im[y,140:820] < 100).sum() > 500]
print("x axis rows:", rows)
for x in range(120,150):
    if (im[:,x] < 100).sum() > 200: print("axis col", x, np.where(im[:,x]<100)[0].min(), np.where(im[:,x]<100)[0].max())
