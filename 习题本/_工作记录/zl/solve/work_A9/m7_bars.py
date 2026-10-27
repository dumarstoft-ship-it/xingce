from PIL import Image
import numpy as np
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2702X-Z125_q.png').convert('L')
a = np.array(im)
H, W = a.shape
# restrict to chart region (x 80..620, y 100..390)
reg = a[100:390, 80:620]
dark = reg < 80
cols = dark.sum(axis=0)
# find bar column runs: columns with many dark pixels
runs = []
inrun = False
for x, c in enumerate(cols):
    if c > 50 and not inrun:
        inrun = True; s = x
    elif c <= 50 and inrun:
        inrun = False; runs.append((s, x - 1))
if inrun: runs.append((s, len(cols) - 1))
print("bar column runs (x offset 80):", [(s + 80, e + 80) for s, e in runs])
# axis baseline: row with many dark pixels across
rows = dark.sum(axis=1)
base = max(range(len(rows)), key=lambda r: rows[r])
print("baseline row", base + 100, "dark count", rows[base])
hs = []
for s, e in runs:
    mid = (s + e) // 2
    col = dark[:, mid]
    top = next(i for i in range(len(col)) if col[i])
    # bottom: last dark pixel above baseline region
    bot = base
    hs.append(bot - top)
    print("bar x", s + 80, e + 80, "top", top + 100, "height", bot - top)
print("ratios", [h / hs[0] for h in hs])
