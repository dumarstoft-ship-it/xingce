# -*- coding: utf-8 -*-
"""生成 blueprints/L04.json 与 blueprints/L04.md（第 3—5 节由数据生成，第 0—2 节来自 head_v2.md）。
用法：python3 -I build_L04.py <scratchpad 根目录>"""
import json, re, sys, os, itertools, collections
from fractions import Fraction as F

ROOT = sys.argv[1]
WORK = os.path.join(ROOT, 'bp_L04_work')
sys.path.insert(0, WORK)
from data_days_a import DAY3, DAY11, DAY18
from data_days_b import DAY24, DAY31, DAY38

DAYS = [DAY3, DAY11, DAY18, DAY24, DAY31, DAY38]
TASK = json.load(open(os.path.join(ROOT, 'tasks_in', 'L04.json'), encoding='utf-8'))
REAL = {r['id']: r for r in TASK['real']}

KF_NAME = {1: '一 否定论点', 2: '二 措施类', 3: '三 他因', 4: '四 因果倒置', 5: '五 溯源', 6: '六 拆桥',
           7: '七 外推与类比', 8: '八 调查样本', 9: '九 实验设计', 10: '十 对照反例', 11: '十一 数据与比例',
           12: '十二 否定论据', 13: '十三 对象识别', 14: '十四 选非', 15: '十五 多项与力度'}
CN = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
      11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五'}
SEED_KF = {'考法' + v: k for k, v in CN.items()}

# 真题主考法归属（与第 1 节一致）
KF_REAL = {
 1: "2020ZJB-70 2022GK-107 2022JSA-94 2022SC1-77 2022ZJA-102 2023HB-105 2023JSA-92 2026ZJA-102 2020ZJB-68 2021JSA-96 2021SC2-81 2022SC1-78 2023GD-61 2023SD-71 2023ZJA-106 2024SC-80 2024SD-92 2024ZJA-105 2024ZJA-109 2024ZJA-110 2025HB-105 2020SC1206-80",
 2: "2020SZS-77 2021GK-106 2021SC2-79 2021SD-70 2021ZJA-114 2022JSA-101 2024GK-113 2024SD-98 2020SC1206-83 2022GD-74 2022SC2-79 2024ZJA-106 2025GK-108 2025HB-104 2025SC-81 2026GD-59",
 3: "2021GK-115 2021ZJA-108 2021ZJA-109 2022GK-114 2022ZJA-107 2023GK-112 2023HB-104 2023JSA-100 2025GK-114 2021SC2-77 2021SC2-82 2023SC-78 2023SD-72 2024GD-59 2024SC-83 2025SC-82 2025ZJA-110 2026GK-107 2020HB-105 2020SZ1-32 2020ZJB-67",
 4: "2020JSA-96 2020SC0725-79 2020ZJB-65 2022GD-72 2021SD-72",
 5: "2020SC0725-78 2020SC0725-84 2021GK-107 2023GK-108",
 6: "2020HB-101 2020SC0725-83 2023GD-70 2024GD-61 2021ZJA-107 2022SD-71 2022ZJA-104 2023SD-75 2025GD-63 2026ZJA-104",
 7: "2023GD-66 2024HB-110 2020HB-109",
 8: "2023SC-82 2024GK-107 2025GK-107",
 9: "2022SD-69 2024HB-107 2022SD-67 2023SC-83 2023SD-73 2025ZJA-108",
 10: "2022SD-73 2023SZ-45 2024SC-78 2024ZJA-108",
 11: "2023SD-69",
 12: "2020SD-70 2021SC2-78 2021SD-67 2023HB-107 2023SZ-42 2024HB-109 2025SC-79",
 13: "2020ZJB-62 2021ZJA-110 2025GD-65 2025SC-78 2024JSA-100 2025JSA-98 2024SZ-37",
 14: "2021ZJA-112 2021ZJA-113 2022SC2-81 2022SD-70 2024GK-111 2025SC-83 2020SC1206-77 2021JSA-95 2022SC1-80 2022SC2-82 2023GK-107 2025HB-103 2025ZJA-107 2026GK-113 2026GK-114 2026ZJA-100",
 15: "2022GK-115 2023SC-77 2020JSA-98 2023SD-74 2020SD-75",
}
KF_REAL = {k: v.split() for k, v in KF_REAL.items()}
REAL_KF = {i: k for k, v in KF_REAL.items() for i in v}

SELF_SOLVED = [
 {"id": "2026ZJA-102", "answer": "A", "note": "论点“跨境文物追索几乎是不可能完成的任务”是全称断言，A 指出国际公约之外还可通过条约、协议等途径追索，直接推翻“几乎不可能”；B 讲流失根源、C 讲公约局限（偏加强）、D 讲走私规模，都不削弱。"},
 {"id": "2026GD-59", "answer": "C", "note": "结论是“组建新团队时只考虑新手”；C 说明突破性设想都要经验丰富的研发人员改进才能实现，老手不可或缺，直接推翻“只考虑新手”；A 成果转化、B 薪资吸引力、D 培养成本都与“是否只要新手”无关或很弱。"},
 {"id": "2026GK-107", "answer": "C", "note": "学者观点是“现代陆地生态的复杂性是白垩纪协同机制延续演化的结果”；C 指出现代复杂性主要由随机扰动、自组织和外源干扰决定，与白垩纪显著不同（另有成因）；A 陆地系统相对稳定、B 各要素同期演化都偏加强，D 只说被子植物作用“可能被高估”，不明确。"},
 {"id": "2026GK-113", "answer": "C", "note": "观点是“居住空间受限是更倾向养猫的主要原因”；A 养狗易扰邻有危险、B 猫不需遛不需大量陪伴、D 养猫开支低，都是他因，能削弱；C 讲的是养猫之后拓展了社交圈，是结果而非选择原因，不能削弱。"},
 {"id": "2026GK-114", "answer": "C", "note": "结论只针对数学学习；A 未做使用培训（结果不能代表正确使用）、B 基础水平等变量未控制、D 时长不足以说明长期效果，都能削弱；C 说的是其他学科，超出结论范围，不能削弱。A 是近似干扰项，解析要说明它指向“使用方式”这一他因。"},
 {"id": "2026ZJA-100", "answer": "D", "note": "自媒体说“恰好 12 行是非转基因、多于 12 行是转基因”；A 技术上难以改变穗行数、B 转入基因不影响外观、C 同一品种不同单株穗行数也有波动，都能反驳；D 只说明穗行数总是双数，14、16 行仍是双数，不触及 12 行与多于 12 行的区分，不能反驳。"},
 {"id": "2026ZJA-104", "answer": "B", "note": "论据是“摄入过多蛋白质会伤肾”，论点是“健身人群长期喝蛋白粉会伤肾”；B 指出运动后肌纤维修复需要更多蛋白质，健身人群补充的并不“过多”，拆掉论据与论点的桥；A 其他病因不否定蛋白粉的风险，C 讲全国人均、对象不符，D 说蛋白粉与其他蛋白来源无区别，不涉及是否过量。"},
]

ISSUES = [
 {"id": "2021GK-107", "problem": "截图和提取文字都混入了下一题（第 108 题）的问句“根据以上陈述，以下哪项不可能？”及 4 个选项（小赵、小刘……），截图中位于灰色条带以下。排版时请把截图裁到灰色条带以上、文字删去最后 3 行。官方答案仍在识别中；本题按溯源题（胶原蛋白促进表皮干细胞更新）排在第 31 天。"},
 {"id": "2020HB-109", "problem": "官方答案 D（正确率 25%）存疑：官方以“B 说的是喜马拉雅山其他地方，论题不一致”排除 B，但论点“该地区的冰川最终将消失殆尽”本身就包括喜马拉雅山其他地方，B“对气温变化不敏感”同样有削弱力。D 的优势在于直接针对珠峰本身、且是事实陈述，B 的“不敏感”是程度判断。建议保留（排第 38 天），解析里正面比较 B、D，不要沿用官方“论题不一致”的说法；如要求一题一解更严格，可改作讲评题。"},
 {"id": "2020SD-75", "problem": "题库备注“答案有争议”。复核结论：官方答案 A 成立——D“新款涨价”说明消费者因价格选择旧款，恰恰说明价格比续航更受重视，反而支持“续航不是首要因素”。保留使用（第 38 天力度组），解析必须专门讲 D 为什么不削弱。"},
 {"id": "2020SC1206-80", "problem": "答案 B 无误；但官方解析把 A（理论上需连续两个月每天喝 1 斤葡萄酒）判为“加强”不妥。A 属于“剂量难以达到”的弱削弱（与 2022SD-67 B 同类），B 直接否定论点、力度更强。使用官方解析时请改写对 A 的定性。"},
 {"id": "2022SC1-78", "problem": "截图底部带出下一题的半行文字，需裁掉。官方答案仍在识别中；B（单一分数标准不能满足人才需要）与 D（个别高分孩子走上犯罪道路）都有削弱力，答案回来后请核对：若为 D，解析要说明“只要……就是最好的教育”是充分条件断言、一个反例即可推翻；若为 B，要说明 D 的“个别”且话题偏到品德，力度不足。"},
 {"id": "2020SZS-77", "problem": "答案 C 无误；官方解析把论点误写成“基因编辑婴儿已健康出生”，实际论点是“编辑这段基因后人体可以免疫流感”。引用官方解析时请改正论点。"},
 {"id": "2021SC2-77", "problem": "提取文字末尾混入页脚“第13页，共18页”，排版用文字时删除；截图正常，题目本身可用。"},
 {"id": "2024SZ-37", "problem": "提取文字里 B、C 两项挤在同一行（“……生活性功能C.在城市发展农业……”），排版用文字时拆开；截图本身是原卷排版，可用。"},
 {"id": "2024ZJA-110", "problem": "官方解析文字中混入水印“淘宝：罗老师的资料铺子 37”，引用解析时删除。"},
 {"id": "2020SC0725-83", "problem": "官方解析有错字（“锯齿鲨”应为“巨齿鲨”，“缺少事物”应为“缺少食物”），引用时改正；答案 C 无误。"},
]

# ---------------------------------------------------------------- 校验
LOG = []
def ok(name, cond, info=''):
    LOG.append(('OK  ' if cond else 'FAIL') + ' ' + name + ((' — ' + info) if info else ''))
    if not cond:
        print('FAIL', name, info)
    return cond

all_ok = True
# 1. 真题不重不漏
alld = [i for d in DAYS for g in d['groups'] for i in g['real']]
all_ok &= ok('真题总数 130', len(alld) == 130, str(len(alld)))
all_ok &= ok('真题不重复', len(set(alld)) == len(alld))
all_ok &= ok('真题不漏（与任务清单一致）', set(alld) == set(REAL), 'missing=%s extra=%s' % (sorted(set(REAL) - set(alld)), sorted(set(alld) - set(REAL))))
all_ok &= ok('主考法归属覆盖 130 道', set(REAL_KF) == set(REAL) and sum(len(v) for v in KF_REAL.values()) == 130)
all_ok &= ok('天数与任务一致', [d['day'] for d in DAYS] == TASK['days'], str([d['day'] for d in DAYS]))

LETTERS = collections.OrderedDict()
DIRS = collections.OrderedDict()
VKF = collections.Counter()
for d in DAYS:
    nreal = sum(len(g['real']) for g in d['groups'])
    nvar = sum(v['n'] for g in d['groups'] for v in g['variants'])
    all_ok &= ok('第 %d 天 真题+改编=45' % d['day'], nreal + nvar == 45, '%d+%d' % (nreal, nvar))
    lc = collections.Counter(); dc = collections.Counter()
    for gi, g in enumerate(d['groups']):
        all_ok &= ok('第 %d 天 第 %d 组有标题' % (d['day'], gi + 1), bool(g['title'].strip()))
        seq = []
        for i in g['real']:
            a = REAL[i]['answer_official']
            if a is None:
                a = {s['id']: s['answer'] for s in SELF_SOLVED}.get(i, '?')
            seq.append(a)
        for v in g['variants']:
            all_ok &= ok('方向合法', v['direction'] in ('巩固', '深化', '拓展'), v['direction'])
            sd = v['seed']
            all_ok &= ok('种子合法 %s' % sd, sd in REAL or sd in SEED_KF, sd)
            if sd in SEED_KF:
                all_ok &= ok('考法种子与 kf 一致 %s' % sd, SEED_KF[sd] == v['kf'], '%s vs %s' % (sd, v['kf']))
            dc[v['direction']] += v['n']
            VKF[v['kf']] += v['n']
            letters = re.findall(r'【(?:第 \d 问)?正确项 ([ABCD])', v['idea'])
            all_ok &= ok('正确项个数=n', len(letters) == v['n'], '%s %s' % (letters, v['idea'][:30]))
            for L in letters:
                lc[L] += 1; seq.append(L)
            # 单选题：其余三个字母都要出现在干扰项 / 能削弱的三项里
            if v['n'] == 1 and '①' not in v['idea']:
                rest = v['idea'].split('【正确项')[1]
                others = [x for x in 'ABCD' if x != letters[0]]
                miss = [x for x in others if not re.search(r'(】|；|，)\s*' + x + r' ', rest)]
                all_ok &= ok('干扰项字母齐全', not miss, '%s 缺 %s' % (v['idea'][:24], miss))
        # 组内（含真题）不出现连续三个相同答案
        run = max((len(list(gr)) for k, gr in itertools.groupby(seq) if k != '?'), default=0)
        all_ok &= ok('第 %d 天 第 %d 组没有连续三题同一答案' % (d['day'], gi + 1), run < 3, ''.join(seq))
    LETTERS[d['day']] = lc; DIRS[d['day']] = dc
    all_ok &= ok('第 %d 天 改编答案大致均衡（各字母 ≤ 改编数/4+3）' % d['day'], max(lc.values()) <= nvar / 4 + 3 and min(lc.get(x, 0) for x in 'ABCD') >= nvar / 4 - 3, dict(sorted(lc.items())).__str__())

all_ok &= ok('改编总数 140', sum(VKF.values()) == 140, str(sum(VKF.values())))
all_ok &= ok('第 38 天没有巩固题', DIRS[38]['巩固'] == 0)
all_ok &= ok('自解 7 道与任务一致', {s['id'] for s in SELF_SOLVED} == {i for i, r in REAL.items() if r['needs_self_solve']})
all_ok &= ok('问题清单 id 都在本模块', all(x['id'] in REAL for x in ISSUES))

# 2. 改编里出现的数字（全部从题面数据出发重算）
NUM = []
def num(name, cond, info=''):
    NUM.append(('OK  ' if cond else 'FAIL') + ' ' + name + ((' — ' + info) if info else ''))
    return cond
n_ok = True
r0, r1 = F(600, 6), F(720, 8)
n_ok &= num('D3 延时服务：每小时办件 100→90，降 10%；总量升 20%', (r0, r1) == (100, 90) and (r1 - r0) / r0 == F(-1, 10) and F(720, 600) == F(6, 5))
n_ok &= num('D3 借阅：前年 60 万册次降 30% 即减少 18 万', 60 * F(3, 10) == 18 and 50 > 18)
n_ok &= num('D11 浓缩洗衣液：单次花费 = 4×1/2 = 2 倍', 4 * F(1, 2) == 2)
h = F(1)  # 前年上、下半年各 1
n_ok &= num('D11 积分制：上半年降 20%、下半年降 24%、半年基数相同 → 全年降 22%', 1 - (h * F(8, 10) + h * F(76, 100)) / (2 * h) == F(22, 100))
young, old = F(70, 80), F(30, 20)
n_ok &= num('D11 年轻干部：资深干部人均做法是年轻干部的约 1.7 倍', abs(float(old / young) - 1.714) < 0.01, '%.3f' % float(old / young))
n_ok &= num('D11 快递：甲单位业务量投诉为其余公司的约 78%', abs(float(F(70, 75) / F(30, 25)) - 0.78) < 0.005, '%.4f' % float(F(70, 75) / F(30, 25)))
n_ok &= num('D11 城乡事故：按里程折算城市事故率是农村的 1/2', F(4, 8) == F(1, 2))
n_ok &= num('D18 钙片：600+400=1000 < 2000', 600 + 400 == 1000 < 2000)
n_ok &= num('D18 增长率×基数：乙新增是甲的 3 倍', (15 * F(1, 10)) / (1 * F(1, 2)) == 3)
ja = F(60, 100) * F(84, 100) + F(40, 100) * F(99, 100)
yi = F(10, 100) * F(68, 100) + F(90, 100) * F(98, 100)
n_ok &= num('D18 辛普森：甲总体 90%、乙 95%，分层甲两层都更高', ja == F(9, 10) and yi == F(95, 100) and F(84, 100) > F(68, 100) and F(99, 100) > F(98, 100), '甲 %s 乙 %s' % (ja, yi))
n_ok &= num('D18 相对风险：十万分之一×3 = 十万分之三', F(1, 100000) * 3 == F(3, 100000))
tot = 500 * 32  # 万元
rest = F(tot - 11200, 495)
n_ok &= num('D24 收入：总 1.6 亿，5 户 1.12 亿，其余户均约 9.7 万 < 10 万，低于全市平均 16 万', tot == 16000 and rest < 10 and rest < 16 and F(32, 2) == 16, '%.2f 万' % float(rest))
part, full = 3 * F(1, 2), F(1)
n_ok &= num('D24 骑手：兼职接单占 60% = 投诉占比', part / (part + full) == F(3, 5))
n_ok &= num('D24 儿科：40 名医生/90 个中心 < 0.5', F(40, 90) < F(1, 2))
n_ok &= num('D24 均值回归：90→60 降三分之一，60 在 57—63', F(90 - 60, 90) == F(1, 3) and 57 <= 60 <= 63)
n_ok &= num('D31 辣椒酱：15 克×3 倍 = 45 克苹果当量 < 200 克的四分之一', 15 * 3 == 45 and F(45, 200) < F(1, 4))
n_ok &= num('D31 共享单车：每万人次事故 24 对 6，是 4 倍', F(240, 10) == 24 and F(600, 100) == 6 and F(240, 10) / F(600, 100) == 4)
n_ok &= num('D38 抽检：5/50 = 1/10，漏检 90%', F(5, 50) == F(1, 10) and 1 - F(5, 50) == F(9, 10))
n_ok &= num('D38 专精特新：乙区培育率是甲区的 2 倍', (F(10, 100) / 1) / (F(40, 100) / 8) == 2)
n_ok &= num('D38 人均绿地：15×20% = 3', 15 * F(20, 100) == 3)
n_ok &= num('D38 招商：60 亿 = 甲团队 15 亿的 4 倍', F(60, 4) == 15)
n_ok &= num('D38 门票：最多 8000×60=48 万 < 7500×100=75 万；若真能翻番为 90 万', 8000 * 60 == 480000 < 750000 == 7500 * 100 and 15000 * 60 == 900000)
n_ok &= num('D38 毕业生问卷：1200/5000 = 24% < 1/4', F(1200, 5000) == F(24, 100) < F(1, 4))
# 3. 真值表：“只要 P 且 Q 就 R”只被 (P,Q,¬R) 推翻
contra = [(p, q, r) for p, q, r in itertools.product([1, 0], repeat=3) if not ((not (p and q)) or r)]
optA, optB, optC = (1, 1, 0), (0, 1, 0), (1, 0, 1)
n_ok &= num('D31 凉茶铺真值表：唯一矛盾情形是“有招牌、在地铁口、不兴隆”；B、C 两种情形与论点相容', contra == [(1, 1, 0)] and optA in contra and optB not in contra and optC not in contra, str(contra))
all_ok &= ok('改编中的数字与真值表全部验算通过（%d 项）' % len(NUM), n_ok)

# ---------------------------------------------------------------- 输出 JSON
out = {"module": "L04", "days": [], "self_solved": SELF_SOLVED, "issues": ISSUES}
for d in DAYS:
    out['days'].append({"day": d['day'], "groups": [
        {"title": g['title'], "real": list(g['real']),
         "variants": [{"n": v['n'], "direction": v['direction'], "seed": v['seed'], "idea": v['idea']} for v in g['variants']]}
        for g in d['groups']]})
jpath = os.path.join(ROOT, 'blueprints', 'L04.json')
json.dump(out, open(jpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- 输出 Markdown（第 3—5 节）
def ans_tag(i):
    r = REAL[i]
    if r['answer_official']:
        return '%s，难度 %d' % (r['answer_official'], r['difficulty'])
    if r['needs_self_solve']:
        return '自解 %s，难度 %d' % ({s['id']: s['answer'] for s in SELF_SOLVED}[i], r['difficulty'])
    return '答案待识别，难度 %d' % r['difficulty']

ORD = ['第 1 次', '第 2 次', '第 3 次', '第 4 次', '第 5 次', '第 6 次']
md = []
md.append('## 3. 各天配置\n')
md.append('### 3.0 六天总表\n')
md.append('| 天 | 次序 | 真题 | 改编 | 改编方向（巩固 / 深化 / 拓展） | 真题难度（1 / 2 / 3） | 组数 | 改编答案（A / B / C / D） |')
md.append('|---|---|---|---|---|---|---|---|')
for k, d in enumerate(DAYS):
    ids = [i for g in d['groups'] for i in g['real']]
    dif = collections.Counter(REAL[i]['difficulty'] for i in ids)
    nvar = sum(v['n'] for g in d['groups'] for v in g['variants'])
    dc = DIRS[d['day']]; lc = LETTERS[d['day']]
    md.append('| 第 %d 天 | %s | %d | %d | %d / %d / %d | %d / %d / %d | %d | %d / %d / %d / %d |' % (
        d['day'], ORD[k], len(ids), nvar, dc['巩固'], dc['深化'], dc['拓展'], dif[1], dif[2], dif[3], len(d['groups']),
        lc['A'], lc['B'], lc['C'], lc['D']))
tot_dir = collections.Counter()
for dc in DIRS.values(): tot_dir.update(dc)
md.append('| 合计 | | 130 | 140 | %d / %d / %d | 48 / 76 / 6 | | |' % (tot_dir['巩固'], tot_dir['深化'], tot_dir['拓展']))
md.append('')
md.append('排法说明：')
md.append('1. 难度前易后难：第 3 天 26 道真题全是难度 1；第 11 天以难度 1 为主；第 18—31 天以难度 2 为主；6 道难度 3 的高错题全部放在第 38 天。')
md.append('2. 考法逐步铺开：第 3 天只练 6 个核心考法；第 11 天加入溯源、调查样本、对象识别、数据陷阱；第 18 天加入实验设计、对照反例、否定论据；第 24 天加入外推与类比、多项与力度。15 个考法到第 24 天全部出现过，之后每次都回炉。')
gd = collections.OrderedDict((d['day'], [i for g in d['groups'] for i in g['real'] if 'GD-' in i]) for d in DAYS)
gd = {k: v for k, v in gd.items() if v}
md.append('3. 广东真题 10 道分散在 %d 天里（%s），2026GD-59 放在第 11 天，尽早见到最新考法；第 18、38 天没有广东真题，用广东情境的改编补（回南天、广州冬季续航、荔枝台风等）。' % (len(gd), '、'.join('第 %d 天 %d 道' % (k, len(v)) for k, v in gd.items())))
md.append('4. 每组先真题后改编；改编的种子优先用同组真题，题库缺的考法用“考法 X”作种子。第 24、31、38 天末尾的“综合辨识（混编）”组不按考法排，每题考法不同，idea 开头的〔〕标签只供答案页使用。')
md.append('5. 每天的改编答案字母大致各占四分之一；校验程序同时检查了组内（含真题）没有连续三题同一答案。')
md.append('')

for k, d in enumerate(DAYS):
    ids = [i for g in d['groups'] for i in g['real']]
    dif = collections.Counter(REAL[i]['difficulty'] for i in ids)
    nvar = sum(v['n'] for g in d['groups'] for v in g['variants'])
    dc = DIRS[d['day']]; lc = LETTERS[d['day']]
    kfc = collections.Counter()
    for g in d['groups']:
        for v in g['variants']:
            kfc[v['kf']] += v['n']
    md.append('### 3.%d 第 %d 天（%s出现%s）\n' % (k + 1, d['day'], ORD[k], '｜试点日，idea 写到可直接出题' if k == 0 else ''))
    md.append('- **配置**：真题 %d 道＋改编 %d 道＝45；改编方向：巩固 %d、深化 %d、拓展 %d；真题难度：%s。' % (
        len(ids), nvar, dc['巩固'], dc['深化'], dc['拓展'],
        '、'.join('%d 级 %d 道' % (x, dif[x]) for x in (1, 2, 3) if dif[x])))
    md.append('- **主题**：%s' % d['theme'])
    md.append('- **用时**：%s' % d['timing'])
    md.append('- **改编的考法分布**：%s。' % '、'.join('%s %d' % (CN[x], kfc[x]) for x in sorted(kfc)))
    md.append('- **改编答案分布**：A %d、B %d、C %d、D %d。' % (lc['A'], lc['B'], lc['C'], lc['D']))
    md.append('')
    for gi, g in enumerate(d['groups']):
        md.append('#### 第 %d 组　%s\n' % (gi + 1, g['title']))
        if g['real']:
            md.append('- 真题（%d 道，按此顺序）：%s' % (len(g['real']), ' → '.join('%s（%s）' % (i, ans_tag(i)) for i in g['real'])))
        else:
            md.append('- 真题：无（本组全部为改编）')
        nv = sum(v['n'] for v in g['variants'])
        md.append('- 改编（%d 道）：' % nv)
        for vi, v in enumerate(g['variants']):
            md.append('  %d. 〔%s｜种子 %s｜%d 道〕%s' % (vi + 1, v['direction'], v['seed'], v['n'], v['idea']))
        md.append('')

md.append('## 4. 真题核查\n')
md.append('### 4.1 问题清单（%d 条）\n' % len(ISSUES))
md.append('没有发现应归入其他模块的题：130 道的设问全是削弱、质疑、反驳、驳斥、缓解担忧或削弱选非，均属 L04。下面是答案存疑和截图、文字残缺的条目，都可以继续使用，按“处理建议”办即可。\n')
md.append('| 题号 | 所在天 | 问题与处理建议 |')
md.append('|---|---|---|')
DAY_OF = {i: d['day'] for d in DAYS for g in d['groups'] for i in g['real']}
for x in ISSUES:
    md.append('| %s | 第 %d 天 | %s |' % (x['id'], DAY_OF[x['id']], x['problem']))
md.append('')
md.append('### 4.2 自解答案（7 道没有官方答案的真题）\n')
md.append('7 道都是逻辑题，不涉及计算，无需程序验算；结论是逐项判定四个选项“削 / 不削”后得出的，四个选项中恰好一个符合设问。\n')
md.append('| 题号 | 所在天 | 答案 | 一句话思路 |')
md.append('|---|---|---|---|')
for s in SELF_SOLVED:
    md.append('| %s | 第 %d 天 | %s | %s |' % (s['id'], DAY_OF[s['id']], s['answer'], s['note']))
md.append('')
md.append('### 4.3 其他说明\n')
pend = [i for i, r in REAL.items() if r['answer_pending_ocr']]
md.append('1. **官方答案识别中的 11 道**（不在本任务中解答，已按题意归考法排入）：%s。答案回来后请顺带核对 4.1 中 2022SC1-78 的 B / D 之争。' % '、'.join('%s（第 %d 天）' % (i, DAY_OF[i]) for i in sorted(pend)))
nojx = sorted(i for i, r in REAL.items() if not r['j_crop'])
md.append('2. **没有官方解析截图的 %d 道**（上面 11 道＋7 道自解）：%s。解析需按 common.md 的统一风格自写；其中 2023SZ-42、2023SZ-45 的难度是估计值。' % (len(nojx), '、'.join(nojx)))
md.append('3. **2022ZJA-102、2022ZJA-104** 分别与 2022 年河北卷第 105、103 题同题；题库的 `db/schedule.json` 已把河北版并入浙江版（2022HB-105→2022ZJA-102，2022HB-103→2022ZJA-104），不会重复出现。')
md.append('4. **后补真题的替换规则**（2021 广东县级/乡镇卷、2021 四川和河北、2022 深圳、2026 贵州和河北联考）：新真题先按第 1 节归考法，再放进第 18—38 天同考法的组里，每进 1 道真题就删掉同组 1 道改编，优先删“巩固”、其次删与新真题情境最接近的那道；题库缺的考法（七类比、八、九的题库缺子类、十一）里的拓展题尽量保留。如果某组改编删光，就把新真题放进当天“综合辨识（混编）”组前面。第 3 天（试点日）不动。')
md.append('')

md.append('## 5. 校验记录\n')
md.append('由 `bp_L04_work/build_L04.py` 生成 JSON 和本文件第 3—5 节时自动校验，结果如下：\n')
md.append('- 结构校验：%s' % ('全部通过' if all_ok else '有失败项'))
summ = [l for l in LOG if 'FAIL' in l] or [
    'JSON 可读；每天真题＋改编＝45（第 3、11、18、24、31、38 天分别为 26+19、25+20、23+22、22+23、20+25、14+31）；',
    '130 道真题每道恰好出现一次，与任务清单一致；140 道改编的方向、种子、正确项字母、干扰项字母齐全；',
    '每组（含真题）没有连续三题同一答案；第 38 天没有巩固题；7 道自解与任务清单一致；问题清单的题号都在本模块。']
for l in summ:
    md.append('  - ' + l)
md.append('- 数字与真值表验算（%d 项，全部从题面数据重算）：' % len(NUM))
for l in NUM:
    md.append('  - ' + l)
md.append('')

head = open(os.path.join(WORK, 'head_v2.md'), encoding='utf-8').read()
dist = '改编 140 道的考法分布：%s。' % '、'.join('%s %d' % (CN[x], VKF[x]) for x in sorted(VKF))
head = head.replace('{{VARIANT_DIST}}', dist)
assert '{{' not in head
mpath = os.path.join(ROOT, 'blueprints', 'L04.md')
open(mpath, 'w', encoding='utf-8').write(head.rstrip() + '\n\n' + '\n'.join(md))

print('ALL OK' if all_ok else 'SOME FAILED')
print('variants by kf:', dict(sorted(VKF.items())))
print('dirs:', {k: dict(v) for k, v in DIRS.items()})
print('letters:', {k: dict(sorted(v.items())) for k, v in LETTERS.items()})
print('wrote', jpath, os.path.getsize(jpath), 'bytes;', mpath, os.path.getsize(mpath), 'bytes')
