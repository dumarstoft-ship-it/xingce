"""Flag crops whose first or last ink band is much thinner than a text line (a line cut in half at the edge)."""
import glob, json, sys, os
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from est_font import bands

def check(path):
    a = np.asarray(Image.open(path).convert('L')); ink = a < 150
    bs = [(s, e) for s, e in bands(a) if (e - s) >= 3]
    if len(bs) < 2: return None
    hs = sorted(e - s for s, e in bs if e - s >= 12 and ink[s:e].any(axis=0).mean() >= 0.08)
    if not hs: return None
    line = hs[len(hs) // 4]
    (s0, e0), (s1, e1) = bs[0], bs[-1]
    cov0 = ink[s0:e0].any(axis=0).mean(); cov1 = ink[s1:e1].any(axis=0).mean()
    out = []
    if e0 - s0 < 0.55 * line and cov0 > 0.15: out.append(f'top band {e0-s0}px vs line {line}px')
    if e1 - s1 < 0.55 * line and cov1 > 0.15: out.append(f'bottom band {e1-s1}px vs line {line}px')
    return out

if __name__ == '__main__':
    ids = None
    if len(sys.argv) > 1: ids = set(json.load(open(sys.argv[1])))
    n = 0
    for p in sorted(glob.glob('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/real2/*_[qj].png')):
        i = os.path.basename(p)[:-6]
        if ids is not None and i not in ids: continue
        r = check(p)
        if r: print(os.path.basename(p), '; '.join(r)); n += 1
    print('flagged', n)
