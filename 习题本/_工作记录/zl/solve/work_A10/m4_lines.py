from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2705X-Z124_q.png').convert('L')
a = np.array(im).astype(float)
print(a.shape)
# options are stacked vertically; examine x columns at 115, 207, 302, 398 for each band
bands = {"A": (70, 200), "B": (240, 370), "C": (410, 540), "D": (590, 676)}
for k, (y0, y1) in bands.items():
    ys = []
    for x in (116, 207, 302, 396):
        col = a[y0:y1, x]
        idx = np.where(col < 128)[0]
        ys.append((y0 + idx.mean()) if len(idx) else None)
    if None in ys: print(k, ys); continue
    d = [round(ys[i+1]-ys[i], 1) for i in range(3)]
    print(k, [round(y, 1) for y in ys], "dy(+ means down)", d)
