import math
from PIL import Image
import numpy as np

p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2736F-Z130_q.png'
im = np.array(Image.open(p).convert('L')).astype(float)

def bil(x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    dx, dy = x - x0, y - y0
    return (im[y0, x0] * (1 - dx) * (1 - dy) + im[y0, x0 + 1] * dx * (1 - dy)
            + im[y0 + 1, x0] * (1 - dx) * dy + im[y0 + 1, x0 + 1] * dx * dy)

def profile(cx, cy, R, N=14400):
    out = np.empty(N)
    for i in range(N):
        a = 2 * math.pi * i / N
        out[i] = bil(cx + R * math.sin(a), cy - R * math.cos(a))
    return out

def darkness_centroid(prof, a0, a1, N=14400):
    # centroid (in degrees) of darkness (255-v) within [a0,a1]
    i0, i1 = int(a0 / 360 * N), int(a1 / 360 * N)
    idx = np.arange(i0, i1)
    w = 255 - prof[idx % N]
    w = np.clip(w - 20, 0, None)
    return (idx * w).sum() / w.sum() * 360 / N

# Pie D: lines of the sliver are isolated (white on both sides) -> measure line centers
for name, (cx0, cy0, r) in {'A': (239.0, 236.0, 126.0), 'D': (239.0, 1123.5, 126.25)}.items():
    best = None
    for dx in np.arange(-2, 2.01, 0.25):
        for dy in np.arange(-2, 2.01, 0.25):
            cx, cy = cx0 + dx, cy0 + dy
            angs = []
            for f in (0.45, 0.6, 0.75, 0.9):
                prof = profile(cx, cy, f * r, N=7200)
                # find 12 o'clock line: white->dark transition near 358-360: use edge where value crosses 128
                # use left edge of the 12 o'clock line
                seg = prof[int(355 / 360 * 7200):]
                k = np.argmax(seg < 128)
                angs.append(355 + k / 20.0)
            spread = max(angs) - min(angs)
            if best is None or spread < best[0]:
                best = (spread, cx, cy, angs)
    print(name, 'best center for 12-oclock consistency', best)
