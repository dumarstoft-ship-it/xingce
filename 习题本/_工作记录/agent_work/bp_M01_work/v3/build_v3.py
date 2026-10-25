# -*- coding: utf-8 -*-
"""Build blueprints/M01.json and blueprints/M01.md from the v3 plan (single source), with consistency checks."""
import json, re, sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from plan_real import KAOFA, REAL_NOTE, REAL_TIP
from plan_days import DAYS
from plan_meta import SELF_SOLVED, ISSUES, OVERRIDES, REPLACE_PLAN, REPLACE_RULE, NEWLY_ANSWERED, BORDER
from md_content import KF, DIRN

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
task = json.load(open(S + '/tasks_in/M01.json'))
REAL = {r['id']: r for r in task['real']}
SELF = {e['id']: e for e in SELF_SOLVED}
CN = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五']
HINT_WORDS = ['赋值', '十字', '设而不求', '不变量', '整体代换', '整体法', '份数', '单位"1"', '单位“1”', '量率', '提示', '考法', '技巧',
              '秒杀', '盈亏', '还原', '倒推', '代换', '代入', '方程', '比例法', '特值', '模型', '公式', '差不变', '注意：', '本题', '【']

errors = []
def err(m): errors.append(m)

# ---------------- checks ----------------
seen = collections.Counter(); vids = set()
day_of_real = {}
for d in DAYS:
    ks = [g['k'] for g in d['groups']]
    if ks != sorted(ks) or len(set(ks)) != len(ks): err(f"day {d['day']} group order {ks}")
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['variants']) for g in d['groups'])
    if nr + nv != 45: err(f"day {d['day']}: {nr}+{nv}!=45")
    for g in d['groups']:
        diffs = [REAL[r]['difficulty'] for r in g['real']]
        if diffs != sorted(diffs): err(f"day {d['day']} k{g['k']} real not easy->hard {diffs}")
        for r in g['real']:
            seen[r] += 1; day_of_real[r] = d['day']
            if r not in REAL: err(f'unknown real {r}')
            if r not in REAL_NOTE or r not in REAL_TIP: err(f'no note/tip {r}')
        vd = [v['d'] for v in g['variants']]
        for v in g['variants']:
            vid = v['id']; dd, kk, ii = vid.split('-')
            if int(dd) != d['day'] or int(kk) != g['k']: err(f'bad vid {vid}')
            if vid in vids: err(f'dup vid {vid}')
            vids.add(vid)
            if v['dir'] not in ('巩固', '深化', '拓展'): err(f'bad dir {vid}')
            if v['seed'] in REAL:
                if v['seed'] not in g['real']: err(f'seed {v["seed"]} of {vid} not in same group')
            elif v['seed'] != '考法' + CN[g['k']]: err(f'seed {v["seed"]} of {vid} should be 考法{CN[g["k"]]}')
            if len(v['opts']) != 4 or len(set(v['opts'])) != 4 or v['ans'] not in v['opts']: err(f'options/answer {vid}')
            if v['d'] not in (1, 2, 3) or v['t'] <= 0: err(f'difficulty/time {vid}')
            for w in HINT_WORDS:
                if w in v['stem'] or any(w in o for o in v['opts']): err(f'hint word "{w}" in stem/options of {vid}')
            for f in ('pt', 'stem', 'sol', 'dis', 'trap'):
                if len(v[f]) < 6: err(f'field {f} too short in {vid}')
missing = set(REAL) - set(seen); dups = [r for r, c in seen.items() if c > 1]
if missing: err(f'missing real {sorted(missing)}')
if dups: err(f'duplicated real {dups}')
need_self = {r['id'] for r in task['real'] if r['needs_self_solve']}
if set(SELF) != need_self: err(f'self_solved {set(SELF)} != {need_self}')
for it in ISSUES:
    if it['id'] not in REAL: err(f'issue id {it["id"]} not a module real')
for k in OVERRIDES:
    if k not in REAL: err(f'override id {k} not a module real')
# cross-check with numeric verification
vsrc = open(os.path.join(HERE, 'verify_v3.py'), encoding='utf-8').read()
vv = set(re.findall(r"check\('([0-9]+-[0-9]+-[0-9]+)'", vsrc))
if vv != vids: err(f'verify ids mismatch: only-plan={sorted(vids - vv)} only-verify={sorted(vv - vids)}')
if errors:
    print('ERRORS:'); [print('  ', e) for e in errors]; sys.exit(1)

# ---------------- helpers ----------------
def ans_of(rid):
    r = REAL[rid]
    return r['answer_official'] or SELF[rid]['answer']
def ans_label(rid):
    if REAL[rid]['answer_official']:
        return f"答案{REAL[rid]['answer_official']}" + ('（官方；截图选项顺序有误，见问题清单）' if rid == '2021GK-67' else '')
    return f"无官方答案，自解为{SELF[rid]['answer']}"
def idea_text(v):
    return (f"〔{v['id']}〕{v['pt']}。题面：{v['stem']} 选项：{'／'.join(v['opts'])}；答案：{v['ans']}。"
            f"解法：{v['sol']} 干扰项：{v['dis']} 解析要点：{v['trap']} 难度{v['d']}，参考用时{v['t']}秒。")
def kname(k): return KAOFA[k]
all_vars = [(d['day'], g['k'], v) for d in DAYS for g in d['groups'] for v in g['variants']]
real_by_k = collections.defaultdict(list)
for d in DAYS:
    for g in d['groups']:
        for r in g['real']: real_by_k[g['k']].append(r)
var_by_k = collections.defaultdict(list)
for day, k, v in all_vars: var_by_k[k].append(v)

# ---------------- JSON ----------------
out = {'module': 'M01', 'name': task['name'], 'days': [], 'self_solved': [], 'issues': [],
       'kaofa': {str(k): KAOFA[k] for k in KAOFA},
       'suggested_overrides': OVERRIDES,
       'replace_plan': REPLACE_PLAN, 'replace_rule': REPLACE_RULE,
       'verify_scripts': {'variants': HERE + '/verify_v3.py', 'self_solved_and_flagged_real': HERE + '/self_solve_v3.py',
                          'all_real_regression': HERE + '/verify_real_regression.py', 'build_and_checks': HERE + '/build_v3.py'}}
for d in DAYS:
    dj = {'day': d['day'], 'groups': []}
    for g in d['groups']:
        dj['groups'].append({'title': kname(g['k']), 'real': list(g['real']),
                             'variants': [{'n': 1, 'direction': v['dir'], 'seed': v['seed'], 'idea': idea_text(v)} for v in g['variants']]})
    out['days'].append(dj)
for e in SELF_SOLVED:
    out['self_solved'].append({'id': e['id'], 'answer': e['answer'], 'note': e['note'], 'jiexi': e['jiexi'], 'verify': e['verify']})
for it in ISSUES:
    out['issues'].append({'id': it['id'], 'action': it['action'], 'problem': it['problem']})
json.dump(out, open(S + '/blueprints/M01.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------------- statistics ----------------
dirs_day = {d['day']: collections.Counter(v['dir'] for g in d['groups'] for v in g['variants']) for d in DAYS}
diff_day = {d['day']: collections.Counter(REAL[r]['difficulty'] for g in d['groups'] for r in g['real']) for d in DAYS}
tot_dirs = collections.Counter(v['dir'] for _, _, v in all_vars)
src = collections.Counter()
for r in REAL.values():
    p = r['paper']
    for key, lab in [('广东', '广东'), ('国考', '国考副省级'), ('浙江', '浙江A'), ('江苏', '江苏A'), ('四川', '四川'), ('河北', '河北'), ('山东', '山东'), ('深圳', '深圳'), ('重庆', '重庆')]:
        if key in p: src[lab] += 1; break
    else: src[p] += 1
diffc = collections.Counter(r['difficulty'] for r in REAL.values())
gd = sorted([r for r in REAL if 'GD-' in r])

L = []
A = L.append
A('# M01 基础应用：和差倍比与比例——考法地图与四天配置（第 1、15、29、39 天）\n')
A('> 广东卷每年1～2道本模块的题：2022县级卷第31题（油耗代入）、2023县级卷第31题（连续卸货）和第33题（比例变化）、2024年第39题（库存百分比列方程）、2026年第36题（装机占比份数）和第37题（两天签约均值）——2026年数学运算的前两题都属本模块。题目不难，但常埋一个"基准"或"不变量"的关键转化；命题人借鉴国考的和差倍、盈亏取整、多主体增长、股权分配，以及浙江的设而不求、比例合并。本模块按15个考法组织，题库缺的"平均分摊与多退少补"和各考法里缺的子变形由改编补齐。\n')
A('> 考生新要求：题目页不显示考法和出处，考生要自己识别题型。因此所有改编的题面只写情境、数据和问句，不出现任何考法名或方法提示（写法约束见 §2.0，构建脚本对每条题面做了提示词扫描）；分组标题只用于答案页和教研排序。改编编号〔天-考法序号-序〕与 M01.json 中每条 idea 开头的编号一致。\n')
A('## 0. 总览\n')
A(f"- 题库：{len(REAL)} 道，难度 1/2/3 = {diffc[1]}/{diffc[2]}/{diffc[3]}。来源：" + '、'.join(f'{k} {v}' for k, v in src.most_common()) + f"。广东 {len(gd)} 道：{'、'.join(gd)}。")
A(f"- 自解 {len(SELF_SOLVED)} 道（{'、'.join(e['id'] + '→' + e['answer'] for e in SELF_SOLVED)}，均用 Python 枚举验算，答案唯一）。原先\"官方答案识别中\"的 8 道现已补齐，逐题核对：7 道与本模块验算一致；2021GK-67 数值无争议（121.6万元），但截图的 C、D 两项顺序与原卷相反，官方答案C按截图会对不上，列入问题清单首条（§4.2）。")
A(f"- 考法：15 个。题库缺 1 个：考法十五（平均分摊与多退少补，0 道）。题库少（≤3 道）3 个：考法六 多重比例合并（3）、考法八 增长率合成（3）、考法十一 等价代换与配套（2）。每个考法还列出了题库没有的子变形，见 §1 总表最后一列。")
A('- 四天配置：\n')
A('| 天 | 定位 | 真题 | 改编 | 巩固/深化/拓展 | 真题难度结构 | 考法组数 |')
A('|---|---|---|---|---|---|---|')
pos = {1: '首次·试点：基础到中等', 15: '第二次：中等为主', 29: '第三次：中等偏难', 39: '最后一次：深化与拓展'}
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['variants']) for g in d['groups'])
    c = dirs_day[d['day']]; df = diff_day[d['day']]
    dstr = '、'.join(f'{k}★×{df[k]}' for k in (1, 2, 3) if df[k])
    A(f"| 第 {d['day']} 天 | {pos[d['day']]} | {nr} | {nv} | {c['巩固']}/{c['深化']}/{c['拓展']} | {dstr} | {len(d['groups'])} |")
A('')
A('- 各考法总题量（真题＋改编）：' + ' · '.join(f"考法{CN[k]} {len(real_by_k[k]) + len(var_by_k[k])}（{len(real_by_k[k])}+{len(var_by_k[k])}）" for k in KAOFA) + f"。改编共 {len(all_vars)} 道：巩固 {tot_dirs['巩固']}、深化 {tot_dirs['深化']}、拓展 {tot_dirs['拓展']}。\n")
A('**本模块最该加练的 3 个点**')
A('1. **"基准"与份数（考法三、七）**：广东2026第36题（占比份数）、江苏2025"多0.6倍"、深圳2024逐层占比、国考2021三道百分数链（正确率6%～43%），错误几乎都出在"比谁""以谁为1"上。要练到：百分点直接加减、"多x倍"＝(1＋x)倍、"少37.5%"换成对方"多60%"、单位"1"切换时从后往前倒推。四天共配12道改编：〔1-2-1〕〔1-3-1〕〔1-3-2〕〔1-7-1〕〔15-3-1〕〔15-7-1〕〔15-7-2〕〔29-3-1〕〔29-7-1〕〔29-7-2〕〔39-7-2〕〔39-7-3〕。')
A('2. **三量关系的比例直除与连比（考法四、六）**：本模块真题最多的一类（9道），广东2026第37题就是"个数比、总量比→均量"。必须在45秒内用"总量比＝个数比×均量比""连比先统一中间项""部分比例→整体比例用十字交叉"直接出答案，不设未知数。四天共配' + str(len(var_by_k[4]) + len(var_by_k[6])) + '道改编，其中〔1-4-1〕〔15-6-1〕〔29-6-1〕专练"已知/所求互换"，〔1-4-2〕〔39-4-1〕专练多因子连乘，〔29-4-1〕〔39-4-2〕把三量关系藏进"船坐几人""奖品价值"里。')
A('3. **抓不变量与整体（考法五、十、十三）**：广东2023第33题（总人数涨20%后党员比例变化）、国考2022图书室转移、浙江2025设而不求，共同点是"不变的那个量"或"可以打包的那个组合"。要练到：总量不变、一方不变、差不变三种不变量一眼认出；一方给另一方m则差变2m；只问组合时不去求单个量。四天共配' + str(len(var_by_k[5]) + len(var_by_k[10]) + len(var_by_k[13])) + '道改编，其中〔29-8-1〕〔39-13-1〕故意放了用不上的条件，专练"整体看"。')
A('（第4个值得提前补的方向是考法八"增长率合成"：广东资料分析里的拉动、比重变化、人均思路正在被数量题借用，题库只有3道，改编补了〔15-8-1〕〔29-8-2〕〔39-8-2〕三种题库缺的问法。）\n')
A('**验算情况**')
A(f"- 改编：`{HERE}/verify_v3.py` 对全部 {len(all_vars)} 条改编逐条从题面数据重新求解（能枚举的都枚举，并检查整数性、唯一性），断言四个选项中恰有一个正确且就是计划答案，同时按\"干扰项\"栏写明的错误路径逐个重算干扰项，全部通过。正式出题若改动数字，请按此脚本的写法重算。")
A(f"- 真题：`{HERE}/self_solve_v3.py` 对4道自解题重新枚举验算，并复核了问题清单里的2021GK-67（两种选项顺序）、2026CQ-57（遮挡处两种补法都得52）、2022ZJA-60（两种口径）、2020HB-75（补回分数后得850），以及新批次6道候选题的答案；`{HERE}/verify_real_regression.py` 对全部74道真题从题面独立复算，除2021GK-67的选项顺序问题外与官方答案全部一致。")
A(f"- JSON：每天真题＋改编＝45、74道真题不重不漏、种子都在本组、题面和选项无提示词、改编编号与验算脚本一一对应，均由 `{HERE}/build_v3.py` 自动检查；md 与 json 由同一份数据生成。\n")
A('**调度说明**')
A('- 第1天（试点）只放题面完整、答案确定的真题：22道1级＋1道2级（2021JSA-51，差不变的标准题）；其中3道2026年真题（2026GD-36、2026GD-37、2026GK-66）没有官方答案，已自解并写好解析（见 §4.1）。截图有瑕疵的2021ZJA-61挪到第15天。')
A('- 有问题需要处理的真题都排在第15天以后：2026CQ-56、2022ZJA-60、2022ZJA-63在第15天；2024ZJA-64、2023GK-74在第29天；2021GK-67、2026CQ-57、2020HB-75、2021GK-64在第39天，留出修正时间。')
A('- 第29天为第39天的三道难题各放一道同结构预热题：〔29-3-2〕→2020HB-75，〔29-10-2〕→2020SC1206-48，〔29-13-2〕→2022GK-62（种子写的是考法，避免"先见改编后见真题"的错位）。')
A('- 后续补进的OCR真题按 §3.5 替换第15、29、39天的指定改编，第1天不动。\n')

# ---------------- §1 ----------------
A('## 1. 考法清单（15 个）\n')
A('总表中"真题"列是74道真题按主考法的归属（每题只归一个考法），括号是排在第几天；最后一列是题库没有、靠改编补的子变形。\n')
A('| 考法 | 标记 | 真题数 | 真题（第几天） | 题库缺的子变形（改编补） |')
A('|---|---|---|---|---|')
for k in KAOFA:
    rs = '、'.join(f"{r}（D{day_of_real[r]}）" for r in real_by_k[k]) or '—'
    A(f"| {kname(k)} | {KF[k]['mark']} | {len(real_by_k[k])} | {rs} | {KF[k]['missing']} |")
A('')
for k in KAOFA:
    A(f"### {kname(k)}" + (f"——{KF[k]['mark']}" if KF[k]['mark'] and KF[k]['mark'] not in kname(k) else '') + '\n')
    A(f"- **识别信号**：{KF[k]['signal']}")
    A(f"- **最快解法**：{KF[k]['fast']}")
    A(f"- **通法**：{KF[k]['general']}")
    A(f"- **常见陷阱与干扰项**：{KF[k]['trap']}")
    A(f"- **题库真题**：{'、'.join(real_by_k[k]) if real_by_k[k] else '无（题库缺）'}。")
    A(f"- **近年出现情况与趋势**：{KF[k]['trend']}\n")

# ---------------- §2 ----------------
A('## 2. 改编方向（巩固 / 深化 / 拓展）\n')
A('### 2.0 通用原则与题干写法约束\n')
A('- **巩固**不是换数字：换问法或已知/所求互换（正推变反推、求部分变求总量、求结果变求条件、问变化前变问变化后）。')
A('- **深化**：多一步转化（单位换算、基数切换、折算）、两个考法嵌套、条件更隐蔽（"空出一间""销售额相等"）、要分类讨论或取整、加"至少/最多"追问；数据设计成必须用比例、整体或不变量才能在90秒内做完。')
A('- **拓展**：新情境（政务服务、基层治理、大湾区跨境、乡村振兴、民生实事、应急防汛、农业园区等）＋跨模块（与概率、行程、工程、最值、不等式、日期计数、利润率组合），以及题库没有的新结构（百分点、同比环比、拉动、标记重捕、出资×时间、AA分摊）。')
A('- **题干写法约束（考生新要求）**：')
A('  - 题面只写情境、数据和问句；不出现任何考法名或方法提示，如"比例问题""盈亏""赋值""份数""不变量""整体""十字交叉""设而不求""代入""公式""提示：……"。方法只写在 kaofa/technique 字段和解析里。')
A('  - 建模必需的假设写成自然的条件，例如"每名医生只参加其中一天""每辆车早高峰运行的趟数相同""两次捕捞之间总数不变"。这些是条件，不是提示，必须写全，否则题面不自足。')
A('  - 规则类题目（考法一、十五）要把规则完整写进题面（"超过300分的部分只按一半计入""每满1000步记1分"），但不写"这是分段规则"之类的话。')
A('  - 不沿用种子真题的数据和情境：每条改编都换了数字和情境（构建时做过数字重合检查，剩下的只是个别数字在不同位置偶合）；同一组内的改编覆盖不同模型或问法，不出现"同一组数据正推一次、反推一次"。')
A('  - 不在题干、选项里暗示解法顺序，不在选项后加括注；分组标题、出处只放在答案页。')
A('  - 选项按数值从小到大列出（不带字母），由出题人分配A～D并使整批答案分布均匀；"凑数项"表示该位置没有明确的错误路径，出题时可换成更有迷惑性的值。\n')
for k in KAOFA:
    A(f"### 2.{k} {kname(k)}\n")
    for dname in ('巩固', '深化', '拓展'):
        vs = [v for v in var_by_k[k] if v['dir'] == dname]
        tail = '；'.join(f"{v['pt']}〔{v['id']}〕" for v in vs) if vs else '（本册此方向未单列，可按骨架补充）'
        A(f"- **{dname}**｜骨架：{DIRN[k][dname]}")
        A(f"  - 本册：{tail}")
    A('')

# ---------------- §3 ----------------
A('## 3. 各天配置\n')
A('排列规则：组按考法编号排；组内先真题（由易到难）后改编（按编号，大体巩固→深化→拓展）。每条改编给出：改编点、题面（可直接改写成正式题）、选项与答案、解法、干扰项来源、易错点、难度和参考用时。题面已按 §2.0 去掉一切考法提示；出题时请保留这一点。\n')
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['variants']) for g in d['groups'])
    c = dirs_day[d['day']]; df = diff_day[d['day']]
    A(f"### 第 {d['day']} 天：真题 {nr} + 改编 {nv} = 45\n")
    A(f"定位：{d['focus']}改编构成：巩固 {c['巩固']} / 深化 {c['深化']} / 拓展 {c['拓展']}；真题难度：" + '、'.join(f'{k}级 {df[k]} 道' for k in (1, 2, 3) if df[k]) + '。\n')
    A('| 组 | 考法 | 真题 | 改编 |')
    A('|---|---|---|---|')
    for i, g in enumerate(d['groups'], 1):
        A(f"| {i} | {kname(g['k'])} | {len(g['real'])} | {len(g['variants'])} |")
    A('')
    seq = []; n = 0
    for g in d['groups']:
        for r in g['real']: n += 1; seq.append(f'{n} {r}')
        for v in g['variants']: n += 1; seq.append(f"{n} 〔{v['id']}〕")
    A('题号顺序：' + '｜'.join(seq) + '\n')
    for i, g in enumerate(d['groups'], 1):
        A(f"#### {d['day']}-组{i}｜{kname(g['k'])}\n")
        if g['real']:
            A('真题（按此顺序）：')
            for r in g['real']:
                A(f"- {r}（{REAL[r]['paper']}，难度{REAL[r]['difficulty']}，{ans_label(r)}）：{REAL_NOTE[r]}")
                A(f"  - 提速点：{REAL_TIP[r]}")
            A('')
        else:
            A('真题：无（本组全部为改编，补题库缺口）。\n')
        A(f"改编 {len(g['variants'])} 道：\n")
        for j, v in enumerate(g['variants'], 1):
            A(f"{j}. 〔{v['id']}〕**{v['dir']}**｜种子 {v['seed']}｜{v['pt']}")
            A(f"   - 题面：{v['stem']}")
            A(f"   - 选项：{' / '.join(v['opts'])}（答案：{v['ans']}）")
            A(f"   - 解法：{v['sol']}")
            A(f"   - 干扰项：{v['dis']}")
            A(f"   - 易错/解析要点：{v['trap']}难度 {v['d']}，参考用时 {v['t']} 秒。")
        A('')
A('### 3.5 新增真题的替换预案\n')
A('cls/out_new_batch.jsonl 里已有6道新批次题被归入M01（尚未进入本模块清单），预案如下（答案均已用程序验算，见 self_solve_v3.py 末尾）：\n')
A('| 新题 | 考法 | 放第几天 | 替换 | 说明 |')
A('|---|---|---|---|---|')
for p in REPLACE_PLAN:
    A(f"| {p['new_id']} | {kname(p['k'])} | 第{p['day']}天 | {p['replace'] if p['replace'] in REAL else '〔' + p['replace'] + '〕'} | {p['note']} |")
A('')
A(f"通用规则：{REPLACE_RULE}\n")

# ---------------- §4 ----------------
A('## 4. 真题核查\n')
A('### 4.1 自解答案（无官方答案的4道）\n')
A('| id | 答案 | 一句话思路 | 所在天 |')
A('|---|---|---|---|')
for e in SELF_SOLVED:
    A(f"| {e['id']} | {e['answer']} | {e['note']} | 第{day_of_real[e['id']]}天 |")
A('')
A('完整解析（json 的 self_solved.jiexi，排版时作为这4道题的解析使用）：\n')
for e in SELF_SOLVED:
    A(f"- {e['id']}：{e['jiexi']}")
A('')
A(f"### 4.2 问题清单（{len(ISSUES)} 条）\n")
A('处理级别：fix＝排版前必须处理；check＝建议处理、问题轻微；keep＝保留，只需在解析或文字版里注意。\n')
A('| id | 级别 | 所在天 | 问题与建议 |')
A('|---|---|---|---|')
for it in ISSUES:
    A(f"| {it['id']} | {it['action']} | 第{day_of_real[it['id']]}天 | {it['problem']} |")
A('')
A('### 4.3 建议的覆盖文本（供 db/real_overrides.json 使用，本任务未改动题库文件）\n')
A('格式与 db/real_overrides.json 现有条目一致（stem/options 用于替换截图，extra 是附注，jiexi_text 替换解析截图）。同样的内容也放在 M01.json 的 suggested_overrides 里。\n')
for k, ov in OVERRIDES.items():
    A(f"- **{k}**：")
    A('```json')
    A(json.dumps({k: ov}, ensure_ascii=False, indent=1))
    A('```')
A('')
A('### 4.4 官方答案新补齐的8道（逐题核对）\n')
A('| id | 官方答案 | 本模块验算 | 结论 |')
A('|---|---|---|---|')
for a, b, c, e in NEWLY_ANSWERED:
    A(f"| {a} | {b} | {c} | {e} |")
A('')
A('### 4.5 归类核查（边界题，均保留在M01）\n')
A('| id | 可能被归到 | 保留在M01的理由 |')
A('|---|---|---|')
for a, b, c in BORDER:
    A(f"| {a} | {b} | {c} |")
A('')
open(S + '/blueprints/M01.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

print('OK. variants', len(all_vars), dict(tot_dirs), 'real', sum(seen.values()), 'issues', len(ISSUES))
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['variants']) for g in d['groups'])
    print('day', d['day'], 'real', nr, 'var', nv, 'groups', len(d['groups']), dict(dirs_day[d['day']]))
