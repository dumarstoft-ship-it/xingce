"""Combine 粉笔 全站正确率 (where printed) with calibrated agent ratings into one passage ranking -> db/zl_rank.json"""
import json, glob, os
import numpy as np
from collections import defaultdict
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def load_ratings(prefix):
    out = {}
    for f in sorted(glob.glob(f'{S}/zl/rate/{prefix}*.json')):
        try: res = json.load(open(f))
        except Exception as e: print('bad', f, e); continue
        for e in res:
            out[e['mat']] = {'pred': float(np.mean([q['acc'] for q in e['q']])), 'batch': os.path.basename(f)[:-5], 'hard_points': e.get('hard_points'),
                             'q': e['q']}
    return out
def pos_adj(rs, n_mats):
    """the last passage of a paper is answered under time pressure (many guess), which pulls its 正确率 down:
    国考-style papers (国考 and 粉笔 国考 mocks) about 14 points for M4 in our data, provincial papers about 3.
    Practice sets are done in full, so most of that is added back."""
    code = rs[0]['paper']; k = rs[0]['mat_idx']
    if 'GK' in code or code.startswith('MK'):
        return {4: 10.0, 3: 1.0}.get(k, 0.0)
    return 3.0 if k == n_mats else 0.0

if __name__ == '__main__':
    raw = json.load(open(S + '/db/zl_raw.json'))
    pool = json.load(open(S + '/db/zl_pool.json'))
    by = defaultdict(list)
    for r in raw: by[r['mat']].append(r)
    pil = load_ratings('pilot'); full = load_ratings('full')
    # calibration on the pilot: actual = a + b * pred
    xs, ys = [], []
    for m, e in pil.items():
        acc = [r['acc'] for r in by[m]]
        if None not in acc: xs.append(e['pred']); ys.append(np.mean(acc))
    b, a = np.polyfit(xs, ys, 1)
    print(f'calibration actual = {a:.1f} + {b:.2f} * pred  (n={len(xs)})')
    # batch offsets in the full run (quasi-random assignment): partial pooling toward the global mean
    bm = defaultdict(list)
    for m, e in full.items(): bm[e['batch']].append(e['pred'])
    g = np.mean([e['pred'] for e in full.values()]) if full else 0
    off = {k: 0.5 * (np.mean(v) - g) for k, v in bm.items()}
    print('batch offsets', {k: round(v, 1) for k, v in sorted(off.items())})
    nm = defaultdict(set)
    for r in raw: nm[r['paper']].add(r['mat_idx'])
    rank = []
    for m in pool:
        acc = [r['acc'] for r in by[m]]
        adj = pos_adj(by[m], len(nm[by[m][0]['paper']]))
        if None not in acc:
            rank.append({'mat': m, 'score': float(np.mean(acc)) + adj, 'src': 'acc', 'pos_adj': adj})
        elif m in full:
            e = full[m]
            rank.append({'mat': m, 'score': float(a + b * (e['pred'] - off[e['batch']])) + adj, 'src': 'rated', 'raw_pred': e['pred'], 'pos_adj': adj, 'hard_points': e['hard_points']})
        else:
            rank.append({'mat': m, 'score': None, 'src': 'missing'})
    rank = sorted([e for e in rank if e['score'] is not None], key=lambda e: e['score']) + [e for e in rank if e['score'] is None]
    json.dump(rank, open(S + '/db/zl_rank.json', 'w'), ensure_ascii=False, indent=0)
    for e in rank[:60]: print(round(e['score'], 1) if e['score'] else None, e['mat'], e['src'], (e.get('hard_points') or '')[:70])
    print('missing', [e['mat'] for e in rank if e['score'] is None][:40])
