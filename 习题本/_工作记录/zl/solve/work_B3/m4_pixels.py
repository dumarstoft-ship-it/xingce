from PIL import Image
import numpy as np
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L'))
h, w = im.shape
# find axis: long dark horizontal line rows
rows = [(y, (im[y,130:800] < 100).sum()) for y in range(h)]
rows = [r for r in rows if r[1] > 500]
print("long horizontal dark rows:", rows[:10])
# tick marks on left axis: find columns near x=130
# find dark pixels in column around left axis
for x in range(120, 140):
    col = (im[:, x] < 100).sum()
    if col > 200: print("vertical axis col", x, col)
