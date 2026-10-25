"""校验 blueprints/M05.json：可读、每天真题+改编=45、真题不重不漏、字段合法。"""
import json, re, collections
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
task = json.load(open(f'{S}/tasks_in/M05.json'))
bp = json.load(open(f'{S}/blueprints/M05.json'))
ids = [q['id'] for q in task['real']]
need_self = {q['id'] for q in task['real'] if q['needs_self_solve']}
ok = True
def bad(msg):
    global ok; ok = False; print('PROBLEM', msg)

assert bp['module'] == 'M05'
days = [d['day'] for d in bp['days']]
if days != task['days']: bad(f'days {days} != {task["days"]}')
seen = collections.Counter()
dirs = collections.Counter()
for d in bp['days']:
    titles = [g['title'] for g in d['groups']]
    if len(titles) != len(set(titles)): bad(f'day {d["day"]} duplicate group titles')
    nreal = sum(len(g['real']) for g in d['groups'])
    nvar = 0
    for g in d['groups']:
        if not g['title'] or ('real' not in g) or ('variants' not in g): bad(f'day {d["day"]} malformed group')
        for r in g['real']:
            seen[r] += 1
            if r not in ids: bad(f'unknown real id {r}')
        for v in g['variants']:
            nvar += v['n']
            dirs[(d['day'], v['direction'])] += v['n']
            if v['direction'] not in ('巩固', '深化', '拓展'): bad(f'bad direction {v}')
            if not isinstance(v['n'], int) or v['n'] < 1: bad(f'bad n {v}')
            if not (v['seed'] in ids or re.fullmatch(r'考法[一二三四五六七八九十]+', v['seed'])): bad(f'bad seed {v["seed"]}')
            if len(v['idea']) < 40: bad(f'idea too short: {v["idea"]}')
    print(f'day {d["day"]}: real {nreal} + variants {nvar} = {nreal + nvar}; groups {len(d["groups"])}')
    if nreal + nvar != 45: bad(f'day {d["day"]} total {nreal + nvar}')
missing = [i for i in ids if seen[i] == 0]
dups = [i for i in ids if seen[i] > 1]
if missing: bad(f'missing real {missing}')
if dups: bad(f'duplicated real {dups}')
ss = {s['id']: s for s in bp['self_solved']}
if set(ss) != need_self: bad(f'self_solved {set(ss)} != {need_self}')
for s in bp['self_solved']:
    if s['answer'] not in 'ABCD' or not s.get('note'): bad(f'bad self_solved {s}')
for it in bp['issues']:
    if it['id'] not in ids or not it.get('problem'): bad(f'bad issue {it}')
print('directions:', dict(dirs))
print('real assigned:', sum(seen.values()), 'of', len(ids), '| issues', len(bp['issues']), '| self_solved', len(bp['self_solved']))
print('ALL OK' if ok else 'HAS PROBLEMS')
