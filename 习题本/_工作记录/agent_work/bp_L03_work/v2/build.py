# -*- coding: utf-8 -*-
"""Build blueprints/L03.md and blueprints/L03.json from the v2 data files, with validation."""
import json, re, sys, os, random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data_kaofa import KAOFA, ORDER, FRAMEWORK, RULES
from data_days_a import DAY2, DAY10
from data_days_b import DAY17, DAY23
from data_days_c import DAY30, DAY37
from data_misc import RNOTE, SELF_SOLVED, CHECKED, ISSUES
import verify_v2

SP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT_MD = SP + '/blueprints/L03.md'
OUT_JSON = SP + '/blueprints/L03.json'
TASK = json.load(open(SP + '/tasks_in/L03.json', encoding='utf-8'))
R = {r['id']: r for r in TASK['real']}
DAYS = [DAY2, DAY10, DAY17, DAY23, DAY30, DAY37]
DAYNUMS = [d['day'] for d in DAYS]
assert DAYNUMS == TASK['days'], (DAYNUMS, TASK['days'])
EXCLUDED = ['2020SZ1-40']
SELF = {d['id']: d for d in SELF_SOLVED}
LET = 'ABCD'
CNN = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五']
PROV = {'GD': '广东', 'GK': '国考', 'ZJA': '浙江', 'ZJB': '浙江', 'JSA': '江苏', 'SD': '山东', 'SC': '四川',
        'HB': '河北', 'SZ': '深圳', 'SZS': '深圳'}
PROV_ORDER = ['广东', '国考', '浙江', '江苏', '山东', '四川', '河北', '深圳']


def src(rid):
    m = re.match(r'^(\d{4})([A-Z]+)', rid)
    return int(m.group(1)), PROV[m.group(2)]


def ans(rid):
    a = R[rid]['answer_official']
    return a if a else SELF[rid]['answer']


def kno(k):
    return int(k[1:])


def ktitle(k):
    return KAOFA[k]['title']


def kshort(k):
    return '考法%s·%s' % (CNN[kno(k)], KAOFA[k]['short'])


# 题库缺/少的标注（★）：整类缺/少，或子考法缺，或高难有争议
STARNOTE = {
    'K2': '子考法题库缺：形式搭桥仅 1 道（深圳）、整合对方原因仅 1 道',
    'K5': '子考法题库缺：数据口径仅 2 道',
    'K6': '子考法题库少：同期对照仅 1 道，双重差分、撤去—反弹—恢复为 0',
    'K7': '题库缺：作正选仅 1 道',
    'K8': '题库缺：剂量反应、前瞻追踪、分批实施均为 0',
    'K9': '题库少：仅 2 道（2026 广东新考）',
    'K11': '子考法题库缺：政务回应质疑、三方观点',
    'K13': '题库少：4 道，全是 2022、2026 年国考/浙江',
    'K14': '题库少：仅浙江 3 道',
    'K15': '高难：6 道里 2 道答案有争议，靠改编补无争议版本',
}


def star(k):
    return ('★' + STARNOTE[k]) if k in STARNOTE else ''


def join_brief(brief, rest):
    sep = '' if brief.endswith(('。', '？', '！')) else '。'
    return brief + sep + rest


# 第 2 天（试点日）改编的预估难度（1 基础 / 2 中等 / 3 难），写进 idea 末尾
D2_DIFF = {'2-1-1': 1, '2-1-2': 2, '2-1-3': 2, '2-1-4': 1, '2-2-1': 1, '2-2-2': 2, '2-2-3': 2, '2-2-4': 1,
           '2-3-1': 1, '2-3-2': 2, '2-3-3': 1, '2-4-1': 2, '2-4-2': 2, '2-4-3': 1, '2-5-1': 1, '2-5-2': 2,
           '2-5-3': 2, '2-6-1': 1, '2-6-2': 1, '2-6-3': 2, '2-6-4': 1, '2-7-1': 2, '2-7-2': 1, '2-7-3': 2, '2-7-4': 1}


# ------------------------------------------------------------------ structure & codes
CLS = defaultdict(list)          # kaofa -> real ids (in schedule order)
PLACE = {}                       # real id -> (day, group index)
VARS = []                        # flat list of variant records
for D in DAYS:
    for gi, g in enumerate(D['groups'], 1):
        for rid in g['real']:
            assert rid in R, rid
            assert rid not in PLACE, ('dup', rid)
            PLACE[rid] = (D['day'], gi)
            assert g['k'] in KAOFA, (D['day'], g['k'], rid)
            CLS[g['k']].append(rid)
        for vi, v in enumerate(g['variants'], 1):
            code = '%d-%d-%d' % (D['day'], gi, vi)
            v['code'] = code
            v['day'] = D['day']
            VARS.append(v)
CODE = {v['code']: v for v in VARS}
placed = set(PLACE)
assert placed | set(EXCLUDED) == set(R), (set(R) - placed - set(EXCLUDED), placed - set(R))
assert not (placed & set(EXCLUDED))
for rid in placed:
    assert rid in RNOTE, ('no RNOTE', rid)

# ------------------------------------------------------------------ answer positions
POS = {}
DAYPOS = {}
for D in DAYS:
    seq = []
    for gi, g in enumerate(D['groups'], 1):
        for rid in g['real']:
            seq.append(['R', ans(rid), rid])
        for vi, v in enumerate(g['variants'], 1):
            for j in range(v['n']):
                seq.append(['V', None, v['code'], j])
    realcnt = Counter(x[1] for x in seq if x[0] == 'R')
    total = len(seq)
    assert total == 45, (D['day'], total)
    if D['day'] == 2:
        for x in seq:
            if x[0] == 'V':
                m = re.search(r'【答案位置】([ABCD])', CODE[x[2]]['idea'])
                assert m, x[2]
                x[1] = m.group(1)
                POS.setdefault(x[2], []).append(m.group(1))
    else:
        target = {L: max(11, realcnt[L]) for L in LET}
        order = sorted(LET, key=lambda L: (realcnt[L], L))
        i = 0
        while sum(target.values()) < total:
            target[order[i % 4]] += 1
            i += 1
        assert sum(target.values()) == total, (D['day'], target)
        need = {L: target[L] - realcnt[L] for L in LET}
        rng = random.Random(1000 + D['day'])
        prev = []
        for x in seq:
            if x[0] == 'R':
                prev.append(x[1])
                continue
            cands = [L for L in LET if need[L] > 0]

            def score(L):
                s = need[L] * 3 + rng.random() * 2
                if prev and prev[-1] == L:
                    s -= 6
                if len(prev) >= 2 and prev[-1] == L and prev[-2] == L:
                    s -= 20
                return s
            L = max(cands, key=score)
            need[L] -= 1
            x[1] = L
            prev.append(L)
            POS.setdefault(x[2], []).append(L)
    allc = Counter(x[1] for x in seq)
    varc = Counter(x[1] for x in seq if x[0] == 'V')
    DAYPOS[D['day']] = dict(real=realcnt, var=varc, all=allc, seq=[x[1] for x in seq])
    assert all(10 <= allc[L] <= 12 for L in LET), (D['day'], allc)


def pos_text(v):
    p = POS[v['code']]
    if len(p) == 1:
        return p[0]
    return '，'.join('第 %d 问 %s' % (i + 1, L) for i, L in enumerate(p))


def idea_full(v):
    t = v['idea'].rstrip()
    if '【答案位置】' not in t:
        t += '【答案位置】%s（同组内可与别的改编对调，全天保持 A～D 各 10～12 个）。' % pos_text(v)
    if v['code'] in D2_DIFF:
        t += '【预估难度】%d。' % D2_DIFF[v['code']]
    return t


def group_title(g):
    if g.get('title'):
        return g['title']
    if g['k'] == 'MIX':
        return '混编检验：%d 题（顺序已打乱，不看标题自己认题型）' % sum(v['n'] for v in g['variants'])
    return ktitle(g['k'])


# ------------------------------------------------------------------ JSON
J = dict(module='L03', days=[], self_solved=[], issues=[])
for D in DAYS:
    dd = dict(day=D['day'], groups=[])
    for gi, g in enumerate(D['groups'], 1):
        gg = dict(title=group_title(g), real=list(g['real']), variants=[])
        for v in g['variants']:
            assert v['direction'] in ('巩固', '深化', '拓展'), v['code']
            seed = v['seed']
            assert seed in R or re.match(r'^考法[一二三四五六七八九十]+$', seed), (v['code'], seed)
            gg['variants'].append(dict(n=v['n'], direction=v['direction'], seed=seed,
                                       idea='〔%s〕%s' % (v['code'], join_brief(v['brief'], idea_full(v)))))
        dd['groups'].append(gg)
    J['days'].append(dd)
for s in SELF_SOLVED:
    J['self_solved'].append(dict(id=s['id'], answer=s['answer'], note=s['note']))
for it in ISSUES:
    J['issues'].append(dict(id=it['id'], problem='【%s】%s' % (it['action'], it['problem'])))

# validation of JSON
seen = []
for dd in J['days']:
    nr = sum(len(g['real']) for g in dd['groups'])
    nv = sum(v['n'] for g in dd['groups'] for v in g['variants'])
    assert nr + nv == 45, (dd['day'], nr, nv)
    seen += [r for g in dd['groups'] for r in g['real']]
assert len(seen) == len(set(seen)) == 101
assert set(seen) | set(EXCLUDED) == set(R)
assert set(i['id'] for i in J['issues']) >= set(EXCLUDED)
need_self = [r['id'] for r in TASK['real'] if r['needs_self_solve']]
assert sorted(need_self) == sorted(s['id'] for s in J['self_solved']), need_self
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
json.dump(J, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ stats for md
VER = verify_v2.run()
assert all(ok for _, _, ok in VER), [x for x in VER if not x[2]]
VK = defaultdict(list)
for v in VARS:
    VK[v['k']].append(v)


def srcline(ids):
    c = Counter(src(i)[1] for i in ids)
    parts = ['%s %d' % (p, c[p]) for p in PROV_ORDER if c[p]]
    recent = sum(1 for i in ids if src(i)[0] >= 2024)
    gd = sorted(i for i in ids if src(i)[1] == '广东')
    gk = sorted(i for i in ids if src(i)[1] == '国考')
    s = '题库 %d 道（%s）；2024—2026 年 %d 道' % (len(ids), '、'.join(parts), recent)
    if gd:
        s += '；广东：%s' % '、'.join(gd)
    if gk:
        s += '；国考：%s' % '、'.join(gk)
    return s


def rid_fmt(rid):
    d, _ = PLACE[rid]
    return '%s（第 %d 天）' % (rid, d)


def fmt_ids(ids):
    return '、'.join(rid_fmt(i) for i in ids)


SUBTYPES = [
    ('形式搭桥（肯定后件修复、否定前件修复、双条件、两步链、特称结论）', '仅 2024SZ-38（深圳）1 道；广东 2026 卷翻译推理 2 道，“加强×翻译”是交叉点', ['10-1-2', '10-9-1', '23-5-1', '30-11-3', '37-11-6']),
    ('两方原因：把对方原因纳入本方链条', '仅 2021SD-75', ['10-1-3', '30-4-1']),
    ('数据口径：增量贡献、绝对数 vs 比率、基数、增速 vs 增量、门槛、净增 vs 新登记、措施算账', '仅 2022JSA-93、2023ZJA-107 两道', ['2-4-1', '10-5-1', '10-5-2', '17-2-5', '30-2-2', '30-2-3', '37-10-2', '37-5-3']),
    ('同期对照/双重差分、部分去除、对照组质量、撤去—反弹—恢复（ABA）', '同期对照仅 2023ZJA-104 一道', ['2-5-2', '2-5-3', '2-7-1', '17-1-1', '17-1-2', '17-1-3', '30-11-1']),
    ('排除他因与样本可比（唯一差异、基线可比、暴露量、自选样本→随机、均值回归、多重可比、幸存者偏差、扣除法、支持甲排除乙）', '作正选的仅 2020SZS-76；广东 2024-64 把它藏在“最不能支持”的三个支持项里', ['17-2-1', '17-2-2', '17-2-3', '17-2-4', '17-2-5', '17-8-1', '30-7-1', '30-7-2', '37-10-1', '37-10-3', '37-11-3']),
    ('剂量反应、前瞻追踪排除倒置、双向操纵、时序、分批实施', '缺（题库 3 道都是“人为操纵/直接暴露”）', ['17-3-2', '17-3-3', '17-3-4', '17-3-5', '23-10-2', '30-8-1', '30-8-2']),
    ('类比外推：动物→人、模拟→真实、模型→实物、样本/物种→总体、政策经验移植、仿生类比选非、功能检验', '题库仅 2 道（结构→功能、短期→长期），广东 2026-64 新考', ['17-8-3', '23-1-3', '23-1-4', '23-1-5', '23-1-6', '23-1-7', '37-4-1', '37-4-2', '37-4-3']),
    ('政务“回应质疑”（确实……但不会……、没有证据表明……）、三方观点支持中间方案', '仅 2025ZJA-109（厂家回应）', ['10-7-3', '23-3-2', '23-3-3', '30-6-2']),
    ('选非·反向项的伪装形态（反例伪装成补充说明、程度反例、使用不当反例、先天 vs 后天、从众他因）', '2026 年国考、浙江新出，题库 4 道', ['10-8-2', '17-7-2', '17-8-2', '23-9-1', '30-10-2', '30-10-3']),
    ('设问变形（得出结论的依据、实验得到的论据、最不可能基于）', '浙江独有 3 道，广东、国考未考', ['17-5-1', '17-5-2', '17-5-3', '37-6-1', '37-6-2']),
    ('跨模块与一材料两问（加强×前提、×解释、×削弱、×资料分析）', '缺', ['37-9-1', '37-9-3', '37-10-1', '37-10-2', '37-10-3']),
]
for _, _, codes in SUBTYPES:
    for c in codes:
        assert c in CODE, c

MAINLINE = {
    'K1': '从广东卷“桥在后半段”的模型出发，依次练缺口前移、原理→推论、“只能 vs 常见”、比较型搭桥、“论据加料 vs 碰到论点新词”；情境向大湾区交通、民生政策倾斜。',
    'K2': '非形式链条（补中间环、政策初衷 vs 准入门槛、整合对方原因、四环链）与形式搭桥（肯定后件修复、否定前件修复、双条件、两步链、特称结论）两条线并进；形式题全部用真值表或有限模型枚举验证只有一个选项能使论证有效。',
    'K3': '机理 vs 倒置/他因/部位偏移的辨析是主线，逐步加入比较型机理、一因两果、半路机理、“来源 vs 作用”、另一条机理同样加强、选非形式；情境向岭南生态和气候（红树林、回南天、空调病）倾斜。',
    'K4': '对论点问一句“为什么”，重点练比较对象的特殊性（年龄段、季节、节日）、整类 vs 局部、“不是 X 而是 Y”、“鉴于 A 和 B”。',
    'K5': '例子、数据、物证三分支；数据口径是重点（占比 vs 增量、绝对数 vs 比率、基数、增速 vs 增量、门槛、净增 vs 新登记），所有数字已核算（第 5.4 节）。',
    'K6': '对照组 → 去因去果 → 同期对照 → 撤去—反弹—恢复 → 部分去除 → 对照组的质量 → 双重差分，一步步加难；也把它们做成选非题的“支持项”。',
    'K7': '题库只有 1 道作正选，改编从唯一差异、基线可比、暴露量讲到自选样本、均值回归、多重可比、幸存者偏差、扣除法、支持甲同时排除乙。',
    'K8': '操纵实验（单向、双向）→ 剂量反应＋控制他因 → 前瞻追踪排除倒置 → 时序＋剂量 → 分批实施，题库缺的四种全部补上。',
    'K9': '以 2026GD-64 为母题：结构→功能（同构、功能检验）、短期→长期、模拟→真实（到真实环境直接检验、模型关键参数相似）、动物→人、样本/物种→总体、政策经验移植、仿生类比选非。',
    'K10': '措施四件套逐件练（必要、可行/不可行、有效、效果等同、无副作用），方案二选一找独有特点，再到方案选非、措施算账、“桥 vs 机理”比力度。',
    'K11': '先标“支持谁”；否定型（难以替代、并非越高越好、不会导致失业）、辩护型（确实……但不会……、没有证据表明……）、三方观点支持中间方案、“经济学家不以为然”。',
    'K12': '用广东 2024-64、2026-60 的同构题打底，再练领域/对象/范围/指标/时间偏移、方向不明的机制描述、复述现象、副作用≠有效、多论点题干先锁定被问的论点。',
    'K13': '他因（另一种动机、同期措施、先天 vs 后天、从众）、反例（全称、程度、使用不当、伪装成补充说明）、“不是 X 而是 Y”的反向证据、问题根源不在措施针对的环节。',
    'K14': '“得出结论的依据”（观察、追踪）、“实验得到的论据”（实验观测 vs 机理 vs 实验所得但无关）、“最不可能基于”（供需方向相反）。',
    'K15': '先圈限定词（更应、一刀切、基于上述原因、主要是为了、能解决），再按排序规则比：目的落空 > 可能性副作用；直接效果 > 必要前提 > 需求背景；桥 > 机理；功能匹配 > 威胁存在；附三道有争议或高难的真题讲评。',
}
def nv_of(*ks):
    return sum(v['n'] for k in ks for v in VK[k])


TOP3 = [
    ('选非题（考法十二、十三）', '广东 2024-64、2026-60 连续考“最不能支持”，国考 2026 年 4 道加强里 3 道是选非，2026 年国考、浙江又把答案换成他因、反例这类“反向项”。六天共 %d 道真题＋%d 道改编，第 2 天起每天都有。' % (len(CLS['K12']) + len(CLS['K13']), nv_of('K12', 'K13'))),
    ('类比与外推（考法九）', '2026 广东第 64 题新考“结构相似→推测功能”，题库作正选的只有 2 道；动物→人、模拟/模型→真实、样本→总体、政策经验移植全靠改编（%d 道），第 23、37 天集中练。' % nv_of('K9')),
    ('因果论证的对照、可比与操纵（考法六、七、八）', '广东 2024-64 的三个支持项全是“可比性”，这类思路既是正选也是选非题的支持项；题库作正选的少（可比 1 道、剂量/前瞻/分批 0 道），改编 %d 道，第 17 天集中、第 30、37 天回炉。' % nv_of('K6', 'K7', 'K8')),
]

# ------------------------------------------------------------------ markdown
L = []
w = L.append
nvar = len(VARS) + sum(v['n'] - 1 for v in VARS)
w('# L03 加强论证 · 考法地图与六天配置')
w('')
w('> 模块：逻辑判断·加强论证（含“不能支持/最不能支持”）｜出现在第 %s 天，每天 45 题｜真题 %d 道（排入 %d 道，建议剔除 %d 道）＋改编 %d 道 ＝ 270 道｜机读配置：`blueprints/L03.json`（与本文件一一对应，改编编号〔天-组-序〕两处一致）' % (
    '、'.join(str(d) for d in DAYNUMS), len(R), len(placed), len(EXCLUDED), nvar))
w('')
w('## 0. 概览')
w('')
w('### 0.1 一页看懂')
w('')
pc = Counter(src(i)[1] for i in R)
dc = Counter(R[i]['difficulty'] for i in R)
w('- **题库构成**：%s；难度 1 级 %d、2 级 %d、3 级 %d；无官方答案、由本蓝图自解的 7 道全部是 2026 年新题（第 5.2 节）。' % (
    '、'.join('%s %d' % (p, pc[p]) for p in PROV_ORDER if pc[p]), dc[1], dc[2], dc[3]))
w('- **考法**：15 个（第 2 节）。★ 标“题库缺/少”的 %d 个：%s；题库缺的子考法和对应改编汇总在 2.16。' % (
    len(STARNOTE), '；'.join('%s（%s）' % (kshort(k), STARNOTE[k]) for k in ORDER if k in STARNOTE)))
w('- **广东命题信号**：2023 县级 57、2025 年 60 考搭桥（措施→中间效果→目标）；2022 县级 67 考“更应”力度；2024 年 64、2026 年 60 考“最不能支持”（答案分别是“死亡率≠发病率”“安全性≠抗衰老”）；2026 年 64 新考“结构相似→推测功能”。')
w('- **本模块最该加练的 3 个点**：')
for i, (t, d) in enumerate(TOP3, 1):
    w('  %d. **%s**：%s' % (i, t, d))
w('- **官方答案补齐后的调整**：原“答案识别中”的 8 道真题已有官方答案，6 道与规划时的预判一致；2021GK-109（官方 C）改归考法十、2021SD-74（官方 C，有争议）改到第 30 天力度组讲评，以它们为种子的 3 道改编已改写或撤换（第 5.3 节）。2020SZ1-40 官方答案存疑（正确率 5%），建议剔除（第 5.5 节）。')
w('')
w('| 天 | 第几次 | 真题 | 改编 | 巩固/深化/拓展 | 真题难度 1/2/3 | 本日主题 |')
w('|---|---|---|---|---|---|---|')
for i, D in enumerate(DAYS, 1):
    nr = sum(len(g['real']) for g in D['groups'])
    dirs = Counter()
    for g in D['groups']:
        for v in g['variants']:
            dirs[v['direction']] += v['n']
    dd = Counter(R[r]['difficulty'] for g in D['groups'] for r in g['real'])
    w('| 第 %d 天 | %d | %d | %d | %d / %d / %d | %d / %d / %d | %s |' % (
        D['day'], i, nr, 45 - nr, dirs['巩固'], dirs['深化'], dirs['拓展'], dd[1], dd[2], dd[3], D['focus'].split('。')[0]))
w('')
w('### 0.2 出题约定')
w('')
rules = RULES.strip().split('\n', 1)[1] if RULES.strip().startswith('###') else RULES.strip()
w(rules.strip())
w('')
w(FRAMEWORK.strip())
w('')
w('---')
w('')
w('## 2. 考法清单（15 个；★ = 题库缺或很少，是改编的重点）')
w('')
w('| 考法 | 题库 | 来源（省/卷） | 2024—2026 | 改编数 | 排在哪几天 | 题库缺/少（★） |')
w('|---|---|---|---|---|---|---|')
for k in ORDER:
    ids = CLS[k]
    c = Counter(src(i)[1] for i in ids)
    days_k = sorted(set([PLACE[i][0] for i in ids] + [v['day'] for v in VK[k]]))
    w('| %s %s | %d | %s | %d | %d | %s | %s |' % (
        '考法' + CNN[kno(k)], KAOFA[k]['short'], len(ids),
        '、'.join('%s %d' % (p, c[p]) for p in PROV_ORDER if c[p]) or '—',
        sum(1 for i in ids if src(i)[0] >= 2024), sum(v['n'] for v in VK[k]), '、'.join(str(d) for d in days_k),
        star(k) or '—'))
w('| （剔除） | 1 | 深圳 1 | 0 | — | — | 2020SZ1-40 答案存疑，见第 5.5 节 |')
w('')
for k in ORDER:
    K = KAOFA[k]
    w('### 2.%d %s%s' % (kno(k), K['title'], ('　' + star(k)) if star(k) else ''))
    w('')
    w('- **识别信号**：' + K['signal'])
    w('- **最快解法**：' + K['fast'])
    w('- **通法**：' + K['general'])
    w('- **陷阱与干扰项设计**：' + K['traps'])
    w('- **真题（%d 道）**：%s' % (len(CLS[k]), fmt_ids(CLS[k]) if CLS[k] else '无（题库缺）'))
    w('- **出现情况与趋势**：%s。%s' % (srcline(CLS[k]) if CLS[k] else '题库无', K['trend']))
    w('')
w('### 2.16 题库缺或很少的子考法 → 改编补在哪里')
w('')
w('| 子考法 | 题库情况 | 改编（编号见第 4 节） |')
w('|---|---|---|')
for name, st, codes in SUBTYPES:
    w('| %s | %s | %s |' % (name, st, '、'.join('〔%s〕' % c for c in codes)))
w('')
w('---')
w('')
w('## 3. 改编方向（巩固 / 深化 / 拓展）')
w('')
w('> 统一要求：只换情境和数字不算变式。**巩固**＝换问法、换缺口位置、已知与所求互换、选是变选非；**深化**＝多一步、条件更隐蔽、两个“沾边项”比力度、两种考法嵌套；**拓展**＝广东政务、产业、大湾区、民生情境，或跨模块（翻译、数据计算、解释、削弱、前提）。下面每个方向列出全部改编的一句话骨架（〔天-组-序〕），完整的题面骨架、正确项、干扰项和答案位置见第 4 节同编号条目。')
w('')


def skeleton(v, n=110):
    m = re.search(r'【(?:骨架|共用材料)】(.*?)(?=【|$)', v['idea'])
    t = m.group(1) if m else ''
    return t if len(t) <= n else t[:n] + '……'


for k in ORDER:
    w('**%s %s**' % ('考法' + CNN[kno(k)], KAOFA[k]['short']) + ('（%s）' % star(k) if star(k) else ''))
    w('')
    w('- 主线：' + MAINLINE[k])
    for dname in ('巩固', '深化', '拓展'):
        vs = [v for v in VK[k] if v['direction'] == dname]
        if not vs:
            continue
        items = '；'.join('〔%s〕%s' % (v['code'], v['brief']) for v in vs)
        w('- **%s**（%d）：%s' % (dname, sum(v['n'] for v in vs), join_brief(items, '')))
        ex = vs[0]
        w('  - 骨架示例〔%s〕：%s' % (ex['code'], skeleton(ex)))
    w('')
w('---')
w('')
w('## 4. 各天配置')
w('')
w('> 读法：每天按“组”排列，组内先真题、后改编；组标题只用于排版和解析，题目页不显示。真题表里的“要点”给解析用；改编条目依次是 编号｜方向｜种子｜答案位置，后面是可直接照着出题的骨架。第 2 天（试点日）每道改编都写到了题干、设问、正确项、三个干扰项和答案位置。')
w('')
for i, D in enumerate(DAYS, 1):
    nr = sum(len(g['real']) for g in D['groups'])
    dp = DAYPOS[D['day']]
    dirs = Counter()
    for g in D['groups']:
        for v in g['variants']:
            dirs[v['direction']] += v['n']
    dd = Counter(R[r]['difficulty'] for g in D['groups'] for r in g['real'])
    tag = '（第 1 次出现·试点日，规划最细）' if i == 1 else ('（最后一次·冲刺）' if i == len(DAYS) else '（第 %d 次出现）' % i)
    w('### 4.%d 第 %d 天%s' % (i, D['day'], tag))
    w('')
    w('- **本日定位**：' + D['focus'])
    w('- **数量**：真题 %d ＋ 改编 %d ＝ 45｜改编：巩固 %d、深化 %d、拓展 %d｜真题难度：1 级 %d、2 级 %d、3 级 %d' % (
        nr, 45 - nr, dirs['巩固'], dirs['深化'], dirs['拓展'], dd[1], dd[2], dd[3]))
    w('- **答案分布**：真题 %s；改编 %s；全天 %s' % tuple(
        '、'.join('%s %d' % (L, c[L]) for L in LET) for c in (dp['real'], dp['var'], dp['all'])))
    w('')
    for gi, g in enumerate(D['groups'], 1):
        nv = sum(v['n'] for v in g['variants'])
        gd = Counter()
        for v in g['variants']:
            gd[v['direction']] += v['n']
        gds = '、'.join('%s %d' % (x, gd[x]) for x in ('巩固', '深化', '拓展') if gd[x])
        w('#### 组 %d｜%s（真题 %d ＋ 改编 %d：%s）' % (gi, group_title(g), len(g['real']), nv, gds))
        w('')
        if g.get('note'):
            w('*组说明*：' + g['note'])
            w('')
        if g['real']:
            w('| 序 | 真题 | 来源 | 难度 | 答案 | 要点 |')
            w('|---|---|---|---|---|---|')
            for j, rid in enumerate(g['real'], 1):
                a = ans(rid)
                if rid in SELF:
                    a += '（自解）'
                w('| %d | %s | %s | %d | %s | %s |' % (j, rid, R[rid]['paper'], R[rid]['difficulty'], a, RNOTE[rid]))
            w('')
        for v in g['variants']:
            seed = v['seed']
            if seed in R:
                sd = PLACE.get(seed, (None,))[0]
                seed_s = seed + ('' if sd == D['day'] else '（第 %d 天真题）' % sd)
            else:
                seed_s = seed
            kk = '' if v['k'] == g['k'] else '｜%s' % kshort(v['k'])
            nn = '｜一材料 %d 问' % v['n'] if v['n'] > 1 else ''
            dif = '｜预估难度 %d' % D2_DIFF[v['code']] if v['code'] in D2_DIFF else ''
            w('- **〔%s〕%s｜种子 %s｜答案 %s%s%s%s**：%s' % (v['code'], v['direction'], seed_s, pos_text(v), dif, kk, nn, v['brief']))
            w('')
            w('  ' + v['idea'].strip())
            w('')
    w('')
w('---')
w('')
w('## 5. 真题核查')
w('')
w('### 5.1 归类说明')
w('')
w('归类以“正确项靠什么起加强作用”为准，不完全沿用题库的考法标签。与题库标签差别较大的：2021GK-109（标签“搭桥”，官方答案是机理 C → 考法十）；2021SD-74（标签“补充论据”，官方答案有争议 → 考法十五讲评）；2024GK-112、2022GK-112（标签“搭桥”，官方按“话题一致、补充论据”解析 → 考法三）；2022GD-67、2022SD-68、2025JSA-97、2025GK-111、2021JSA-93（都靠比力度定答案 → 考法十五）；2025ZJA-105、2024ZJA-104、2024ZJA-107（设问变形 → 考法十四）；2023SZ-36（官方“必要条件＞补充论据” → 考法十措施组，按力度题讲）。')
w('')
w('### 5.2 自解答案（无官方答案的 7 道 2026 年真题）')
w('')
w('均为逻辑题，无数值计算；已逐题对照原卷截图核对题干和选项完整。')
w('')
w('| 真题 | 答案 | 排在 | 一句话思路 |')
w('|---|---|---|---|')
for s in SELF_SOLVED:
    w('| %s | %s | 第 %d 天 | %s |' % (s['id'], s['answer'], PLACE[s['id']][0], s['note']))
w('')
w('### 5.3 原“官方答案识别中”的 8 道：规划预判 vs 官方答案')
w('')
w('| 真题 | 现排 | 预判 | 官方 | 处理 |')
w('|---|---|---|---|---|')
for c in CHECKED:
    assert R[c['id']]['answer_official'] == c['official'], c['id']
    assert PLACE[c['id']][0] == c['day'], c['id']
    w('| %s | 第 %d 天 | %s | %s | %s |' % (c['id'], c['day'], c['pred'], c['official'], c['note']))
w('')
w('### 5.4 验算记录（Python 独立求解）')
w('')
w('形式搭桥题把题干条件写成命题（个体）或一元谓词（“所有/有的”），逐个把选项加进前提，用真值表或有限模型枚举检验结论是否必然成立；数据题从题面数字重新计算。脚本：`bp_L03_work/v2/verify_v2.py`。')
w('')
w('| 条目 | 结果 | 通过 |')
w('|---|---|---|')
for name, detail, ok in VER:
    w('| %s | %s | %s |' % (name, detail, '✓' if ok else '✗'))
w('')
w('### 5.5 问题清单（%d 条）' % len(ISSUES))
w('')
w('| 真题 | 处理 | 问题 |')
w('|---|---|---|')
for it in ISSUES:
    w('| %s | %s | %s |' % (it['id'], it['action'], it['problem']))
w('')
md = '\n'.join(L)
open(OUT_MD, 'w', encoding='utf-8').write(md)

# ------------------------------------------------------------------ report
print('md chars', len(md), '| json bytes', os.path.getsize(OUT_JSON))
for dd in J['days']:
    nr = sum(len(g['real']) for g in dd['groups'])
    nv = sum(v['n'] for g in dd['groups'] for v in g['variants'])
    print('day %d: real %d + variants %d = %d | answers %s' % (dd['day'], nr, nv, nr + nv, dict(sorted(DAYPOS[dd['day']]['all'].items()))))
print('kaofa', len(ORDER), '| issues', len(ISSUES), '| self_solved', len(SELF_SOLVED))
