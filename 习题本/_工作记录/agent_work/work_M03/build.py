# 生成 blueprints/M03.json 与 blueprints/M03.md，并做一致性检查
import json, os, re, sys, collections
BASE = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
sys.path.insert(0, BASE + '/work_M03')
from data_kaofa import KAOFA, DIRS, NUM, STEM_RULES
from data_days import DAYS, BACKUP, REPLACE, REAL_BRIEF, REAL_TIP

TASK = json.load(open(BASE + '/tasks_in/M03.json', encoding='utf-8'))
META = {q['id']: q for q in TASK['real']}
KF = {d['k']: d for d in KAOFA}
TITLE = {d['k']: f"考法{d['k']}：{d['name']}" for d in KAOFA}
kno = lambda k: NUM.index(k) + 1

# ---------------------------------------------------------------- 组装
def idea_text(vid, v):
    return (f"〔{vid}〕【{v['design']}】题干：{v['stem']}｜答案：{v['ans']}｜选项：{v['opts']}"
            f"｜解法：{v['sol']}｜易错：{v['trap'].rstrip('。')}｜参考用时：{v['time']}")

days_json = []
for d in DAYS:
    groups = []
    for g in d['groups']:
        vs = []
        for i, v in enumerate(g['vars'], 1):
            v['id'] = f"{d['day']}-{kno(g['k'])}-{i}"
            vs.append({'n': 1, 'direction': v['direction'], 'seed': v['seed'], 'idea': idea_text(v['id'], v)})
        groups.append({'title': TITLE[g['k']], 'real': g['real'], 'variants': vs})
    days_json.append({'day': d['day'], 'groups': groups})

SELF = [
 {'id': '2026GD-38', 'answer': 'B', 'note': '总量20×5=100台·天；12小时=0.5天用掉10台·天，剩90÷25台=3.6天'},
 {'id': '2026ZJA-46', 'answer': 'A', 'note': '水深差8−5=3米，每小时缩小0.2+0.3=0.5米→6小时，8:30+6小时=14:30'},
 {'id': '2026GK-67', 'answer': 'B', 'note': '设乙效率1、甲m：5(m+1)=3(1.5m+n)→0.5m=3n−5→m=6n−10'},
 {'id': '2026ZJA-56', 'answer': 'B', 'note': '2小时内甲加工72、乙108，丙120个用100分钟→每小时36:54:72=2:3:4；270按2:3:4分为60、90、120，丙比甲多60'},
]

ISSUES = [
 ('2020SZS-29', '需处理', r'题干（提取文字与原卷截图一致）写“若乙组先做15天”，官方解析却按“10乙”列式。按15天：3甲+4(甲+乙)=15乙+2甲→甲:乙=11:5，与“甲每天多种5棵”联立得甲$\frac{55}{6}$、乙$\frac{25}{6}$棵/天，不是整数，四个选项都不对；按10天才得B（1232米）。建议排版时按解析把题干订正为“10天”并加注“据官方解析订正”；不订正就剔除，用〔备1〕补位。已排第30天。另：粉笔把本题归植树问题，本蓝图按核心（效率比）归M03，末步是两侧植树（每侧棵数−1）。'),
 ('2022SC1-46', '需处理', r'首句“甲、丙先合作两天，完成了全部任务的__”中的分数，在提取文字和原卷截图里都缺失，题目不自足；官方答案也还在识别中。缺失值不能靠选项反推：在三条线效率都为正的前提下，A、B、C三项各对应一个可能的缺失值（D项在任何取值下都不成立）。需从原卷或官方解析补全后再用；补不全就剔除，用〔备2〕补位。已排第30天。题目截图底部还带下一题的残行，排版时裁掉。'),
 ('2025ZJA-58', '排版', r'选项是4幅折线图，只能用原卷截图排版（本轮重裁后的截图四图完整、无页脚水印）；改成文字版会丢掉选项。'),
 ('2021ZJA-65', '排版', r'提取文字丢了两个分数：“不低于$\frac{2}{3}x$吨”“不低于$\frac{3}{5}x$吨”（截图清晰）。用文字排版时按截图补上，否则题目不自足。'),
 ('2023SC-46', '排版', r'提取文字丢了“乙救援时间为甲的$\frac{1}{2}$”“丙救援时间为乙的$\frac{1}{3}$”两个分数（截图可见），用文字排版时补上。'),
 ('2024GK-72', '排版', r'提取文字丢了“又完成剩余任务量的$\frac{2}{3}$”中的分数（截图可见），用文字排版时补上。'),
 ('2022SC2-42', '排版', r'题目截图底部带下一题的半行残字，排版时裁掉或改用文字版（文字版完整）。'),
 ('2022SC1-54', '提示', r'题干只说“两个工程队同时开始工作且在完成所有工程之前中途不休息”，没有列明“实施方案”的范围（常规理解为4种：甲A乙B、甲B乙A、两队先合做A再合做B、先合做B再合做A，先完工的队转去支援）。官方答案仍在识别中，写解析时要按官方口径写清方案集合。题目截图底部也带下一题残行。'),
 ('2025JSA-61', '提示', r'官方解析截图被截断（只剩左上角两行）。答案B来自OCR（db/answer_fixes.json），已用程序复算（M单独4.5小时），解析需自写。'),
 ('2023HB-67', '提示', r'精确结束时刻是10:13:45（总时长73.75分钟），选项C“10点14分”是取整。答案C不变，解析写“约10点14分”，免得学生纠结。'),
 ('2020SZS-26', '提示', r'原卷错字“同行效率将降低15%”，应为“通行效率”，排版时直接订正或加注。'),
]
issues_json = [{'id': i, 'problem': f'【{lv}】{p}'} for i, lv, p in ISSUES]

OUT = {'module': 'M03', 'days': days_json, 'self_solved': SELF, 'issues': issues_json}

# ---------------------------------------------------------------- 检查
errs = []
allreal = [r for d in days_json for g in d['groups'] for r in g['real']]
ids = [q['id'] for q in TASK['real']]
cnt = collections.Counter(allreal)
if sorted(allreal) != sorted(ids): errs.append(f'真题不重不漏失败：多{[i for i in cnt if cnt[i] > 1]} 缺{sorted(set(ids) - set(allreal))} 外{sorted(set(allreal) - set(ids))}')
for d in days_json:
    tot = sum(len(g['real']) for g in d['groups']) + sum(v['n'] for g in d['groups'] for v in g['variants'])
    if tot != 45: errs.append(f"第{d['day']}天合计{tot}≠45")
    for g in d['groups']:
        for v in g['variants']:
            if v['direction'] not in ('巩固', '深化', '拓展'): errs.append('方向非法 ' + v['idea'][:12])
            s = v['seed']
            if not (s in ids or (s.startswith('考法') and s[2:] in NUM)): errs.append('种子非法 ' + s)
# 每条改编都在验算脚本中通过
chk_out = open(BASE + '/work_M03/ideas_check_output.txt', encoding='utf-8').read()
okkeys = set(re.findall(r'^OK  (\S+) ->', chk_out, re.M))
if re.search(r'^XX', chk_out, re.M): errs.append('验算脚本有未通过项')
vids = [v['id'] for d in DAYS for g in d['groups'] for v in g['vars']] + [b['id'] for b in BACKUP]
miss = [x for x in vids if x not in okkeys]
if miss: errs.append(f'未验算的改编：{miss}')
# 题干/选项禁用词（不得提示考法）
BAN = ['牛吃草', '赋值', '工程问题', '比例法', '整体法', '交替合作', '周期', '模型', '提示', '考法', '公式', '特值', '代入',
       '秒杀', '技巧', '资源消耗', '效率比型', '给定时间', '正负效率', '净效率', '方程', '比较优势', '差值', '统筹', '线性规划', '植树问题', '不定方程', '按劳分配']
for v in [v for d in DAYS for g in d['groups'] for v in g['vars']] + BACKUP:
    txt = v['stem'] + v['opts'].split('（')[0]
    hit = [w for w in BAN if w in txt]
    if hit: errs.append(f"〔{v['id']}〕题干含提示词{hit}")
# 种子为真题时，该真题须在同一天或更早出现
first_day = {r: d['day'] for d in days_json for g in d['groups'] for r in g['real']}
for d in days_json:
    for g in d['groups']:
        for v in g['variants']:
            if v['seed'] in first_day and first_day[v['seed']] > d['day']:
                errs.append(f"{v['idea'][:10]} 的种子 {v['seed']} 排在更晚的第{first_day[v['seed']]}天")
# 自解与题库标记一致
need_self = sorted(q['id'] for q in TASK['real'] if q['needs_self_solve'])
if sorted(s['id'] for s in SELF) != need_self: errs.append(f'自解名单不符：{need_self}')
if errs:
    print('\n'.join(errs)); sys.exit(1)

os.makedirs(BASE + '/blueprints', exist_ok=True)
with open(BASE + '/blueprints/M03.json', 'w', encoding='utf-8') as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- Markdown
def realdesc(i):
    q = META[i]
    ans = q['answer_official'] or next((s['answer'] + '，自解' for s in SELF if s['id'] == i), '待识别')
    return f"{i}（{q['paper']}，难度{q['difficulty']}，答案{ans}）：{REAL_BRIEF[i]}"

dayof = {r: d['day'] for d in DAYS for g in d['groups'] for r in g['real']}
L = []
A = L.append
diff = collections.Counter(q['difficulty'] for q in TASK['real'])
src_name = {'GD': '广东', 'GK': '国考副省级', 'ZJA': '浙江A', 'ZJB': '浙江B', 'JSA': '江苏A', 'SC': '四川', 'SD': '山东', 'HB': '河北', 'SZS': '深圳'}
src = collections.Counter(re.match(r'\d{4}([A-Z]+)', i).group(1) for i in ids)
src_txt = '、'.join(f'{src_name[k]} {v}' for k, v in src.most_common())
gd = [i for i in ids if 'GD-' in i]

A('# M03 工程问题：考法地图与三天配置（第 2、16、30 天）\n')
A('> 广东卷每年 1～2 道工程题：2022、2023 县级卷各 2 道（计划天数、差值恒定、牛吃草、推迟完成），2024 考“提前完成”，2025 考“中途人员变动”，2026 考“资源消耗（蓄电池）”。题目都是基础到中等难度，但常有一步关键转化（单位换算、比例、分段）。命题人会借鉴国考的“差值恒定、合作提效、字母关系”和浙江的“同时开工比例、水深变化、图像”。本模块按 15 个考法组织，题库缺的“进水排水标准型”和“报酬费用”由改编补齐。\n')
A('> 考生新要求：题目页不显示考法和出处，考生要自己识别题型。因此所有改编的题干只写情境和数据，不提示考法（写法约束见 §2.0）；分组标题只用于答案页和教研。改编编号〔天-考法序号-序〕与 M03.json 中每条 idea 开头的编号一致。\n')

A('## 0. 总览\n')
A(f"- 题库：{len(ids)} 道，难度 1/2/3 = {diff[1]}/{diff[2]}/{diff[3]}。来源：{src_txt}。广东 {len(gd)} 道：" + '、'.join(gd) + '。')
A('- 自解 4 道（2026GD-38、2026ZJA-46、2026GK-67、2026ZJA-56，均已用 Python 双法验算）；官方答案待识别 3 道（2022SC1-46、2021SD-42、2022SC1-54，按要求未解，全部排在第 30 天）。')
A('- 考法：15 个。题库缺 2 个：考法八（进水排水的标准管道型，题库只有 1 道水深变化）、考法十五（报酬费用，0 道）。题库少（≤2 道）3 个：考法六资源消耗、考法十三多工程调配、考法十四字母关系。另有一批常见子变形题库没有，改编来补，详见 §1 总表最后一列。')
A('- 三天配置：\n')
A('| 天 | 定位 | 真题 | 改编 | 巩固/深化/拓展 | 真题难度结构 | 考法组数 |')
A('|---|---|---|---|---|---|---|')
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['vars']) for g in d['groups'])
    c = collections.Counter(v['direction'] for g in d['groups'] for v in g['vars'])
    dc = collections.Counter(META[r]['difficulty'] for g in d['groups'] for r in g['real'])
    pos = {2: '首次·试点：基础到中等', 16: '第二次：中等为主', 30: '最后一次：深化与拓展'}[d['day']]
    A(f"| 第 {d['day']} 天 | {pos} | {nr} | {nv} | {c['巩固']}/{c['深化']}/{c['拓展']} | " + '、'.join(f'{k}★×{dc[k]}' for k in sorted(dc)) + f" | {len(d['groups'])} |")
tot = collections.Counter(); totr = collections.Counter(); totv = collections.Counter()
for d in DAYS:
    for g in d['groups']:
        totr[g['k']] += len(g['real']); totv[g['k']] += len(g['vars'])
A('')
A('- 各考法总题量（真题+改编）：' + ' · '.join(f"考法{k} {totr[k] + totv[k]}（{totr[k]}+{totv[k]}）" for k in NUM) + '。\n')
A('**本模块最该加练的 3 个点**')
A('1. **中途变化的分段列式（考法九、十）**：题库里最多的一类（8 道），广东 2025（中途人员变动）、国考 2024（多段合作+合作提效）都是它。要练到“画时间轴→按各队实际工作天数列一个总量方程”，不逐段求剩余。三天共配 ' + str(totv['九'] + totv['十']) + ' 道改编，覆盖反求返回时间、推迟天数、维修时长、提效百分比、等间隔投入、不等式最值。')
A('2. **资源消耗与牛吃草的“存量±流量”统一模型（考法六、七）**：广东 2026 刚考资源消耗（还藏着“12 小时=0.5 天”的单位换算），2023 县级考过牛吃草。下一步最可能出“中途增减+补给+取整”的组合，而且常披着积水、泄洪、排队、库存的外衣，考生要自己认出来。三天共配 ' + str(totv['六'] + totv['七']) + ' 道改编，其中 5 道是伪装情境（〔2-7-2〕隧道积水、〔16-6-1〕应急水源+补给、〔16-7-1〕政务大厅排队、〔16-7-2〕仓库库存、〔30-7-2〕水库泄洪），另有考法十一组的〔16-11-2〕工单池。')
A('3. **比例秒杀的时间差与同时开工（考法二、五）**：广东 2022—2024 连续三年考“提前/推迟”，浙江 2022、2025、2026 连考“同时开工的进度比/按效率分配”。这两类都是 30—60 秒的题，必须用“效率比↔时间反比”“提效 1/n→时间缩短 1/(n+1)”“同时段完成量之比=效率比”秒掉，不列方程。三天共配 ' + str(totv['二'] + totv['五']) + ' 道改编。\n')
A('**验算情况**')
A(f'- 真题：`{BASE}/verify/bp_M03_realcheck.py` 从题面数据独立复算 47 道（43 道官方答案全部一致，4 道自解）；2020SZS-29 只有按解析口径（乙先做 10 天）才得官方答案，见问题清单；3 道待识别答案按要求未解。')
n_chk = len(re.findall(r'^OK  ', chk_out, re.M))
A(f'- 改编：`{BASE}/verify/bp_M03_ideas.py` 对全部 84 条改编和 5 条备用改编逐条从题面数据计算（枚举、逐时模拟、线性规划网格），断言答案正确且四个选项中恰有一个正确，并核对主要干扰项的来源，共 {n_chk} 项检查，全部通过。正式出题若改动数字，请按此脚本的写法重算。')
A(f'- JSON：每天真题+改编=45、51 道真题不重不漏、种子合法、题干无提示词，均由 `{BASE}/work_M03/build.py` 自动检查。\n')
A('**调度说明**')
A('- 第 2 天（试点）只放题面完整、答案确定的真题：难度 1 的 11 道全部在这一天，另加 7 道难度 2；两道 2026 自解题（2026GD-38、2026ZJA-46）也在这一天，答案已验算。')
A('- 另两道 2026 自解题 2026ZJA-56、2026GK-67 放在第 16 天：国考 2026 的字母关系题在第 16 天首次出现，第 30 天再用 2020SC0725-46 和两道改编升级。')
A('- 4 道有问题或答案待识别的真题（2020SZS-29、2022SC1-46、2021SD-42、2022SC1-54）都排在第 30 天，留出修正和识别时间；前两道若无法修正，用 §3 末尾的〔备1〕〔备2〕补位，当天仍是 45 题。')
A('- 后续补进的 OCR 真题按 §3 末尾的替换预案替换第 16、30 天的指定改编，第 2 天不动。\n')

A('## 1. 考法清单（15 个）\n')
A('总表中“真题”列是本模块 51 道真题按主考法的归属（每题只归一个考法），括号是排在第几天；最后一列是题库没有、要靠改编补的子变形。\n')
A('| 考法 | 标记 | 真题数 | 真题（第几天） | 题库缺的子变形（改编补） |')
A('|---|---|---|---|---|')
for d in KAOFA:
    rl = '、'.join(f"{r}（D{dayof[r]}）" for r in d['real']) or '—'
    A(f"| {TITLE[d['k']]} | {d['mark']} | {len(d['real'])} | {rl} | {d['sub']} |")
A('')
for d in KAOFA:
    A(f"### {TITLE[d['k']]}" + (f"——{d['mark']}" if d['mark'] else '') + '\n')
    A(f"- **识别信号**：{d['signal']}")
    A(f"- **最快解法**：{d['fast']}")
    A(f"- **通法**：{d['general']}")
    A(f"- **常见陷阱与干扰项**：{d['trap']}")
    A(f"- **题库真题**：" + ('、'.join(d['real']) if d['real'] else '无') + '。')
    A(f"- **近年出现情况与趋势**：{d['trend']}\n")

A('## 2. 改编方向（巩固 / 深化 / 拓展）\n')
A('### 2.0 通用原则与题干写法约束\n')
A('- **巩固**不是换数字：换问法或已知/所求互换（正推变反推、求时间变求效率、求日期变求天数、求结果变求条件）。')
A('- **深化**：多一步转化（单位换算、体积守恒、折算标准单位）、两个考法嵌套、条件更隐蔽、要分类讨论或取整、加“至少/最多”追问；数据设计成必须用比例或整体法才能快做。')
A('- **拓展**：新情境（政务服务、防汛抗旱、应急救援、大湾区制造、快递物流、12345热线等）+跨模块（工程+费用/利润、工程+行程、工程+排列组合、工程+不定方程、工程+日期星期、工程+数列、工程+二次函数最值、工程+体积）。')
A('- **题干写法约束（考生新要求）**：')
for r in STEM_RULES: A(f'  - {r}')
A('')
for d in KAOFA:
    A(f"### 2.{kno(d['k'])} {TITLE[d['k']]}\n")
    for kind in ('巩固', '深化', '拓展'):
        for s in DIRS[d['k']][kind]:
            A(f'- **{kind}**｜{s}')
    A('')

A('## 3. 各天配置\n')
A('排列规则：组按考法编号排（编号大体由易到难）；组内先真题（由易到难）后改编（巩固→深化→拓展）。改编编号〔天-考法序号-序〕，与 JSON 中 idea 开头一致。每条改编给出：改编点、题干（可直接改写成正式题）、答案、四个选项及干扰项来源、解法、易错点、参考用时。题干已按 §2.0 去掉一切考法提示；出题时请保留这一点。\n')
for d in DAYS:
    nr = sum(len(g['real']) for g in d['groups']); nv = sum(len(g['vars']) for g in d['groups'])
    c = collections.Counter(v['direction'] for g in d['groups'] for v in g['vars'])
    A(f"### 第 {d['day']} 天：真题 {nr} + 改编 {nv} = {nr + nv}\n")
    A(f"定位：{d['stage']}改编构成：巩固 {c['巩固']} / 深化 {c['深化']} / 拓展 {c['拓展']}。\n")
    A('| 组 | 考法 | 真题 | 改编 |')
    A('|---|---|---|---|')
    for gi, g in enumerate(d['groups'], 1):
        A(f"| {gi} | {TITLE[g['k']]} | {len(g['real'])} | {len(g['vars'])} |")
    A('')
    seq = []; n = 0
    for g in d['groups']:
        for r in g['real']: n += 1; seq.append(f'{n} {r}')
        for v in g['vars']: n += 1; seq.append(f"{n} 〔{v['id']}〕")
    A('题号顺序：' + '｜'.join(seq) + '\n')
    for gi, g in enumerate(d['groups'], 1):
        A(f"#### {d['day']}-组{gi}｜{TITLE[g['k']]}\n")
        if g['real']:
            A('真题（按此顺序）：')
            for r in g['real']:
                A(f'- {realdesc(r)}')
                if r in REAL_TIP and d['day'] == 2: A(f'  - 提速点：{REAL_TIP[r]}')
        else:
            A('真题：无（题库缺或间隔复习，本组全部为改编）。')
        A('')
        A(f"改编 {len(g['vars'])} 道：\n")
        for v in g['vars']:
            A(f"{v['id'].split('-')[-1]}. 〔{v['id']}〕**{v['direction']}**｜种子 {v['seed']}｜{v['design']}")
            A(f"   - 题干：{v['stem']}")
            A(f"   - 答案：{v['ans']}；选项：{v['opts']}")
            A(f"   - 解法：{v['sol']}")
            A(f"   - 易错：{v['trap'].rstrip('。')}；参考用时：{v['time']}")
        A('')

A('### 新增真题的替换预案\n')
A('后续补进的 OCR 真题（2021 广东县级/乡镇卷、2021 四川和河北、2022 深圳、2026 贵州和河北联考）先按 §1 归入考法，再按下表处理，每天仍保持 45 题：')
A('- 难度 1—2 的放第 16 天，难度 3 的放第 30 天；第 2 天（试点日）不动。')
A('- 每补 1 道真题，删掉同天同考法组里下表所列的那道改编；同一考法再来第 2 道，删同组的下一道改编（先删巩固，再删深化），每组至少保留 1 道拓展。')
A('- 当天没有这个考法组时，新建该组，并删掉相邻考法组里的 1 道巩固。考法八、十五（题库缺）的改编尽量保留。\n')
A('| 新题考法 | 第 16 天默认替换 | 第 30 天默认替换 |')
A('|---|---|---|')
for k in NUM:
    a, b = REPLACE[k]
    a = f'〔{a}〕' if a[0].isdigit() else a
    A(f'| 考法{k} | {a} | 〔{b}〕 |')
A('')
A('### 备用改编（问题真题被剔除时补位，或作机动题）\n')
for b in BACKUP:
    where = f"第{b['day']}天「{TITLE[b['k']]}」" if b['day'] else f"「{TITLE[b['k']]}」机动"
    A(f"- 〔{b['id']}〕{where}｜{b['note']}｜**{b['direction']}**｜种子 {b['seed']}｜{b['design']}")
    A(f"  - 题干：{b['stem']}")
    A(f"  - 答案：{b['ans']}；选项：{b['opts']}")
    A(f"  - 解法：{b['sol']}")
    A(f"  - 易错：{b['trap'].rstrip('。')}；参考用时：{b['time']}")
A('')

A('## 4. 真题核查\n')
A('### 4.1 自解答案（无官方答案的 4 道，均用 Python 从题面数据双法验算）\n')
A('| id | 答案 | 一句话思路 |')
A('|---|---|---|')
for s in SELF: A(f"| {s['id']} | {s['answer']} | {s['note']} |")
A('')
A('### 4.2 其余真题的验算\n')
A('- 有官方答案的 44 道全部从题面数据重算：43 道与官方答案一致；2020SZS-29 只有按解析口径（乙先做 10 天）才得 B，与题干矛盾，见问题清单。')
A('- 2022SC1-46、2021SD-42、2022SC1-54 的官方答案仍在识别中，按要求未解。其中 2021SD-42 题面完整可用；2022SC1-46 题干缺数据；2022SC1-54 方案范围需按官方口径说明。')
A('- 51 道题目截图（本轮重裁版）已逐张目检：提取文字缺公式的 3 道（2021ZJA-65、2023SC-46、2024GK-72）截图完整，排版用截图或按截图补字即可。\n')
A(f'### 4.3 问题清单（{len(ISSUES)} 条）\n')
A('| id | 级别 | 问题与处理建议 |')
A('|---|---|---|')
for i, lv, p in ISSUES: A(f'| {i} | {lv} | {p} |')
A('')
A('级别说明：需处理=不修正不能用；排版=截图或文字有缺陷，按说明处理即可；提示=不影响使用，写解析时注意。\n')
A('### 4.4 其他提醒\n')
A('- 归类边界：2020SZS-26、2021JSA-53（粉笔归基础应用）、2022GD-32、2025GK-71（也可看作和差倍比）、2023HB-67（输液，消耗问题）、2025HB-75（疏散，也有统筹色彩）、2021ZJA-65（不等式整数解计数）、2022SC1-54（方案比较）都按“总量=效率×时间”的核心留在 M03，不建议移出。')
A('- 上次中断时记下的 2022JSA-63、2024SC-48、2025GD-39 截图残缺和 2025ZJA-58 截图水印，题目截图已在本轮重裁，复查完整，已从问题清单移除；2024SC-48、2024SC-49 的解析截图也已分开，不再串题。上次对 2022SC1-46 缺失值与选项对应关系的记录有误，已按 4.3 改正。')
A('- 2024SD-54 精确耗时 7.88 天，题干问“约多少天”，答案 B（8 天）无歧义。')

with open(BASE + '/blueprints/M03.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print('written; days:', [(d['day'], sum(len(g['real']) for g in d['groups']), sum(len(g['variants']) for g in d['groups'])) for d in days_json])
print('issues', len(ISSUES), 'self', len(SELF), 'variants', len(vids) - len(BACKUP), 'backups', len(BACKUP))
