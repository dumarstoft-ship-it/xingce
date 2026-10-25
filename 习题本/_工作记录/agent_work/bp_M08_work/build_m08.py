# -*- coding: utf-8 -*-
# 由 m08_plan.py 生成 blueprints/M08.json 与 blueprints/M08.md，并做一致性校验。
import json, re, sys, collections, importlib.util
SCR = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
sys.path.insert(0, SCR + '/bp_M08_work')
import m08_plan as P

TASK = json.load(open(SCR + '/tasks_in/M08.json'))
Q = {q['id']: q for q in TASK['real']}
EXCL = [i['id'] for i in P.ISSUES if i['action'].startswith('剔除')]
PENDING = [q['id'] for q in TASK['real'] if q['answer_pending_ocr']]
SELF = [q['id'] for q in TASK['real'] if q['needs_self_solve']]

# ------------------------------------------------------------ 校验
spec = importlib.util.spec_from_file_location('ideas', SCR + '/verify/bp_M08_ideas.py')
ideas_mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(ideas_mod)
CHECKED = set(ideas_mod.CHECKS)

kf_of_real = {}
for k in P.KAOFA:
    for i in k['real']:
        assert i not in kf_of_real, i
        kf_of_real[i] = k['code']
assert set(kf_of_real) | set(EXCL) == set(Q), set(Q) ^ (set(kf_of_real) | set(EXCL))
assert not (set(kf_of_real) & set(EXCL))
codes = [k['code'] for k in P.KAOFA]

used = []
vids = []
for d in P.DAYS:
    tot = 0
    for gi, g in enumerate(d['groups'], 1):
        used += g['real']; tot += len(g['real'])
        for si, v in enumerate(g['variants'], 1):
            assert v['vid'] == f"{d['day']}-{gi}-{si}", (v['vid'], d['day'], gi, si)
            assert v['direction'] in ('巩固', '深化', '拓展')
            assert v['seed'] in Q or v['seed'] in codes, v['seed']
            assert v['kf'] in codes
            assert v['vid'] in CHECKED, ('缺少核对函数', v['vid'])
            assert v['idea'].startswith(f"〔{v['vid']}〕")
            vids.append(v['vid']); tot += v['n']
        # 组内真题按难度不降
        diffs = [Q[i]['difficulty'] for i in g['real']]
        assert diffs == sorted(diffs), (g['title'], diffs)
    assert tot == 45, (d['day'], tot)
assert len(used) == len(set(used)), collections.Counter(used).most_common(3)
assert set(used) == set(Q) - set(EXCL), set(Q) - set(EXCL) - set(used)
assert len(vids) == len(set(vids))
for b in P.BACKUP:
    assert 'B-' + b['for'] in CHECKED
assert not (set(PENDING) & set(P.DAYS[0]['groups'][0]['real'] + [i for g in P.DAYS[0]['groups'] for i in g['real']])), '第7天不放待识别答案的题'
assert {s['id'] for s in P.SELF_SOLVED} == set(SELF)

# ------------------------------------------------------------ 统计
def kf_name(code): return next(k for k in P.KAOFA if k['code'] == code)
real_day = {i: d['day'] for d in P.DAYS for g in d['groups'] for i in g['real']}
var_by_kf = collections.Counter(v['kf'] for d in P.DAYS for g in d['groups'] for v in g['variants'])
real_by_kf = collections.Counter(kf_of_real[i] for i in real_day)
days_by_kf = collections.defaultdict(set)
for d in P.DAYS:
    for g in d['groups']:
        for i in g['real']: days_by_kf[kf_of_real[i]].add(d['day'])
        for v in g['variants']: days_by_kf[v['kf']].add(d['day'])
total_by_kf = {c: real_by_kf[c] + var_by_kf[c] for c in codes}
assert sum(total_by_kf.values()) == 180

CN = '一二三四五六七八九十'
def star_str(ids):
    c = collections.Counter(Q[i]['difficulty'] for i in ids)
    return '、'.join(f'{k}★×{c[k]}' for k in sorted(c)) if ids else '—'

def dir_count(vs):
    c = collections.Counter(v['direction'] for v in vs)
    return c['巩固'], c['深化'], c['拓展']

# ------------------------------------------------------------ JSON
out = {
 'module': P.MODULE,
 'name': P.NAME,
 'days': [],
 'self_solved': [dict(id=s['id'], answer=s['answer'], note=s['note'], verify=SCR + '/verify/bp_M08_selfsolve.py') for s in P.SELF_SOLVED],
 'issues': [dict(id=i['id'], action=i['action'], problem=i['problem']) for i in P.ISSUES],
 'kaofa': [dict(code=k['code'], name=k['name'], real=k['real'], gap=k['gap'], gap_forms=k['gaps']) for k in P.KAOFA],
 'excluded': EXCL,
 'pending_reference': [dict(id=p['id'], ref=p['ref'], note=p['note'] + '（非官方，仅供与 OCR 结果比对）') for p in P.PENDING_REF],
 'backup_variants': [dict(**{'for': b['for']}, day=b['day'], group=b['group'], n=1, direction=b['direction'], seed=b['seed'], idea=b['idea']) for b in P.BACKUP],
 'replace_rule': P.REPLACE_RULE,
 'verify_scripts': {
   'real_recheck': SCR + '/verify/bp_M08_realcheck.py',
   'self_solved': SCR + '/verify/bp_M08_selfsolve.py',
   'variant_ideas': SCR + '/verify/bp_M08_ideas.py'},
}
for d in P.DAYS:
    out['days'].append(dict(day=d['day'], stage=d['stage'], groups=[
        dict(title=g['title'], real=g['real'],
             variants=[dict(n=v['n'], direction=v['direction'], seed=v['seed'], idea=v['idea']) for v in g['variants']])
        for g in d['groups']]))
json.dump(out, open(SCR + '/blueprints/M08.json', 'w'), ensure_ascii=False, indent=1)

# ------------------------------------------------------------ MD
L = []
w = L.append
n_real = len(Q); n_used = len(real_day); n_var = len(vids)
n_off = n_real - len(SELF) - len(PENDING)
w('# M08 几何问题：考法地图与四天配置蓝图')
w('')
w(f'> 模块在第 **7、21、35、42** 天出现，每天 45 题。真题 {n_real} 道：{n_off} 道有官方答案（含 2 道建议剔除题），{len(SELF)} 道自解，{len(PENDING)} 道官方答案还在识别中；'
  f'建议剔除 {len(EXCL)} 道（{"、".join(EXCL)}），入册 {n_used} 道。全书共 180 题，其中改编 {n_var} 道。')
w('> 记号：idea 里的 √、π、²、³、⅓ 等是便于阅读的 Unicode 写法，成书时请改为 KaTeX（如 $8\\sqrt{3}$、$\\frac{1}{3}$、$\\pi$）；C(n,k) 为组合数。改编编号〔天-组-序〕与 M08.json 中每条 idea 开头的编号一致。')
w('> **题面无提示（考生新要求）**：题目页不显示考法和出处。每条 idea 里“题面”部分可以写进题干；“解”“干扰”“陷阱”只写进解析。题干和选项里不得出现考法、技巧、模型名称（如“蝴蝶”“鸟头”“将军饮马”“射影”“外心”“相似”），也不得出现“同某年某题”“沿用真题结构”之类字样，需要的结构一律在题干里用文字或示意图完整交代。分组标题只用于目录和解析页。')
w('')
w('## 0. 总览')
w('')
w('| 天 | 定位 | 真题 | 改编 | 巩固/深化/拓展 | 真题难度结构 |')
w('|---|---|---|---|---|---|')
short_stage = {7: '首次出现（试点日）：平面核心工具 + 立体体积入门 + 最值入门，基础到中等', 21: '平面深化：多边形与圆、勾股进阶、不规则面积、面积比进阶、最值、最短路径', 35: '立体专题 + 计数：等积分类、表面积、计数、相似比³、空间度量、展开与旋转体（题库缺）', 42: '综合冲刺：跨考法、跨模块、难题取舍，深化与拓展为主'}
sum_dir = [0, 0, 0]; sum_r = 0; sum_v = 0
for d in P.DAYS:
    reals = [i for g in d['groups'] for i in g['real']]
    vs = [v for g in d['groups'] for v in g['variants']]
    a, b, c = dir_count(vs); sum_dir = [sum_dir[0] + a, sum_dir[1] + b, sum_dir[2] + c]
    sum_r += len(reals); sum_v += len(vs)
    w(f"| 第 {d['day']} 天 | {short_stage[d['day']]} | {len(reals)} | {len(vs)} | {a}/{b}/{c} | {star_str(reals)} |")
w(f'| 合计 | | {sum_r} | {sum_v} | {sum_dir[0]}/{sum_dir[1]}/{sum_dir[2]} | |')
w('')
order = sorted(codes, key=lambda c: -total_by_kf[c])
w('**各考法总题量（真题 + 改编）**：' + ' · '.join(f"{c} {total_by_kf[c]}（{real_by_kf[c]}+{var_by_kf[c]}）" for c in order) + '。')
w('')
w('**本模块最该加练的 3 个点**')
t5 = total_by_kf['考法五']; t23 = total_by_kf['考法二'] + total_by_kf['考法三']; t911 = total_by_kf['考法九'] + total_by_kf['考法十一']
w(f'1. **三角形面积比模型（考法五）**：2026 广东原题就是这一类（2026GD-41，对角线分四块 + 百分数），国考 2023、2025，浙江 2022、2025，四川 2025、重庆 2026 也都考过，是近三年最热的几何考法。真题多为 3★，但“相对两块之积相等”“梯形 a²∶ab∶b²∶ab”“共角三角形”“同底等高”四个模型一旦熟练，60 秒内可解。全书配 {t5} 题（第 7、21、42 天）。')
w(f'2. **勾股与特殊角（考法二 + 三）**：题库里题量最多（15 道）。广东 2024 考“方位 + 等边三角形”，浙江 2026 考“行进转向 + 勾股”，国考 2023、2024 连续考勾股与特殊角。提速关键有三：先认勾股数，方位夹角画十字，记住 30°/45°/60°/120° 的边长比。折叠、相切、一线三直角是常见的“关键转化”。全书配 {t23} 题。')
w(f'3. **立体的等积与相似比³（考法九 + 十一）**：国考 2021、2023、2025 三次考圆锥相似（注水、漂浮、露出体积），广东县级 2023 考切割等积。广东省级卷还没考过立体，但命题人会借鉴国考考法，这一类是最可能出现的立体题。易错点集中在两处：未完全浸没要分类，k² 与 k³ 容易混用。全书配 {t911} 题。')
w('')
w('**验算情况**')
w(f'- 入册的 64 道有官方答案的真题已全部用程序从题面独立复算，只有 2022GK-73 与库内答案字母不同（选项顺序问题，见问题清单），其余全部一致：`{SCR}/verify/bp_M08_realcheck.py`（同一脚本还核查了 2 道建议剔除题，并给出 6 道待识别题的参考值）。')
w(f'- 6 道自解题用独立脚本求解，每题都断言“四个选项恰好一个成立”：`{SCR}/verify/bp_M08_selfsolve.py`。')
w(f'- {n_var} 条改编 idea 和 {len(P.BACKUP)} 条备用 idea 的数据、预期答案、选项唯一性，以及每条写明来源的干扰项，都已逐条断言核对（含蒙特卡洛、体素、枚举等暴力核对）：`{SCR}/verify/bp_M08_ideas.py`。出题时如果改动数字，请仿照同编号函数重算。')
w('')
w('**调度说明**')
w('- 6 道待识别答案的真题（2021GK-70、2021GK-74、2021SD-36、2021SD-41、2022SC1-53、2023SZ-51）都不排在第 7 天，不影响试点；每道都备好了补位改编（第 3 节末尾）。')
w('- 题库里的 4 道广东题（省级 2024GD-38、2026GD-41，县级 2023GD-34、2022GD-39）全部排在第 7 天打底；2026GD-41 是第 7 天唯一的 3★ 真题，放在最后一组压轴。')
w('- 2021SD-41 截图缺数据，排在第 35 天，若届时仍无法补全，按问题清单剔除并用〔B-2021SD-41〕补位。')
w('- 后续补入的 OCR 真题按第 3 节末尾的“替换预案”替换第 21、35、42 天的指定改编名额，第 7 天不动。')
w('- 组内题目按“真题 → 巩固 → 深化 → 拓展”排列，真题内部由易到难；题目页不显示分组标题。若担心同组相邻题暴露考法，排版时可只在解析页显示分组，题目页按组顺序连续编号即可。')
w('')
w('---')
w('')
w(f'## 1. 考法清单（{len(P.KAOFA)} 个）')
w('')
w('| 考法 | 真题数 | 真题难度 | 出现天 | 全书题量 | 题库状态 |')
w('|---|---|---|---|---|---|')
for k in P.KAOFA:
    c = k['code']; n = len(k['real'])
    status = '**题库缺**（0 题）' if n == 0 else ('偏少' if n <= 3 else '充足')
    w(f"| {k['short']} | {n} | {star_str(k['real'])} | {'、'.join(str(x) for x in sorted(days_by_kf[c]))} | {total_by_kf[c]} | {status} |")
w('')
for k in P.KAOFA:
    w(f"### {k['name']}{'【题库缺】' if k['gap'] else ''}")
    w(f"- **识别信号**：{k['signal']}")
    w(f"- **最快解法**：{k['fast']}")
    w(f"- **通法**：{k['general']}")
    w(f"- **陷阱与干扰项**：{k['traps']}")
    w(f"- **真题**：{'、'.join(k['real']) if k['real'] else '无（题库缺）'}。")
    w(f"- **趋势**：{k['trend']}")
    w(f"- **题库缺（改编补上）**：{k['gaps']}")
    w('')
w('---')
w('')
w('## 2. 改编方向（巩固 / 深化 / 拓展）')
w('')
w('> 题面骨架后面的〔编号〕指第 3 节已排进某一天的改编，那里有完整数据和答案。三类方向的含义：巩固是换问法、已知与所求互换，不只换数字；深化是多一步转化、嵌套、分类讨论、隐蔽条件或技巧才能快做的数据；拓展是新情境、跨模块组合，或真题里少见但合理的变形。')
w('')
w('| 考法 | 巩固 | 深化 | 拓展 |')
w('|---|---|---|---|')
for row in P.DIRECTIONS:
    w('| ' + ' | '.join(row) + ' |')
w('')
w('**还可以继续扩充的骨架**（备用，后续补进真题或需要换题时使用）：' + '；'.join(f'{chr(9312 + i)}{s}' for i, s in enumerate(P.EXTRA_SKELETONS)) + '。')
w('')
w('---')
w('')
w('## 3. 各天配置')
w('')
w('> 组内先放真题，后放改编；各组大体由易到难。每条改编的格式为：〔编号〕方向｜种子｜【变化点】题面 → 选项 → 答案 → 解 → 干扰 → 难度与参考用时。第 7 天写到可以直接出题的程度，其余各天也给出完整数据、选项和预期答案。所有答案已用 verify/bp_M08_ideas.py 核对。')
w('')
titles = {7: '第 7 天（首次出现·试点日）', 21: '第 21 天', 35: '第 35 天', 42: '第 42 天（最后一次）'}
for d in P.DAYS:
    reals = [i for g in d['groups'] for i in g['real']]
    vs = [v for g in d['groups'] for v in g['variants']]
    w(f"### {titles[d['day']]}｜真题 {len(reals)} + 改编 {len(vs)} = 45")
    w('')
    w(f"**定位**：{d['stage']}")
    w('')
    w('| 组 | 分组标题 | 真题（按顺序） | 改编数（巩/深/拓） |')
    w('|---|---|---|---|')
    for gi, g in enumerate(d['groups'], 1):
        a, b, c = dir_count(g['variants'])
        w(f"| {gi} | {g['title']} | {'、'.join(g['real']) if g['real'] else '—'} | {len(g['variants'])}（{a}/{b}/{c}） |")
    w('')
    for gi, g in enumerate(d['groups'], 1):
        w(f"#### 组 {gi}　{g['title']}")
        if g['real']:
            w('- **真题**：' + ' → '.join(f"{i}（{P.REAL_DESC[i]}）" for i in g['real']))
        else:
            w('- **真题**：无（题库缺或综合组，全部用改编）')
        w('- **改编**：')
        for v in g['variants']:
            body = v['idea'][len(f"〔{v['vid']}〕"):]
            w(f"  - **〔{v['vid']}〕 {v['direction']}**｜种子 {v['seed']}｜{body}")
        w('')
w('### 新增真题的替换预案与备用改编')
w('')
w('- **替换预案**：' + P.REPLACE_RULE)
w('- **备用改编**（对应真题被剔除，或待识别答案最终无法确认时补位，数据已核对）：')
for b in P.BACKUP:
    w(f"  - 第 {b['day']} 天「{b['group']}」·{b['direction']}：{b['idea']}")
w('')
w('---')
w('')
w('## 4. 真题核查')
w('')
w('### 4.1 复算结论')
w(f'- 入册的 64 道有官方答案的真题全部从题面独立复算，63 道与库内答案一致；2022GK-73 的计算结果 (√2+1)π+2 在本截图中是 C 项，库内记为 A（解析来自另一种选项顺序），需改字母。')
w('- 2024ZJA-67（菱形点阵 7 种边长）、2025SC-48（上界 24 的证明）、2022SC2-44（按解析图读出 8 个孔位、体素计数得 40）、2023GK-64（任取三角形坐标得 18 倍）、2024GK-71（8∶9）、2023GK-75（露出 0.801x）等容易出错的题都用暴力或坐标法复核，结论与官方一致。')
w('- 库内备注已过时的几处：2020SD-41、2024ZJA-65 的截图现已完整（选项、题干后半句都在），不再列为问题；2024SC-53、2025SC-48、2025SC-49 备注写“answer 缺失”，但库内已有官方答案（OCR 自解析图片），与复算一致。')
w('- 2022JSA-55（定积分）与 2023JSA-55（椭圆方阵）建议剔除，理由见问题清单。')
w('')
w('### 4.2 自解答案')
w('')
w('| id | 答案 | 思路 |')
w('|---|---|---|')
for s in P.SELF_SOLVED:
    w(f"| {s['id']} | {s['answer']} | {s['note']} |")
w('')
w(f'验算脚本：`{SCR}/verify/bp_M08_selfsolve.py`（2026GK-75 用原图坐标做最小外接矩形穷举，并对一般的“两腰内倾”梯形抽样验证“+25%”；2026GD-41 三种配对都试过，只有图中配对有正数解）。')
w('')
w('### 4.3 待识别答案的参考值（非官方，仅供与 OCR 结果比对，未写入 self_solved）')
w('')
w('| id | 参考答案 | 依据 |')
w('|---|---|---|')
for p in P.PENDING_REF:
    w(f"| {p['id']} | {p['ref']} | {p['note']} |")
w('')
w(f'### 4.4 问题清单（{len(P.ISSUES)} 条）')
w('')
w('| id | 处理建议 | 问题 |')
w('|---|---|---|')
for i in P.ISSUES:
    w(f"| {i['id']} | {i['action']} | {i['problem']} |")
w('')
open(SCR + '/blueprints/M08.md', 'w').write('\n'.join(L))

print('OK  考法', len(P.KAOFA), ' 改编', n_var, ' 入册真题', n_used, ' 剔除', EXCL)
for d in P.DAYS:
    reals = [i for g in d['groups'] for i in g['real']]; vs = [v for g in d['groups'] for v in g['variants']]
    print(f"  第{d['day']}天 真题{len(reals)} 改编{len(vs)} 巩/深/拓 {dir_count(vs)}")
print('  各考法', {c: (real_by_kf[c], var_by_kf[c]) for c in codes})
print('  问题清单条目', len(P.ISSUES))
