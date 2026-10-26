import json, glob, os, sys
import numpy as np
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
pl = json.load(open(S + '/zl/pilot.json'))
raw = json.load(open(S + '/db/zl_raw.json'))
by = {}
for r in raw: by.setdefault(r['mat'], []).append(r)
def rank(a): return np.argsort(np.argsort(a)).astype(float)
def spear(a, b): return float(np.corrcoef(rank(np.array(a)), rank(np.array(b)))[0, 1])
pm, am, pq, aq = [], [], [], []
rows = []
for f in sorted(glob.glob(S + '/zl/rate/pilot*.json')):
    if f.endswith('.prompt.txt'): continue
    try: res = json.load(open(f))
    except Exception as e: print('bad', f, e); continue
    for e in res:
        m = e['mat']; rs = sorted(by[m], key=lambda r: r['pos'])
        acc = [r['acc'] for r in rs]
        if None in acc: continue
        pa = [q['acc'] for q in e['q']]
        pm.append(float(np.mean(pa))); am.append(float(np.mean(acc)))
        pq += pa; aq += acc
        rows.append((m, round(np.mean(acc), 1), round(np.mean(pa), 1), os.path.basename(f)))
print('materials', len(pm), 'spearman', round(spear(pm, am), 3), 'pearson', round(float(np.corrcoef(pm, am)[0, 1]), 3))
print('questions', len(pq), 'spearman', round(spear(pq, aq), 3))
for r in sorted(rows, key=lambda r: r[1]): print(*r)
