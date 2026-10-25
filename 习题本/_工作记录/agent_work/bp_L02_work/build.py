# -*- coding: utf-8 -*-
"""Build blueprints/L02.json + the day-configuration section of blueprints/L02.md from plan.py, and validate."""
import json, re, sys, collections
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
sys.path.insert(0, S + '/bp_L02_work')
from plan import DAYS, ISSUES, SELF_SOLVED, K, KN

task = json.load(open(S + '/tasks_in/L02.json'))
REAL = {r['id']: r for r in task['real']}
assert task['days'] == [d['day'] for d in DAYS], (task['days'], [d['day'] for d in DAYS])

out = {'module': 'L02', 'days': DAYS, 'self_solved': SELF_SOLVED, 'issues': ISSUES}
json.dump(out, open(S + '/blueprints/L02.json', 'w'), ensure_ascii=False, indent=1)

# ------------------------------ validation ------------------------------
d = json.load(open(S + '/blueprints/L02.json'))
errs = []
seen = []
titles = set(K.values())
seeds_ok = set(REAL) | set(KN.values())
checked = set(re.findall(r'^OK\s+(D\d\d-\d+-\d+)', open(S + '/bp_L02_work/ideas_check.log').read(), re.M))
bad_ids = set(re.findall(r'^BAD\s+(D\d\d-\d+-\d+)', open(S + '/bp_L02_work/ideas_check.log').read(), re.M))
HINT = ['矛盾', '反对', '下反对', '假设', '代入', '推出关系', '真假推理', '归纳', '同义替换', '偷换', '无中生有', '考法']
TF_TITLES = {K[i] for i in range(1, 8)}
summary = []
for day in d['days']:
    nreal = sum(len(g['real']) for g in day['groups'])
    nvar = sum(v['n'] for g in day['groups'] for v in g['variants'])
    dirs = collections.Counter()
    for g in day['groups']:
        if g['title'] not in titles:
            errs.append(f"day {day['day']}: unknown title {g['title']}")
        seen += g['real']
        for r in g['real']:
            if r not in REAL:
                errs.append(f"day {day['day']}: real {r} not in module list")
        for v in g['variants']:
            dirs[v['direction']] += v['n']
            if v['direction'] not in ('巩固', '深化', '拓展'):
                errs.append(f"bad direction {v['direction']}")
            if v['seed'] not in seeds_ok:
                errs.append(f"day {day['day']} {g['title']}: bad seed {v['seed']}")
            if not isinstance(v['n'], int) or v['n'] < 1:
                errs.append('bad n')
            tags = re.findall(r'〔验算 (D\d\d-\d+-\d+)〕', v['idea'])
            for t in tags:
                if t not in checked or t in bad_ids:
                    errs.append(f'tag {t} not verified OK')
            is_tf = g['title'] in TF_TITLES or (g['title'] == K['mix'] and v['seed'] in [KN[i] for i in range(1, 8)])
            if is_tf and not tags:
                errs.append(f"truth/lie variant without verification tag: day {day['day']} {g['title']} {v['idea'][:30]}")
            m = re.search(r'【(?:题面|材料要点)】(.*?)(?:问：)', v['idea'])
            stem = m.group(1) if m else ''
            if not m:
                errs.append(f"idea without 【题面/材料要点】…问： structure: {v['idea'][:40]}")
            for h in HINT:
                if h in stem:
                    errs.append(f"hint word '{h}' inside stem part: day {day['day']} {g['title']} :: {stem[:60]}")
            if '（答案' not in v['idea']:
                errs.append(f"idea without marked answer: {v['idea'][:40]}")
    if nreal + nvar != 45:
        errs.append(f"day {day['day']}: real {nreal} + variants {nvar} != 45")
    summary.append((day['day'], nreal, nvar, dict(dirs), len(day['groups'])))
cnt = collections.Counter(seen)
dups = [k for k, c in cnt.items() if c > 1]
missing = sorted(set(REAL) - set(seen))
if dups: errs.append(f'duplicate real: {dups}')
if missing: errs.append(f'missing real: {missing}')
print('summary (day, real, variants, directions, groups):')
for s in summary: print('  ', s)
print('real used:', len(seen), '/', len(REAL), '| verified tags available:', len(checked))
print('issues:', len(d['issues']), '| self_solved:', len(d['self_solved']))
if errs:
    print('ERRORS:'); [print('  -', e) for e in errs]; sys.exit(1)
print('JSON OK')

# ------------------------------ markdown day section ------------------------------
INTRO = {
    7: '第 7 天（首次出现 · 试点周先做）：基础到中等为主。真假推理只练“找矛盾→看其余”“反对／下反对”“推出关系＋代入”三把主刀（考法一、三、四、五），归纳推理只练最常见的“可以推出”（考法八、九）和数量型（考法十一）。改编以巩固为主，每组安排 1 道拓展。答案待识别和难度最高的真题都不放在这一天。',
    14: '第 14 天：真假推理七个考法全部出现，重点是考法二（隐性矛盾，先翻译再找）和题库缺的考法七（一人多句、身份型）首次登场；归纳推理加入考法十（关联词与论述结构）。考法一只留 2 道快题做回顾。巩固与深化大致各半。',
    27: '第 27 天：与综合推理 C05（真假综合）同一天。L02 这一侧只练纯粹的真假判断，不做排序或匹配，避免与 C05 重复。真假推理以深化为主（多真多假、反对与下反对叠加、至多一假、链式指控）；归纳推理加入考法十二（规则·公式）和考法十三（选非、最能支持、不可能为真）。答案待识别的 2021SD-66 排在这一天。有 3 道标“考场可先跳过”。',
    36: '第 36 天（最后一次）：以深化和拓展为主。考法三、五、六、七都上难度（说谎人数、7 句恰 3 真、补充条件、元信息、诚实／说谎／随意）。归纳推理以数量、公式、弱推出为主。最后一组 8 道真假与归纳交替的混练用来模拟考场上自己判型。全天有 5 道标“考场可放弃”，解析里要写明取舍。',
}
lines = []
lines.append('| 天 | 真题 | 改编 | 巩固/深化/拓展 | 组数 |')
lines.append('|---|---|---|---|---|')
for day, nr, nv, dirs, ng in summary:
    lines.append(f"| 第 {day} 天 | {nr} | {nv} | {dirs.get('巩固', 0)}/{dirs.get('深化', 0)}/{dirs.get('拓展', 0)} | {ng} |")
lines.append('')
lines.append('> 组内顺序：先排真题（按表中顺序，由易到难），再按明细顺序排改编。组的小标题与 json 里的 `title` 完全一致。小标题只出现在书末解析里，题目页只有题号。')
lines.append('> 给出题人的统一提醒：')
lines.append('> 1. 【题面】／【材料要点】是成题时要写进题干的内容；【解析要点】【陷阱】只写进解析，不能出现在题干里。题干里不得出现“矛盾”“反对”“假设”“代入”“推出关系”这类会提示考法的字样，也不加“提示”。')
lines.append('> 2. 题干要用自己的话写，可以调整措辞、人名、地名和数字，但不能改动逻辑结构。真假题改动后，必须用自己写的程序重新枚举，确认四个选项里恰好一个符合设问。规划阶段的粗验见 `verify/bp_L02_ideas.py`，每条 idea 末尾的〔验算 Dxx-g-k〕就是脚本里的编号。')
lines.append('> 3. idea 里正确项多写在 A 位，只是为了方便阅读。成题时请打乱选项顺序，让全天 A/B/C/D 大致均衡；真题的答案不变。')
lines.append('> 4. 难度和参考用时写进解析。标“考场可放弃／可先跳过”的题，解析要写明取舍理由。')
lines.append('')
for gi, day in enumerate(d['days']):
    dd, nr, nv, dirs, ng = summary[gi]
    lines.append(f"### 第 {dd} 天：真题 {nr} + 改编 {nv} = 45（巩固 {dirs.get('巩固', 0)} / 深化 {dirs.get('深化', 0)} / 拓展 {dirs.get('拓展', 0)}）")
    lines.append('')
    lines.append(INTRO[dd])
    lines.append('')
    lines.append('| # | 组（小标题） | 真题（按顺序） | 改编数 | 巩固/深化/拓展 |')
    lines.append('|---|---|---|---|---|')
    for k, g in enumerate(day['groups'], 1):
        c = collections.Counter()
        for v in g['variants']:
            c[v['direction']] += v['n']
        real = '、'.join(f"{r}（{REAL[r]['difficulty']}级）" for r in g['real']) or '（无，纯改编）'
        lines.append(f"| {dd}-{k} | {g['title']} | {real} | {sum(c.values())} | {c.get('巩固', 0)}/{c.get('深化', 0)}/{c.get('拓展', 0)} |")
    lines.append('')
    for k, g in enumerate(day['groups'], 1):
        lines.append(f"#### {dd}-{k} {g['title']}")
        lines.append('')
        if g['real']:
            lines.append('真题：' + '；'.join(f"{r}（{REAL[r]['paper']}，{REAL[r]['difficulty']}级，答案 {REAL[r]['answer_official'] or '待识别'}）" for r in g['real']) + '。')
        else:
            lines.append('真题：无（本组全部为改编）。')
        lines.append('')
        for j, v in enumerate(g['variants'], 1):
            lines.append(f"{j}. 〔{v['direction']}｜种子 {v['seed']}〕{v['idea']}")
        lines.append('')
open(S + '/bp_L02_work/md_days.md', 'w').write('\n'.join(lines))
print('md day section written:', len('\n'.join(lines)), 'chars')
