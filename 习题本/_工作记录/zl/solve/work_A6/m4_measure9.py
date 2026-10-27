from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L')
a = np.array(im).astype(int)
y_zero, y_top = 377.4, 63.9
scale = (y_zero-y_top)/3.0
print("expected y for 2.35: %.1f, 2.40: %.1f" % (y_zero-2.35*scale, y_zero-2.40*scale))
for x in [575, 576, 600, 610, 620, 643, 644]:
    print(x, [a[y, x] for y in range(116, 136)])
