"""Create generation prompt files for given days/parts once blueprints exist. Prints a manifest."""
import json, os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prompts import gen_prompt, split_groups, self_solve_ids, S

def make(day, part, per_agent=16):
    sched = json.load(open(S + '/db/schedule.json'))['schedule'][day - 1]
    module = sched[part]
    bp = 'C' if part == 'zh' else module
    if not os.path.exists(f'{S}/blueprints/{bp}.json'):
        return None
    plan = json.load(open(f'{S}/blueprints/{bp}.json'))
    dp = next(d for d in plan['days'] if d['day'] == day)
    nvar = sum(v['n'] for g in dp['groups'] for v in g.get('variants', []))
    k = max(1, math.ceil(nvar / per_agent))
    bins = split_groups(day, part, module, k)
    out = []
    for i, b in enumerate(bins, 1):
        prefix = f'D{day:02d}-{part}-{i}'
        of = f'{S}/gen/D{day:02d}_{part}_{i}.json'
        real_ids = [r for t, n, real in b for r in real]
        ss = self_solve_ids(bp, real_ids)
        txt = gen_prompt(day, part, module, [t for t, n, real in b], of, prefix, ss)
        pf = f'{S}/prompts/gen_D{day:02d}_{part}_{i}.txt'
        open(pf, 'w').write(txt)
        out.append({'prompt': pf, 'out': of, 'n': sum(n for t, n, real in b), 'groups': len(b), 'self_solve': ss})
    return out

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        d, p = arg.split(':')
        r = make(int(d), p)
        print(arg, json.dumps(r, ensure_ascii=False) if r else 'NO BLUEPRINT')
