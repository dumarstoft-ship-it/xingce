"""Estimate the text size of a crop from its ink bands (rows of text), in points at the crop's render dpi."""
import json, sys
import numpy as np
from PIL import Image

def bands(a, ink=150, min_cov=0.004):
    rows = (a < ink).mean(axis=1) > min_cov
    out = []; y = 0; h = len(rows)
    while y < h:
        if rows[y]:
            s = y
            while y < h and rows[y]: y += 1
            out.append((s, y))
        else:
            y += 1
    return out

def est_pt(path, dpi=200):
    a = np.asarray(Image.open(path).convert('L'))
    ink = a < 150
    # text-like bands: at least 12 px tall with ink in a fair share of columns (rows of dots, rules and
    # lone option letters fall below this). Lines holding fractions, superscripts or figures are taller
    # than plain text, so the smallest qualifying band is the best guess for the text size.
    bs = [e - s for s, e in bands(a) if e - s >= 12 and ink[s:e].any(axis=0).mean() >= 0.08]
    if not bs: return None
    hpx = float(min(bs))
    return hpx / (dpi / 72.0) / 0.92   # CJK ink height is ~0.92 em

if __name__ == '__main__':
    for p in sys.argv[1:]:
        js = json.load(open(p + '.json')) if __import__('os').path.exists(p + '.json') else {}
        print(p.split('/')[-1], 'est %.1f pt' % (est_pt(p) or 0), 'sidecar', js)
