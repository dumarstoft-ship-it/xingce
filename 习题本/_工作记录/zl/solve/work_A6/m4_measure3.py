from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L')
a = np.array(im).astype(int)
for y in range(40, 400):
    seg = a[y, 133:140]
    if (seg < 180).sum() >= 3:
        print("inner tick y", y, seg.tolist())
# label rows on left: find dark pixel rows in x=100..125 (tick label text)
rows = [y for y in range(40,400) if (a[y,95:126] < 128).sum() > 0]
# group
groups = []
for y in rows:
    if groups and y - groups[-1][-1] <= 1: groups[-1].append(y)
    else: groups.append([y])
for g in groups: print("label rows", g[0], g[-1], (g[0]+g[-1])/2)
# vertical axis top
col = a[:, 131]
H = a.shape[0]; ys = [y for y in range(H) if col[y] < 128]
print("axis from", min(ys), "to", max(ys))
