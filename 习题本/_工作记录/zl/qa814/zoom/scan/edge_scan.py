import re, os, sys
import numpy as np
from PIL import Image
H = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/out/zl_d8-14.html'
h = open(H).read()
toks = re.findall(r'(<span class="t">[^<]+</span>|<div class="mat-h">[^<]+</div>|<span class="no">\d+</span>|src="file://([^"]+)")', h)
items = []; st = None; mat = None; q = None
for t in toks:
    s = t[0]
    if s.startswith('<span class="t">'): st = re.sub('<[^>]+>', '', s).strip()
    elif s.startswith('<div class="mat-h">'): mat = re.sub('<[^>]+>', '', s)[:3]; q = None
    elif s.startswith('<span class="no">'): q = int(re.sub('<[^>]+>', '', s))
    else:
        f = t[1]
        kind = 'Q%d' % q if f.endswith('_q.png') else 'mat' + mat
        items.append((st, kind, f))
def bands(a, ink=200):
    rows = (a < ink).any(axis=1)
    idx = np.flatnonzero(np.diff(np.concatenate([[0], rows.astype(np.int8), [0]])))
    return [(int(s), int(e)) for s, e in zip(idx[0::2], idx[1::2])]
for st, kind, f in items:
    im = Image.open(f).convert('L'); a = np.asarray(im); hgt, w = a.shape
    b = bands(a)
    flags = []
    if not b: flags.append('EMPTY')
    else:
        if b[0][0] <= 1: flags.append(f'top-touch(h={b[0][1]-b[0][0]})')
        if b[-1][1] >= hgt - 1: flags.append(f'bottom-touch(h={b[-1][1]-b[-1][0]})')
        if len(b) >= 2 and b[-1][1] - b[-1][0] <= 16 and b[-1][0] - b[-2][1] >= 3: flags.append(f'thin-last(h={b[-1][1]-b[-1][0]},gap={b[-1][0]-b[-2][1]})')
        if len(b) >= 2 and b[0][1] - b[0][0] <= 16 and b[1][0] - b[0][1] >= 3: flags.append(f'thin-first(h={b[0][1]-b[0][0]},gap={b[1][0]-b[0][1]})')
    cols = (a < 200).any(axis=0); cx = np.flatnonzero(cols)
    if len(cx):
        if cx[0] <= 1: flags.append('left-touch')
        if cx[-1] >= w - 2: flags.append('right-touch')
    if flags: print(st, kind, os.path.basename(f), (w, hgt), ' '.join(flags))
print('total items', len(items))
