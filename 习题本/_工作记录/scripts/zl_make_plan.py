"""Turn the difficulty ranking into sets of 4 passages and a day plan (hardest passages only).
Usage: zl_make_plan.py <first_day> <last_day> [first_set_no]
Reads db/zl_rank.json (hardest first); keeps passages whose 5 answers and 解析 crops are all present."""
import json, sys, os
from collections import defaultdict
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def complete(rs, fix):
    for r in rs:
        if not (r['answer_official'] or (fix.get(r['id']) or {}).get('answer')): return False
        if (fix.get(r['id']) or {}).get('check'): return False
        if not os.path.exists(f"{S}/crops/zl/{r['id']}_j.png") and not (fix.get(r['id']) or {}).get('jiexi'): return False
    return True
def make(d0, d1, first_set=1, per_day=2, per_set=4, used=(), selfsolve=('MK',), skip_papers=('2026GK', '2026ZJA')):
    raw = json.load(open(S + '/db/zl_raw.json'))
    fix = json.load(open(S + '/db/zl_fixes.json')) if os.path.exists(S + '/db/zl_fixes.json') else {}
    by = defaultdict(list)
    for r in raw: by[r['mat']].append(r)
    # mock papers have no official key: their passages are solved twice independently (zl/solve), so they need no answers yet
    rank = [e for e in json.load(open(S + '/db/zl_rank.json')) if e['score'] is not None and e['mat'] not in set(used)
            and e['mat'].split('-M')[0] not in skip_papers and (e['mat'].startswith(selfsolve) or complete(by[e['mat']], fix))]
    n_sets = (d1 - d0 + 1) * per_day
    pick = rank[:n_sets * per_set]
    sets = [[] for _ in range(n_sets)]
    for k, e in enumerate(pick):  # snake draft: every set gets a similar mix of the very hardest and the merely hard
        rnd, pos = divmod(k, n_sets)
        sets[pos if rnd % 2 == 0 else n_sets - 1 - pos].append(e)
    paper = lambda e: e['mat'].split('-M')[0]
    for _ in range(3):  # spread passages of one paper over different sets: swap within the same draft round
        for i in range(n_sets):
            for j in range(per_set):
                if sum(paper(x) == paper(sets[i][j]) for x in sets[i]) < 2: continue
                for i2 in range(n_sets):
                    if i2 == i: continue
                    a, b = sets[i][j], sets[i2][j]
                    if paper(b) not in [paper(x) for x in sets[i] if x is not a] and paper(a) not in [paper(x) for x in sets[i2] if x is not b]:
                        sets[i][j], sets[i2][j] = b, a; break
    out = []
    for i, ss in enumerate(sets):
        ss = sorted(ss, key=lambda e: e['score'], reverse=True)  # within a set: the merely hard first, the hardest last
        out.append({'set': first_set + i, 'day': d0 + i // per_day, 'mats': [e['mat'] for e in ss], 'scores': [round(e['score'], 1) for e in ss],
                    'src': [e['src'] for e in ss]})
    return out
if __name__ == '__main__':
    d0, d1 = int(sys.argv[1]), int(sys.argv[2]); fs = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    old = json.load(open(S + '/db/zl_sets.json')) if os.path.exists(S + '/db/zl_sets.json') else []
    keep = [s for s in old if s['day'] < d0]                       # sets of earlier days stay as delivered
    sets = make(d0, d1, fs, used=[m for s in keep for m in s['mats']])
    sets = keep + sets
    json.dump(sets, open(S + '/db/zl_sets.json', 'w'), ensure_ascii=False, indent=1)
    plan = defaultdict(list)
    for s in sets: plan[str(s['day'])].append({'set': s['set'], 'mats': s['mats']})
    json.dump(plan, open(S + '/db/zl_plan.json', 'w'), ensure_ascii=False, indent=1)
    sets = [s for s in sets if s['day'] >= d0]
    for s in sets: print(s['set'], s['day'], s['mats'], s['scores'], round(sum(s['scores']) / len(s['scores']), 1))
