"""Deduped, complete passage pool for 资料 selection -> db/zl_pool.json"""
import json, os
from collections import defaultdict
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
RESERVED = {'2024GD', '2025GD', '2026GD'}   # kept back for full mock exams
BROKEN = {'2016GK', '2026CQ'}                # 2016GK: passage grouping off by one; 2026CQ: answers printed under the questions
def build(extra_raw=()):
    raw = json.load(open(S + '/db/zl_raw.json')) + list(extra_raw)
    dups = json.load(open(S + '/db/zl_dups.json'))
    inc = set(json.load(open(S + '/db/zl_incomplete.json')))
    by = defaultdict(list)
    for r in raw: by[r['mat']].append(r)
    pool, skip = [], set()
    order = sorted(by, key=lambda m: (0 if 'GK-' in m and 'GKD' not in m and 'GKX' not in m else 1, m))
    for m in order:
        rs = by[m]
        if m in skip or m in inc or rs[0]['paper'] in RESERVED | BROKEN: continue
        for d, ov in dups.get(m, []): skip.add(d)
        pool.append(m)
    return pool
if __name__ == '__main__':
    pool = build()
    json.dump(pool, open(S + '/db/zl_pool.json', 'w'))
    print(len(pool), [m for m in pool if m.startswith('2016GKD')])
