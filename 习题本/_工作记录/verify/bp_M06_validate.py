import json, re, collections
ROOT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
bp = json.load(open(f'{ROOT}/blueprints/M06.json', encoding='utf-8'))
task = json.load(open(f'{ROOT}/tasks_in/M06.json', encoding='utf-8'))
given = [q['id'] for q in task['real']]
assert bp['module'] == 'M06'
assert [d['day'] for d in bp['days']] == task['days'] == [5, 19, 33, 41], [d['day'] for d in bp['days']]
seen = collections.Counter()
tags = []
for d in bp['days']:
    nr = sum(len(g['real']) for g in d['groups'])
    nv = sum(v['n'] for g in d['groups'] for v in g['variants'])
    dirs = collections.Counter()
    for g in d['groups']:
        assert g['title'].strip()
        for r in g['real']: seen[r] += 1
        for v in g['variants']:
            assert set(v) == {'n', 'direction', 'seed', 'idea'}, v.keys()
            assert v['direction'] in ('巩固', '深化', '拓展') and v['n'] >= 1 and v['seed'] and len(v['idea']) > 40
            dirs[v['direction']] += v['n']
            m = re.match(r'〔(\d+-\d+-\d+)〕', v['idea']); assert m, v['idea'][:20]
            tags.append(m.group(1))
            assert m.group(1).split('-')[0] == str(d['day'])
            if re.match(r'\d{4}[A-Z]', v['seed']): assert v['seed'] in given, v['seed']
    print(f"day {d['day']:>2}: groups={len(d['groups'])} real={nr:>2} variants={nv:>2} total={nr+nv}  巩固/深化/拓展={dirs['巩固']}/{dirs['深化']}/{dirs['拓展']}")
    assert nr + nv == 45
dup = [k for k, c in seen.items() if c > 1]
missing = [i for i in given if seen[i] == 0]
unknown = [k for k in seen if k not in given]
issue_ids = [x['id'] for x in bp['issues']]
dropped = []  # 没有建议剔除的题
print('real placed:', sum(seen.values()), '/', len(given), ' dup:', dup, ' missing:', missing, ' unknown:', unknown)
assert not dup and not missing and not unknown and sum(seen.values()) == 51
need_self = sorted(q['id'] for q in task['real'] if q['needs_self_solve'])
assert sorted(x['id'] for x in bp['self_solved']) == need_self == ['2026GD-42', '2026ZJA-51', '2026ZJA-61']
assert all(x['answer'] in 'ABCD' and x['note'] for x in bp['self_solved'])
assert all(i in given for i in issue_ids) and len(set(issue_ids)) == len(issue_ids)
assert len(tags) == len(set(tags)) == 129
# 与验算脚本的键完全对应
src = open(f'{ROOT}/verify/bp_M06_ideas.py', encoding='utf-8').read()
keys = set(re.findall(r"'(\d+-\d+-\d+)':", src))
assert keys == set(tags), (set(tags) - keys, keys - set(tags))
# md 与 json 一致：md 里每个编号都出现、每个真题 id 都出现
md = open(f'{ROOT}/blueprints/M06.md', encoding='utf-8').read()
assert all(f'〔{t}〕' in md for t in tags) and all(i in md for i in given)
assert '<!--' not in md
print('self_solved:', [(x['id'], x['answer']) for x in bp['self_solved']])
print('issues:', len(bp['issues']), issue_ids)
print('ALL CHECKS PASSED')
