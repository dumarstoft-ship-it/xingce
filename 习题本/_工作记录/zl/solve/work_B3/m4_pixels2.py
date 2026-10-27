from PIL import Image
import numpy as np
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L'))
h, w = im.shape
# ticks on left axis: dark pixels just left of axis col 131 (x=125..130)
ticks = [y for y in range(h) if (im[y,124:130] < 120).sum() >= 4]
print("left ticks rows:", ticks)
# vertical axis top
col = np.where(im[:,131] < 100)[0]
print("axis col 131 dark range:", col.min(), col.max())
# bars: find vertical bar edges along row 370
row = im[370, 131:820]
dark = np.where(row < 120)[0] + 131
print("dark x at row 370:", dark)
