"""Font size of a crop from the height of its digit-like glyphs (column runs inside each text band whose
width/height looks like a single digit). Formula crops (fractions, radicals) fool the line-band estimate."""
import numpy as np
from PIL import Image

def digit_height(path, ink=140):
    a = np.asarray(Image.open(path).convert('L')) < ink
    rows = a.any(axis=1)
    hs = []
    y = 0; H = len(rows)
    while y < H:
        if not rows[y]: y += 1; continue
        y0 = y
        while y < H and rows[y]: y += 1
        band = a[y0:y]
        cols = band.any(axis=0); x = 0; W = len(cols)
        while x < W:
            if not cols[x]: x += 1; continue
            x0 = x
            while x < W and cols[x]: x += 1
            sub = band[:, x0:x]; r = np.where(sub.any(axis=1))[0]
            h = r[-1] - r[0] + 1; w = x - x0
            if 10 <= h <= 90 and 0.35 <= w / h <= 0.8: hs.append(h)
    if len(hs) < 3: return None
    hs.sort()
    return hs[len(hs) // 2]

def font_pt(path, dpi=200):
    h = digit_height(path)
    return None if h is None else h / 0.72 * 72 / dpi  # digit height is about 0.72 em
