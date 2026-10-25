"""Validate blueprints/M01.json independently: readable, 45 per day, real ids exactly once, fields legal."""
import json, re, collections
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
task = json.load(open(f'{S}/tasks_in/M01.json'))
bp = json.load(open(f'{S}/blueprints/M01.json'))
ids = [q['id'] for q in task['real']]
need_self = {q['id'] for q in task['real'] if q['needs_self_solve']}
ok = True
def bad(m):
    global ok; ok = False; print('PROBLEM', m)
assert bp['module'] == 'M01'
if [d['day'] for d in bp['days']] != task['days']: bad('days mismatch')
seen = collections.Counter(); dirs = collections.Counter(); vids = set()
for d in bp['days']:
    titles = [g['title'] for g in d['groups']]
    if len(titles) != len(set(titles)): bad(f'day {d["day"]} duplicate titles')
    nreal = sum(len(g['real']) for g in d['groups']); nvar = 0
    for g in d['groups']:
        for r in g['real']:
            seen[r] += 1
            if r not in ids: bad(f'unknown real {r}')
        for v in g['variants']:
            nvar += v['n']; dirs[(d['day'], v['direction'])] += v['n']
            if v['direction'] not in ('巩固', '深化', '拓展'): bad(f'direction {v}')
            if not isinstance(v['n'], int) or v['n'] < 1: bad(f'n {v}')
            if not (v['seed'] in ids or re.fullmatch(r'考法[一二三四五六七八九十]+', v['seed'])): bad(f'seed {v["seed"]}')
            m = re.match(r'〔(\d+-\d+-\d+)〕', v['idea'])
            if not m: bad('idea without id'); continue
            if m.group(1) in vids: bad('dup vid ' + m.group(1))
            vids.add(m.group(1))
            for key in ('题面：', '选项：', '答案：', '解法：', '干扰项：', '难度', '参考用时'):
                if key not in v['idea']: bad(f'idea {m.group(1)} lacks {key}')
    print(f'day {d["day"]}: real {nreal} + variants {nvar} = {nreal + nvar}; groups {len(d["groups"])}')
    if nreal + nvar != 45: bad(f'day {d["day"]} total')
miss = [i for i in ids if seen[i] == 0]; dup = [i for i in ids if seen[i] > 1]
if miss: bad(f'missing {miss}')
if dup: bad(f'dup {dup}')
ss = {s['id']: s for s in bp['self_solved']}
if set(ss) != need_self: bad('self_solved set')
for s in bp['self_solved']:
    if s['answer'] not in 'ABCD' or not s.get('note'): bad(f'self_solved {s}')
for it in bp['issues']:
    if it['id'] not in ids or not it.get('problem'): bad(f'issue {it}')
print('directions:', dict(dirs))
print('real assigned', sum(seen.values()), 'of', len(ids), '| variants', len(vids), '| issues', len(bp['issues']), '| self_solved', len(bp['self_solved']))
print('ALL OK' if ok else 'HAS PROBLEMS')
