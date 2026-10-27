# refine: classify each angle by pixel mix along radial segment; hatched = many dark+light alternations
import numpy as np, math
from PIL import Image
from collections import Counter
path = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2706X-Z115_q.png'
a = np.array(Image.open(path).convert('L')).astype(int)
centers = {'A': (199.0, 211.0), 'B': (198.5, 434.0), 'C': (198.5, 653.0), 'D': (199.5, 876.0)}
R = 99.0
for lab, (cx, cy) in centers.items():
    cls = []
    for k in range(3600):
        th = math.radians(k / 10.0)
        vals = np.array([a[int(round(cy - rr * math.cos(th))), int(round(cx + rr * math.sin(th)))]
                         for rr in np.linspace(0.3 * R, 0.85 * R, 60)])
        dark = (vals < 90).mean(); light = (vals > 200).mean(); mid = ((vals >= 90) & (vals <= 200)).mean()
        if mid > 0.7: c = 'G'
        elif light > 0.9: c = 'W'
        elif dark > 0.9: c = 'K'
        elif dark > 0.05 and light > 0.05: c = 'H'
        else: c = '?'
        cls.append(c)
    cnt = Counter(cls); tot = sum(cnt.values())
    print(lab, {k: round(v / tot * 100, 1) for k, v in sorted(cnt.items())})
