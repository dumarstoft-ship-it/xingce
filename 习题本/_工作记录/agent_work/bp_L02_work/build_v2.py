# -*- coding: utf-8 -*-
"""Build blueprints/L02.json and blueprints/L02.md from bp_L02_work/plan.py (single source of truth),
validate both, and print a summary. Run: python3 -I bp_L02_work/build_v2.py"""
import json, re, sys, collections, subprocess
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
W = S + '/bp_L02_work'
sys.path.insert(0, W)
from plan import DAYS, ISSUES, SELF_SOLVED, K, KN

task = json.load(open(S + '/tasks_in/L02.json'))
REAL = {r['id']: r for r in task['real']}
assert task['days'] == [d['day'] for d in DAYS], (task['days'], [d['day'] for d in DAYS])

# ------------------------------------------------------------------ JSON
out = {'module': 'L02', 'days': DAYS, 'self_solved': SELF_SOLVED, 'issues': ISSUES}
json.dump(out, open(S + '/blueprints/L02.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
d = json.load(open(S + '/blueprints/L02.json', encoding='utf-8'))          # re-read: JSON must parse

# ------------------------------------------------------------------ verification results (run fresh)
res = subprocess.run([sys.executable, '-I', W + '/ideas_v2.py'], capture_output=True, text=True)
OKTAGS = set(re.findall(r'^OK\s+(D\d\d-\d+-\d+)', res.stdout, re.M))
BADTAGS = set(re.findall(r'^BAD\s+(D\d\d-\d+-\d+)', res.stdout, re.M))
res_r = subprocess.run([sys.executable, '-I', W + '/real_v2.py'], capture_output=True, text=True)
REAL_OK = set(re.findall(r'^OK\s+(\S+?):', res_r.stdout, re.M))

errs = []
if res.returncode != 0 or BADTAGS:
    errs.append(f'ideas_v2.py failed: {sorted(BADTAGS)}')
if res_r.returncode != 0:
    errs.append('real_v2.py failed')

TF_TITLES = {K[i] for i in range(1, 8)}
TF_SEEDS = {KN[i] for i in range(1, 8)}
titles = set(K.values())
seeds_ok = set(REAL) | set(KN.values())
HINT = ['矛盾', '反对', '下反对', '假设', '代入', '推出关系', '真假推理', '归纳', '同义替换', '偷换', '无中生有', '考法',
        '一真一假', '必有一', '同真', '同假', '逆否', '等价', '对当', '强句', '弱句', '提示', '注意', '技巧', '秒杀',
        '题型', '日常结论', '翻译', '互推', '选言', '联言', '充分条件', '必要条件', '真值', '穷举', '公式法', '赋值',
        '十字交叉', '本题', '改编', '真题']
used_tags = []
seen = []
summary = []
per_day = {}


def is_tf(g, v=None):
    return g['title'] in TF_TITLES or (g['title'] == K['mix'] and v is not None and v['seed'] in TF_SEEDS)


def real_secs(rid, tf):
    dif = REAL[rid]['difficulty']
    return {1: 45, 2: 65, 3: 90}[dif] if tf else {1: 40, 2: 50, 3: 70}[dif]


for day in d['days']:
    dd = day['day']
    nreal = sum(len(g['real']) for g in day['groups'])
    nvar = sum(v['n'] for g in day['groups'] for v in g['variants'])
    dirs = collections.Counter()
    tf_n = ind_n = 0
    secs = 0
    skip = 0
    for gi, g in enumerate(day['groups'], 1):
        if g['title'] not in titles:
            errs.append(f'day {dd}: unknown title {g["title"]}')
        seen += g['real']
        for r in g['real']:
            if r not in REAL:
                errs.append(f'day {dd}: real {r} not in module list')
                continue
            tf = g['title'] in TF_TITLES
            tf_n += tf
            ind_n += (not tf)
            secs += real_secs(r, tf)
        for vi, v in enumerate(g['variants'], 1):
            dirs[v['direction']] += v['n']
            if v['direction'] not in ('巩固', '深化', '拓展'):
                errs.append(f'bad direction {v["direction"]}')
            if v['seed'] not in seeds_ok:
                errs.append(f'day {dd} {g["title"]}: bad seed {v["seed"]}')
            if not isinstance(v['n'], int) or v['n'] != 1:
                errs.append(f'day {dd}: n must be 1 (one idea per variant) -> {v["n"]}')
            tf = is_tf(g, v)
            tf_n += tf * v['n']
            ind_n += (not tf) * v['n']
            idea = v['idea']
            tags = re.findall(r'〔验算 (D\d\d-\d+-\d+)〕', idea)
            for t in tags:
                used_tags.append(t)
                if t != f'D{dd:02d}-{gi}-{vi}':
                    errs.append(f'tag {t} at wrong position (should be D{dd:02d}-{gi}-{vi})')
                if t not in OKTAGS:
                    errs.append(f'tag {t} not verified OK by ideas_v2.py')
            if tf and not tags:
                errs.append(f'truth/lie variant without verification tag: D{dd:02d}-{gi}-{vi}')
            m = re.search(r'【(?:题面|材料要点)】(.*?)问：(.*?)(?:【解析要点】|难度\d)', idea)
            if not m:
                errs.append(f'idea without 【题面/材料要点】…问：… structure: D{dd:02d}-{gi}-{vi}')
                continue
            stem, ask_opts = m.group(1), m.group(2)
            opts_clean = re.sub(r'（[^（）]*）', '', ask_opts)       # drop writer-only notes such as （答案…）
            for h in HINT:
                if h in stem:
                    errs.append(f"hint word '{h}' in stem: D{dd:02d}-{gi}-{vi} :: {stem[:50]}")
                if h in opts_clean:
                    errs.append(f"hint word '{h}' in question/options: D{dd:02d}-{gi}-{vi} :: {opts_clean[:60]}")
            if '（答案' not in idea:
                errs.append(f'idea without marked answer: D{dd:02d}-{gi}-{vi}')
            letters = re.findall(r'(?<![A-Za-z])([ABCD])\.', ask_opts)
            if letters[:4] != ['A', 'B', 'C', 'D']:
                errs.append(f'options not A-D in order: D{dd:02d}-{gi}-{vi} {letters}')
            mt = re.search(r'参考用时(\d+)秒', idea)
            if not mt:
                errs.append(f'no 参考用时: D{dd:02d}-{gi}-{vi}')
            else:
                secs += int(mt.group(1)) * v['n']
            if re.search(r'考场可(?:放弃|先跳过)', idea):
                skip += v['n']
    if nreal + nvar != 45:
        errs.append(f'day {dd}: real {nreal} + variants {nvar} != 45')
    summary.append((dd, nreal, nvar, dict(dirs), len(day['groups'])))
    per_day[dd] = dict(tf=tf_n, ind=ind_n, secs=secs, skip=skip, dirs=dirs, nreal=nreal, nvar=nvar)

cnt = collections.Counter(seen)
dups = [k for k, c in cnt.items() if c > 1]
missing = sorted(set(REAL) - set(seen))
if dups:
    errs.append(f'duplicate real: {dups}')
if missing:
    errs.append(f'missing real: {missing}')
if len(used_tags) != len(set(used_tags)):
    errs.append('duplicate verification tags')
unused = sorted(OKTAGS - set(used_tags))
if unused:
    errs.append(f'verified tags not used in plan: {unused}')
for r in REAL:
    if REAL[r]['module'] != 'L02':
        errs.append(f'{r} not L02 in task file')
tf_real = [r for g in (g for dd in d['days'] for g in dd['groups']) if g['title'] in TF_TITLES for r in g['real']]
for r in tf_real:
    if r not in REAL_OK:
        errs.append(f'truth/lie real {r} not re-checked OK by real_v2.py')
for e in d['issues']:
    if e['id'] not in REAL:
        errs.append(f'issue id {e["id"]} not a module real question')

print('summary (day, real, variants, directions, groups):')
for s in summary:
    print('  ', s, '| 真假/归纳 =', per_day[s[0]]['tf'], '/', per_day[s[0]]['ind'],
          '| 估计用时 %.1f 分钟' % (per_day[s[0]]['secs'] / 60), '| 可放弃', per_day[s[0]]['skip'])
print('real used:', len(seen), '/', len(REAL), '| verified idea tags:', len(OKTAGS), '| real re-checked:', len(REAL_OK))
print('issues:', len(d['issues']), '| self_solved:', len(d['self_solved']))
if errs:
    print('ERRORS:')
    for e in errs:
        print('  -', e)
    sys.exit(1)
print('JSON OK')

# ------------------------------------------------------------------ markdown: head with computed numbers
head = open(W + '/md_head_v2.md', encoding='utf-8').read()
days = [s[0] for s in summary]
fill = {
    '{{TF_RATIO}}': '，'.join(f'第 {dd} 天 {per_day[dd]["tf"]}∶{per_day[dd]["ind"]}' for dd in days),
    '{{DIR_RATIO}}': '，'.join(f'第 {dd} 天 {per_day[dd]["dirs"]["巩固"]}/{per_day[dd]["dirs"]["深化"]}/{per_day[dd]["dirs"]["拓展"]}' for dd in days),
    '{{LAST_DEEP}}': '%d%%' % round(100 * (per_day[days[-1]]['dirs']['深化'] + per_day[days[-1]]['dirs']['拓展']) / per_day[days[-1]]['nvar']),
    '{{TIME}}': '合计约 ' + '，'.join(f'第 {dd} 天 {per_day[dd]["secs"] / 60:.0f} 分钟' for dd in days) + (
        '，都在建议用时 45 分钟以内' if all(per_day[dd]['secs'] <= 45 * 60 for dd in days) else '（有的天超过建议用时 45 分钟，需删减）'),
    '{{SKIP}}': '，'.join(f'第 {dd} 天 {per_day[dd]["skip"]} 道' for dd in days),
}
for k, v in fill.items():
    assert k in head, k
    head = head.replace(k, v)
assert '{{' not in head

# ------------------------------------------------------------------ markdown: day sections
INTRO = {
    7: '第 7 天（首次出现 · 试点周先做）：基础到中等为主。真假推理只练“找矛盾→看其余”“反对／下反对”“推出关系＋代入”三把主刀（考法一、三、四、五），归纳推理只练最常见的“可以推出”（考法八、九）和数量型（考法十一）。改编以巩固为主，每组安排 1 道拓展。难度最高（3级、正确率低）的真题都不放在这一天。**本日每条 idea 都写到了可以直接出题的程度**：题面、四个选项、答案、解析要点、陷阱、难度、参考用时齐全，真假题都有验算编号。',
    14: '第 14 天：真假推理七个考法全部出现，重点是考法二（隐性矛盾，先翻译再找）和题库缺的考法七（一人多句、身份型）首次登场；归纳推理加入考法十（关联词与论述结构）。考法一只留 2 道快题做回顾。巩固略多于深化，拓展约占四分之一。',
    27: '第 27 天：与综合推理 C05（混合与一拖n，含真假综合）同一天。L02 这一侧只练纯粹的真假判断，不做排序或匹配，避免与 C05 重复。真假推理以深化为主（多真多假、反对与下反对叠加、至多一假、链式指控、等价互推）；归纳推理加入考法十二（规则·公式）和考法十三（选非、最能支持、不可能为真）。2021SD-66（至多一假＋名次情境，官方答案B已补齐）排在这一天。有 3 道标“考场可先跳过”。',
    36: '第 36 天（最后一次）：以深化和拓展为主。考法三、五、六、七都上难度（说谎人数、7 句恰 3 真、补充条件、元信息、诚实／说谎／随意）。归纳推理以数量、公式、弱推出为主。最后一组 8 道真假与归纳交替的混练用来模拟考场上自己判型。全天有 5 道标“考场可放弃”，解析里要写明取舍。',
}
L = []
L.append('---')
L.append('')
L.append('## 六、各天配置')
L.append('')
L.append('| 天 | 真题 | 改编 | 巩固/深化/拓展 | 真假∶归纳 | 组数 | 估计用时 | 可放弃／可先跳过 |')
L.append('|---|---|---|---|---|---|---|---|')
for dd, nr, nv, dirs, ng in summary:
    p = per_day[dd]
    L.append(f"| 第 {dd} 天 | {nr} | {nv} | {dirs.get('巩固', 0)}/{dirs.get('深化', 0)}/{dirs.get('拓展', 0)} | {p['tf']}∶{p['ind']} | {ng} | 约 {p['secs'] / 60:.0f} 分钟 | {p['skip']} 道 |")
L.append('')
L.append('> 组内顺序：先排真题（按表中顺序，由易到难），再按明细顺序排改编。组的小标题与 json 里的 `title` 完全一致；小标题只出现在书末解析里，题目页只有题号。')
L.append('> 给出题人的统一提醒：')
L.append('> 1. 【题面】／【材料要点】是成题时要写进题干的内容；【解析要点】【陷阱】只写进解析，不能出现在题干里。题干和选项里不得出现“矛盾”“反对”“假设”“代入”“一真一假”“等价”“逆否”这类会提示考法或解法的字样，也不加“提示”“注意”之类的话。')
L.append('> 2. 选项后括号里的（答案）（偷换：…）（无中生有）等标注只供出题人参考，成题时删去，意思写进解析。')
L.append('> 3. 题干要用自己的话写，可以调整措辞、人名、地名和数字，但不能改动逻辑结构。真假题改动后，必须用自己写的程序重新枚举（写到 `verify/<vid>.py`），确认四个选项里恰好一个符合设问。规划阶段的验算见 `bp_L02_work/ideas_v2.py`，每条 idea 末尾的〔验算 Dxx-g-k〕就是脚本里的编号。')
L.append('> 4. 不要把题目改回种子真题的原句子组合或原数据（考生通常刚做完那道真题）。')
L.append('> 5. idea 里正确项的位置只是规划时的写法。成题时请打乱选项顺序，让全天 A/B/C/D 大致均衡；真题的答案不变。')
L.append('> 6. 难度和参考用时写进 `difficulty`／`time_s` 字段（解析里不写“参考用时”，排版会自动加）。标“考场可放弃／可先跳过”的题，解析要写明取舍理由。')
L.append('')
for dd, nr, nv, dirs, ng in summary:
    day = next(x for x in d['days'] if x['day'] == dd)
    L.append(f"### 第 {dd} 天：真题 {nr} + 改编 {nv} = 45（巩固 {dirs.get('巩固', 0)} / 深化 {dirs.get('深化', 0)} / 拓展 {dirs.get('拓展', 0)}）")
    L.append('')
    L.append(INTRO[dd])
    L.append('')
    L.append('| # | 组（小标题） | 真题（按顺序） | 改编数 | 巩固/深化/拓展 |')
    L.append('|---|---|---|---|---|')
    for k, g in enumerate(day['groups'], 1):
        c = collections.Counter()
        for v in g['variants']:
            c[v['direction']] += v['n']
        real = '、'.join(f"{r}（{REAL[r]['difficulty']}级）" for r in g['real']) or '（无，纯改编）'
        L.append(f"| {dd}-{k} | {g['title']} | {real} | {sum(c.values())} | {c.get('巩固', 0)}/{c.get('深化', 0)}/{c.get('拓展', 0)} |")
    L.append('')
    for k, g in enumerate(day['groups'], 1):
        L.append(f"#### {dd}-{k} {g['title']}")
        L.append('')
        if g['real']:
            L.append('真题：' + '；'.join(f"{r}（{REAL[r]['paper']}，{REAL[r]['difficulty']}级，答案 {REAL[r]['answer_official']}）" for r in g['real']) + '。')
        else:
            L.append('真题：无（本组全部为改编）。')
        L.append('')
        for j, v in enumerate(g['variants'], 1):
            L.append(f"{j}. 〔{v['direction']}｜种子 {v['seed']}〕{v['idea']}")
        L.append('')

# ------------------------------------------------------------------ markdown: real-question check
L.append('---')
L.append('')
L.append('## 七、真题核查')
L.append('')
L.append(f'### 7.1 问题清单（{len(d["issues"])} 条，均为“保留使用、排版或解析时处理”，没有建议剔除的题）')
L.append('')
L.append('| id | 问题与处理建议 |')
L.append('|---|---|')
for e in d['issues']:
    L.append(f"| {e['id']} | {e['problem']} |")
L.append('')
L.append('### 7.2 自解答案')
L.append('')
L.append('无。32 道真题都有官方答案；原先缺官方答案的 2021SD-66 现已补齐官方答案B和解析截图，按有官方答案处理（json 的 `self_solved` 为空）。')
L.append('')
L.append('### 7.3 复核记录（已查、无需处理的项）')
L.append('')
L.append('- **答案**：17 道真假真题和 2 道数值型归纳真题（2024JSA-102、2020SC1206-84）由 `bp_L02_work/real_v2.py` 从题面独立穷举复核，全部与官方答案一致；其余 13 道归纳真题逐项对照了原题截图和官方解析，答案没有疑义（2020SZS-75 的归类说明见 7.1）。')
L.append('- **2021SD-66**：官方答案B（只有小夏说了假话）。把场上人数取 3～8 人分别复核，结论都一样；“小夏的名次不好”无法验证，和官方解析一样不计入。')
L.append('- **截图**：32 道题的 q_crop 和排版实际使用的去题号版（crops/real2_nonum）都重新看过。中断前记录的 2022SC2-80、2023SD-66 底边带进下一行文字的问题，重新裁图后已经没有了；2022GK-109、2022SD-74、2022ZJA-101、2023GK-110、2024HB-108、2025HB-108 的底边只有一两个像素的残点，不影响阅读。需要处理的只有 2023SC-85（见 7.1）。')
L.append('- **归类**：17 道真假题的核心都是找矛盾、反对、推出关系或元信息，没有一道需要先判真假再排序或匹配，所以都不归 C05；2025HB-110、2021SD-66 虽是名次情境，但靠矛盾／反对一步就能锁定，留在 L02。15 道归纳题都是“由非形式化材料推结论”的方向，不归 L01、L03。')
L.append('')

md = head.rstrip('\n') + '\n\n' + '\n'.join(L) + '\n'
open(S + '/blueprints/L02.md', 'w', encoding='utf-8').write(md)

# ------------------------------------------------------------------ markdown checks
md2 = open(S + '/blueprints/L02.md', encoding='utf-8').read()
merr = []
for r in REAL:
    if r not in md2:
        merr.append(f'real {r} not mentioned in md')
for dd in days:
    day = next(x for x in d['days'] if x['day'] == dd)
    for g in day['groups']:
        for v in g['variants']:
            if v['idea'] not in md2:
                merr.append('idea text missing in md')
for bad in ('答案待识别', '还在识别', 'verify/bp_L02_ideas.py` 对', '{{', '}}'):
    if bad in md2:
        merr.append(f'stale text in md: {bad}')
if merr:
    print('MD ERRORS:', merr[:10])
    sys.exit(1)
print('MD OK:', len(md2), 'chars,', md2.count('\n'), 'lines')
