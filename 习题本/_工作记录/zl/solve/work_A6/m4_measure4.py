from PIL import Image
import numpy as np
def analyze(path, x0, x1, y_zero, y_top, top_val, ylo=40, yhi=None):
    im = Image.open(path).convert('L')
    a = np.array(im).astype(int)
    H, W = a.shape
    yhi = yhi or y_zero
    # find horizontal dark runs (bar tops) of length >= 40 within the plot area
    res = []
    for y in range(ylo, int(y_zero)-2):
        row = a[y, x0:x1] < 140
        # find runs
        run = 0; start = None
        for i, v in enumerate(row):
            if v:
                if run == 0: start = i
                run += 1
            else:
                if run >= 40: res.append((y, x0+start, x0+start+run-1, run))
                run = 0
        if run >= 40: res.append((y, x0+start, x0+start+run-1, run))
    scale = (y_zero - y_top)/top_val
    for y, s, e, r in res:
        print("row %d x %d-%d len %d value=%.3f" % (y, s, e, r, (y_zero - y)/scale))
print("Chart2")
analyze('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png', 133, 800, 377.4, 63.9, 3.0)
