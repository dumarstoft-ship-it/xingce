# -*- coding: utf-8 -*-
"""Independent check of the delivered blueprints/L03.json (reads only the delivered file + tasks_in)."""
import json, re, sys
SP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
task = json.load(open(SP + '/tasks_in/L03.json', encoding='utf-8'))
bp = json.load(open(SP + '/blueprints/L03.json', encoding='utf-8'))
ids = [r['id'] for r in task['real']]
errs = []
if bp.get('module') != 'L03':
    errs.append('module')
if [d['day'] for d in bp['days']] != task['days']:
    errs.append('days %s' % [d['day'] for d in bp['days']])
seen = []
codes = set()
for d in bp['days']:
    nr = sum(len(g['real']) for g in d['groups'])
    nv = sum(v['n'] for g in d['groups'] for v in g['variants'])
    print('day %2d: real %2d + variants %2d = %d' % (d['day'], nr, nv, nr + nv))
    if nr + nv != 45:
        errs.append('day %d sum %d' % (d['day'], nr + nv))
    for g in d['groups']:
        if not g.get('title'):
            errs.append('empty title day %d' % d['day'])
        seen += g['real']
        for v in g['variants']:
            if set(v) != {'n', 'direction', 'seed', 'idea'}:
                errs.append('variant keys %s' % sorted(v))
            if v['direction'] not in ('巩固', '深化', '拓展'):
                errs.append('direction %s' % v['direction'])
            if not (v['seed'] in ids or re.fullmatch(r'考法[一二三四五六七八九十]+', v['seed'])):
                errs.append('seed %s' % v['seed'])
            if not isinstance(v['n'], int) or v['n'] < 1:
                errs.append('n %s' % v['n'])
            m = re.match(r'〔(\d+-\d+-\d+)〕', v['idea'])
            if not m or m.group(1) in codes:
                errs.append('code %s' % v['idea'][:20])
            else:
                codes.add(m.group(1))
            for key in ('【设问】', '【答案位置】'):
                if key not in v['idea'] and not (key == '【设问】' and '【第 1 问】' in v['idea']):
                    errs.append('%s missing in %s' % (key, m.group(1) if m else '?'))
dup = sorted(set(x for x in seen if seen.count(x) > 1))
missing = sorted(set(ids) - set(seen))
extra = sorted(set(seen) - set(ids))
excluded = sorted(i['id'] for i in bp['issues'] if '剔除（未排入' in i['problem'])
print('real placed: %d unique of %d; duplicates %s; extra %s' % (len(set(seen)), len(ids), dup, extra))
print('not placed: %s; excluded via issues: %s' % (missing, excluded))
if dup or extra or missing != excluded:
    errs.append('real coverage')
need = sorted(r['id'] for r in task['real'] if r['needs_self_solve'])
got = sorted(s['id'] for s in bp['self_solved'])
print('self_solved: %s' % ', '.join('%s=%s' % (s['id'], s['answer']) for s in bp['self_solved']))
if need != got or any(s['answer'] not in 'ABCD' or len(s['answer']) != 1 for s in bp['self_solved']):
    errs.append('self_solved')
print('issues: %d' % len(bp['issues']))
print('variants: %d entries, %d questions' % (sum(len(g['variants']) for d in bp['days'] for g in d['groups']),
                                             sum(v['n'] for d in bp['days'] for g in d['groups'] for v in g['variants'])))
print('ERRORS:', errs if errs else 'none')
sys.exit(1 if errs else 0)
