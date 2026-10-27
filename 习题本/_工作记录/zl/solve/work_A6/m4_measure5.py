from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L')
a = np.array(im).astype(int)
y_zero, y_top = 377.4, 63.9
scale = (y_zero-y_top)/3.0
for x in range(570, 655):
    col = a[100:377, x]
    dark = [100+i for i, v in enumerate(col) if v < 140]
    if len(dark) > 150:
        # vertical edge: find contiguous run ending at axis
        ys = sorted(dark)
        # topmost of the contiguous run that reaches near axis
        run_top = ys[-1]
        for yy in reversed(ys):
            if yy == run_top or yy == run_top - 1:
                run_top = yy
            else:
                break
        print("x", x, "count", len(dark), "edge top", run_top, "value %.3f" % ((y_zero-run_top)/scale))
