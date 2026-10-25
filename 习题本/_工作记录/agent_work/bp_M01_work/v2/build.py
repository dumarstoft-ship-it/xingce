# -*- coding: utf-8 -*-
"""Build blueprints/M01.json and section 5 of blueprints/M01.md from bp_data.py, with consistency checks."""
import json, re, sys, collections, os
sys.path.insert(0, os.path.dirname(__file__))
from bp_data import DAYS, KAOFA, REAL_NOTE, SELF_SOLVED, ISSUES

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
task = json.load(open(S + '/tasks_in/M01.json'))
REAL = {r['id']: r for r in task['real']}
CN = '零一二三四五六七八九十'

def kname(k):
    return KAOFA[k]

errors = []
seen_real = collections.Counter()
seen_vid = set()
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups'])
    nv = sum(len(g['variants']) for g in d['groups'])
    if nr + nv != 45:
        errors.append(f"day {d['day']}: {nr}+{nv}!=45")
    ks = [g['k'] for g in d['groups']]
    if ks != sorted(ks) or len(set(ks)) != len(ks):
        errors.append(f"day {d['day']}: group order {ks}")
    for g in d['groups']:
        for r in g['real']:
            seen_real[r] += 1
            if r not in REAL: errors.append(f'unknown real {r}')
            if r not in REAL_NOTE: errors.append(f'no note {r}')
        diffs = [REAL[r]['difficulty'] for r in g['real']]
        if diffs != sorted(diffs):
            errors.append(f"day {d['day']} k{g['k']}: real not easy->hard {diffs}")
        for vid, dirn, seed, idea in g['variants']:
            dd, kk, ii = vid.split('-')
            if int(dd) != d['day'] or int(kk) != g['k']: errors.append(f'bad id {vid}')
            if vid in seen_vid: errors.append(f'dup id {vid}')
            seen_vid.add(vid)
            if dirn not in ('巩固', '深化', '拓展'): errors.append(f'bad dir {vid}')
            if not (seed in REAL or re.fullmatch(r'考法[一二三四五六七八九十]+', seed)): errors.append(f'bad seed {vid} {seed}')
            if seed in REAL and seed not in sum([g2['real'] for d2 in DAYS for g2 in d2['groups']], []): errors.append(f'seed not scheduled {vid}')
            for bad in ('赋值法', '十字交叉法', '设而不求法', '不变量法'):
                stem = idea.split('题面：', 1)[1].split('选项：', 1)[0] if '题面：' in idea else ''
                if bad in stem: errors.append(f'method hint in stem {vid}: {bad}')
            if '题面：' not in idea or '答案' not in idea or '难度' not in idea: errors.append(f'idea incomplete {vid}')
missing = set(REAL) - set(seen_real)
dups = [r for r, c in seen_real.items() if c > 1]
if missing: errors.append(f'missing real {sorted(missing)}')
if dups: errors.append(f'duplicated real {dups}')
# cross-check with numeric verification ids
vsrc = open(os.path.join(os.path.dirname(__file__), 'verify_variants.py'), encoding='utf-8').read()
vids = set(re.findall(r"check\('([0-9]+-[0-9]+-[0-9]+)'", vsrc))
if vids != seen_vid:
    errors.append(f'verify ids mismatch: only-in-plan={sorted(seen_vid - vids)} only-in-verify={sorted(vids - seen_vid)}')
if errors:
    print('ERRORS:'); [print(' ', e) for e in errors]; sys.exit(1)

# ---------- JSON ----------
out = {'module': 'M01', 'days': [], 'self_solved': SELF_SOLVED, 'issues': ISSUES}
for d in DAYS:
    dj = {'day': d['day'], 'groups': []}
    for g in d['groups']:
        dj['groups'].append({
            'title': kname(g['k']),
            'real': list(g['real']),
            'variants': [{'n': 1, 'direction': dirn, 'seed': seed, 'idea': f'〔{vid}〕' + idea}
                         for vid, dirn, seed, idea in g['variants']]})
    out['days'].append(dj)
json.dump(out, open(S + '/blueprints/M01.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- Markdown section 5 ----------
lines = []
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups'])
    vs = [v for g in d['groups'] for v in g['variants']]
    c = collections.Counter(v[1] for v in vs)
    diff = collections.Counter(REAL[r]['difficulty'] for g in d['groups'] for r in g['real'])
    lines.append(f"### 第 {d['day']} 天：真题 {nr} + 改编 {len(vs)} = 45（巩固 {c['巩固']} / 深化 {c['深化']} / 拓展 {c['拓展']}）\n")
    lines.append(f"真题难度分布：1 级 {diff[1]} 道、2 级 {diff[2]} 道、3 级 {diff[3]} 道。分组按下表顺序排版，组内先真题（易→难）后改编。\n")
    lines.append('| 组 | 分组标题 | 真题 | 改编 |')
    lines.append('|---|---|---|---|')
    for i, g in enumerate(d['groups'], 1):
        rs = '、'.join(g['real']) if g['real'] else '—'
        lines.append(f"| {i} | {kname(g['k'])} | {rs} | {len(g['variants'])} |")
    lines.append('')
    for i, g in enumerate(d['groups'], 1):
        lines.append(f"#### {i}. {kname(g['k'])}（真题 {len(g['real'])} + 改编 {len(g['variants'])}）\n")
        if g['real']:
            rr = '；'.join(f"{r} {REAL_NOTE[r]}（{REAL[r]['difficulty']} 级）" for r in g['real'])
            lines.append(f"- 真题：{rr}")
        else:
            lines.append('- 真题：无（本组全部为改编，补题库缺口）')
        for vid, dirn, seed, idea in g['variants']:
            lines.append(f"- 〔{vid}〕**{dirn}**｜种子 {seed}｜{idea}")
        lines.append('')
open(os.path.join(os.path.dirname(__file__), 'section5_days.md'), 'w', encoding='utf-8').write('\n'.join(lines))

# summary
tot = collections.Counter(v[1] for d in DAYS for g in d['groups'] for v in g['variants'])
print('OK. variants', sum(tot.values()), dict(tot), 'real', sum(seen_real.values()))
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['variants']) for g in d['groups'])
    print('day', d['day'], 'real', nr, 'var', nv, 'groups', len(d['groups']))
