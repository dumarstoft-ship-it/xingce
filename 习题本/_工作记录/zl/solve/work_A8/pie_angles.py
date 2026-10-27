import sys, json
import numpy as np
from PIL import Image

path = sys.argv[1]
pies = json.loads(sys.argv[2])  # list of [label, cx, cy, r]
im = np.array(Image.open(path).convert('L')).astype(float)
H, W = im.shape

def sample(x, y):
    x0 = int(np.floor(x)); y0 = int(np.floor(y))
    dx = x - x0; dy = y - y0
    v = (im[y0, x0] * (1 - dx) * (1 - dy) + im[y0, x0 + 1] * dx * (1 - dy)
         + im[y0 + 1, x0] * (1 - dx) * dy + im[y0 + 1, x0 + 1] * dx * dy)
    return v

for lab, cx, cy, R in pies:
    angs = np.arange(0, 360, 0.1)
    score = []
    for a in angs:
        t = np.radians(a)
        rs = np.linspace(0.25 * R, 0.9 * R, 120)
        vals = [sample(cx + r * np.sin(t), cy - r * np.cos(t)) for r in rs]
        vals = np.array(vals)
        score.append((vals < 140).mean())
    score = np.array(score)
    # find peaks above 0.85
    peaks = []
    n = len(angs)
    i = 0
    while i < n:
        if score[i] >= 0.8:
            j = i
            while j + 1 < n and score[j + 1] >= 0.8:
                j += 1
            seg = score[i:j + 1]
            k = i + int(np.argmax(seg))
            # center of mass of the run
            peaks.append((round(angs[i], 1), round(angs[j], 1), round(float((angs[i] + angs[j]) / 2), 2), round(float(score[k]), 3)))
            i = j + 1
        else:
            i += 1
    print(lab, 'center', cx, cy, 'R', R)
    for p in peaks:
        print('   run', p)
    # region classification at mid radius: mean intensity per 5 deg
    prof = []
    for a in range(0, 360, 5):
        t = np.radians(a + 2.5)
        pts = []
        for r in np.linspace(0.3 * R, 0.85 * R, 60):
            pts.append(sample(cx + r * np.sin(t), cy - r * np.cos(t)))
        pts = np.array(pts)
        prof.append((a, int(pts.mean()), round(float((pts < 140).mean()), 2)))
    print('   profile(angle, mean, darkfrac):', prof)
