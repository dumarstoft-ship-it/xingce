# -*- coding: utf-8 -*-
# 独立校验 blueprints/M08.json：可读、每天 真题+改编=45、真题不重不漏（剔除题须在 issues 中）、字段合法、编号连续。
import json, re, collections, sys
SCR = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
bp = json.load(open(SCR + '/blueprints/M08.json'))
task = json.load(open(SCR + '/tasks_in/M08.json'))
ids = [q['id'] for q in task['real']]
need_self = {q['id'] for q in task['real'] if q['needs_self_solve']}
pending = {q['id'] for q in task['real'] if q['answer_pending_ocr']}
problems = []
def bad(msg): problems.append(msg)

if bp.get('module') != 'M08': bad('module 不是 M08')
days = [d['day'] for d in bp['days']]
if days != task['days']: bad(f'天数不符 {days} vs {task["days"]}')

placed = []
for d in bp['days']:
    tot = 0
    for gi, g in enumerate(d['groups'], 1):
        if not g.get('title'): bad(f"第{d['day']}天组{gi}缺标题")
        for i in g['real']:
            if i not in ids: bad(f'{i} 不在本模块真题清单')
        placed += g['real']; tot += len(g['real'])
        for si, v in enumerate(g['variants'], 1):
            if set(v) != {'n', 'direction', 'seed', 'idea'}: bad(f'字段不符 {v.keys()}')
            if v['direction'] not in ('巩固', '深化', '拓展'): bad(f"方向非法 {v['direction']}")
            if not (v['seed'] in ids or re.fullmatch(r'考法[一二三四五六七八九十]+', v['seed'])): bad(f"种子非法 {v['seed']}")
            if not isinstance(v['n'], int) or v['n'] < 1: bad('n 非法')
            if not v['idea'].startswith(f"〔{d['day']}-{gi}-{si}〕"): bad(f"编号不连续 {v['idea'][:12]}")
            if len(v['idea']) < 120: bad(f"idea 过短 {v['idea'][:20]}")
            tot += v['n']
    if tot != 45: bad(f"第{d['day']}天合计 {tot} ≠ 45")
    print(f"第{d['day']}天：真题 {sum(len(g['real']) for g in d['groups'])} + 改编 {sum(v['n'] for g in d['groups'] for v in g['variants'])} = {tot}")

dup = [k for k, c in collections.Counter(placed).items() if c > 1]
if dup: bad(f'真题重复 {dup}')
missing = set(ids) - set(placed)
issue_ids = {i['id'] for i in bp['issues']}
excluded = set(bp.get('excluded', []))
for m in missing:
    if m not in issue_ids or m not in excluded: bad(f'{m} 未排入且未在 issues 中建议剔除')
if excluded & set(placed): bad(f'剔除题仍被排入 {excluded & set(placed)}')
ss = {s['id']: s for s in bp['self_solved']}
if set(ss) != need_self: bad(f'自解题不符 {set(ss) ^ need_self}')
for s in bp['self_solved']:
    if s['answer'] not in 'ABCD' or len(s['answer']) != 1: bad(f"自解答案非法 {s}")
if set(ss) & pending: bad('把待识别题写进了 self_solved')
first_day = bp['days'][0]
if pending & {i for g in first_day['groups'] for i in g['real']}: bad('第一天放了待识别答案的题')
for i in bp['issues']:
    if not i.get('id') or not i.get('problem'): bad(f'issue 缺字段 {i}')

print('真题', len(ids), '道；排入', len(placed), '道；建议剔除', sorted(missing))
print('自解', sorted(ss), '；问题清单', len(bp['issues']), '条')
print('改编合计', sum(v['n'] for d in bp['days'] for g in d['groups'] for v in g['variants']))
if problems:
    print('PROBLEM:'); [print(' -', p) for p in problems]; sys.exit(1)
print('校验通过')
