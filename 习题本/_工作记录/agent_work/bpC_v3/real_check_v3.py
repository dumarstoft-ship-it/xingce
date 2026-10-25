# -*- coding: utf-8 -*-
"""v3 独立验算：5 道无官方答案真题自解 + 旧核对脚本未覆盖的真题 + 有疑点真题复核。"""
from lib import *

print('#' * 20, '自解（无官方答案）')
# ---- 2026GD-62：一排6座，1..6 从左到右（同一视角，右手边=编号更大）
N = ['教育', '住建', '交通', '农业', '人社', '财政']
base = line(N, 6, [lambda s: s['财政'] == s['人社'] + 1,            # 财政在人社右手边并相邻
                   lambda s: s['住建'] - s['财政'] >= 2,           # 财政在住建左手边但不相邻
                   lambda s: abs(s['教育'] - s['交通']) == 2])      # 教育与交通之间隔着一个
S = [s for s in base if abs(s['农业'] - s['财政']) == 1]
print('2026GD-62 基础解数', len(base), '附加后', [fmt_line(s) for s in S])
judge('2026GD-62', S, {'A': lambda s: 7 - s['教育'] == 3,   # 从右到左第三位 = 4号
                        'B': lambda s: 7 - s['住建'] == 2,   # 从右到左第二位 = 5号
                        'C': lambda s: s['交通'] == 3,
                        'D': lambda s: s['人社'] == 2}, 'must')

# ---- 2026ZJA-97
N = ['A', 'B', 'C', 'D', 'E', 'F']   # 甲:A,B 乙:C,D 丙:E,F
S = line(N, 6, [lambda s: abs(s['A'] - s['C']) != 1, lambda s: abs(s['F'] - s['C']) != 1,
                lambda s: [s['A'] in (1, 6), s['B'] in (1, 6)].count(True) == 1,
                lambda s: s['C'] == 2 and s['E'] == 4])
print('2026ZJA-97 解', [fmt_line(s) for s in S])
judge('2026ZJA-97', S, {'A': lambda s: s['B'] == 1, 'B': lambda s: s['B'] == 5,
                         'C': lambda s: s['D'] == 5, 'D': lambda s: s['D'] == 6}, 'possible')

# ---- 2026GK-110：7选4
P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = []
for c in combinations(P, 4):
    s = set(c)
    if '甲' in s and '丁' in s: continue
    if (s & {'丙', '戊'}) and not ('甲' in s and '己' not in s): continue
    if (s & {'乙', '庚'}) and not ('丁' in s and '甲' not in s): continue
    S.append(s)
print('2026GK-110 方案', [sorted(x) for x in S])
judge('2026GK-110', S, {'A': lambda s: {'乙', '庚'} <= s, 'B': lambda s: {'丙', '丁'} <= s,
                         'C': lambda s: {'己', '戊'} <= s, 'D': lambda s: {'甲', '乙'} <= s}, 'must')

# ---- 2026ZJA-98：一等1、二等2、三等3
P = ['琪琪', '依依', '冰冰', '鑫鑫', '磊磊', '静静']
S = []
for a in set(permutations([1, 2, 2, 3, 3, 3])):
    s = dict(zip(P, a))
    if not (s['琪琪'] == 2 or s['冰冰'] == 1): continue                       # 除非琪二，否则冰一
    if (s['琪琪'] == 2 or s['依依'] == 2) and not (s['鑫鑫'] == 3 and s['静静'] == 2): continue
    if s['鑫鑫'] == 3 and not (s['冰冰'] == 2 and s['依依'] != 3): continue
    S.append(s)
print('2026ZJA-98 解', S)
judge('2026ZJA-98', S, {'A': lambda s: s['冰冰'] != 1, 'B': lambda s: s['琪琪'] == 2,
                         'C': lambda s: s['鑫鑫'] != 1, 'D': lambda s: s['磊磊'] == 3}, 'must')

# ---- 2026GD-63：两种理解都验——(a)"相当"=收入相等（允许并列）；(b)"相当"不要求相等，只要求两村都不是最高
V = ['甲', '乙', '丙', '丁']; AW = ['文旅', '非遗', '生态', '数字']
def gd63(mode):
    out = []
    for a in permutations(AW):
        A = dict(zip(V, a)); W = {v: k for k, v in A.items()}
        rng = product(range(4), repeat=4) if mode == 'a' else permutations(range(4))
        for inc in rng:
            I = dict(zip(V, inc)); top = max(inc)
            if not I[W['文旅']] > I['丙']: continue
            if W['数字'] == '甲': continue                      # "甲村和数字农业示范村"是两个村
            if mode == 'a' and I['甲'] != I[W['数字']]: continue
            if I['甲'] == top or I[W['数字']] == top: continue
            if not I[W['生态']] > I['丁']: continue
            if not I['丙'] > I[W['非遗']]: continue
            out.append((A, I))
    return out
for mode in ('a', 'b'):
    S = gd63(mode)
    print(f'2026GD-63[{mode}] 获奖分配', sorted({tuple(x[0][v] for v in V) for x in S}))
    second_strict = lambda I, v: sum(I[u] > I[v] for u in V) == 1 and sum(I[u] == I[v] for u in V) == 1
    judge(f'2026GD-63[{mode}]', S, {'A': lambda x: second_strict(x[1], '甲'), 'B': lambda x: x[0]['乙'] == '文旅',
                                    'C': lambda x: x[0]['丙'] == '数字', 'D': lambda x: x[0]['丁'] == '非遗'}, 'must')
    # A 项若把"并列第二"也算作"位列第二"
    loose = lambda I, v: sum(I[u] > I[v] for u in V) == 1
    print('    A项(并列也算第二)是否必然:', all(loose(x[1], '甲') for x in S))

print('#' * 20, '旧脚本未覆盖的有官方答案真题')
# ---- 2022GD-62
cand7 = {'甲': '语文', '乙': '数学', '丙': '英语'}; cand8 = {'丁': '数学', '戊': '历史', '己': '语文'}
def ok62(team):
    g7 = [x for x in team if x in cand7]; g8 = [x for x in team if x in cand8]
    subj = [cand7.get(x) or cand8.get(x) for x in team]
    return len(g7) == 2 and len(g8) == 1 and len(set(subj)) == 3
opts = {'A': ['甲', '己', '戊'], 'B': ['甲', '乙', '己'], 'C': ['乙', '丙', '戊'], 'D': ['乙', '丙', '丁']}
good = [k for k, v in opts.items() if ok62(v)]
print('2022GD-62 符合要求的选项', good, '(官方 C)')
# ---- 2023GD-58
g1 = {'甲': '历史', '乙': '地理', '丙': '政治'}; g2 = {'丁': '地理', '戊': '语文'}; g3 = {'己': '政治', '庚': '数学'}
def ok58(team):
    c = [sum(x in g for x in team) for g in (g1, g2, g3)]
    subj = [{**g1, **g2, **g3}[x] for x in team]
    return c == [2, 1, 1] and len(set(subj)) == 4
opts = {'A': '甲乙丁庚', 'B': '甲乙戊己', 'C': '乙丙戊己', 'D': '乙戊己庚'}
print('2023GD-58 符合要求的选项', [k for k, v in opts.items() if ok58(list(v))], '(官方 B)')
# ---- 2023GD-56
P = ['甲', '乙', '丙', '张', '李', '王']; male = {'甲', '乙', '丙'}
S = []
for a in product('ABCD', repeat=6):
    s = dict(zip(P, a))
    if any(any(s[m] == c for m in male) and not any(s[f] == c for f in ('张', '李', '王')) for c in 'ABCD'): continue
    if s['张'] not in 'AB' or s['乙'] != 'D': continue
    if s['李'] != 'C': continue
    S.append(s)
judge('2023GD-56', S, {'A': lambda s: s['丙'] == 'A', 'B': lambda s: s['张'] == 'B',
                        'C': lambda s: s['甲'] == 'C', 'D': lambda s: s['王'] == 'D'}, 'must', 'D')
# ---- 2026CQ-100（遮挡处按"那么"补全；"只有丁去S"= 去S的恰为丁一人）
P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
S = []
for aw in product('PQRS', repeat=7):
    a = dict(zip(P, aw)); c = {k: aw.count(k) for k in 'PQRS'}
    if any(not (1 <= c[k] <= 3) for k in c) or c['Q'] != 3 or c['R'] != c['P']: continue
    if sum(a[x] == 'Q' for x in ('甲', '乙', '丙')) <= 2 and [x for x in P if a[x] == 'S'] != ['丁']: continue
    if (a['丁'] != 'S' or a['戊'] != 'S') and not (a['乙'] == 'S' and a['庚'] == 'S'): continue
    S.append(a)
print('2026CQ-100 解', S)
judge('2026CQ-100', S, {'A': lambda a: a['乙'] == 'Q' and a['戊'] == 'S', 'B': lambda a: a['甲'] == 'Q' and a['丁'] == 'P',
                         'C': lambda a: a['己'] == 'P' and a['庚'] == 'R', 'D': lambda a: a['丙'] == 'P' and a['戊'] == 'S'}, 'must', 'A')

print('#' * 20, '疑点复核')
# ---- 2024SC-85 闭世界（一等奖获得者的四项信息都在表中出现过的取值之内）vs 开放
tab = {'甲': ('赵', '男', '馆员', '借阅部'), '乙': ('钱', '女', '研究馆员', '咨询部'), '丙': ('孙', '男', '馆员', '借阅部'),
       '丁': ('李', '女', '研究馆员', '采编部'), '戊': ('钱', '女', '副研究馆员', '借阅部')}
for mode in ('闭世界', '职务与部门可在表外'):
    dims = [sorted({v[i] for v in tab.values()}) for i in range(4)]
    if mode != '闭世界':
        dims[2].append('表外职务'); dims[3].append('表外部门')
    S = [c for c in product(*dims) if all(sum(v[i] == c[i] for i in range(4)) == 1 for v in tab.values())]
    print('2024SC-85', mode, S)
# ---- 2020SZS-73 说谎人数
feas = {sum(c) for c in product([1, 3, 5, 7, 9], repeat=6)}
claims = [10, 30, 33, 58]
liars = sorted({sum(not t for t in tr) for tr in product([True, False], repeat=4)
                if all((not t) or (x in feas) for t, x in zip(tr, claims))})
print('2020SZS-73 可能的说谎人数', liars, '→ C(至少一人)、D(至少两人)都必然为真；官方取D（最强结论）')
# ---- 2023SZ-38 两种"相隔n天"口径
SH = ['篮', '滑', '牛', '凉', '拖']
for mode, g in (('日期差=n', lambda n: n), ('中间隔n天', lambda n: n + 1)):
    S = []
    for days in product(SH, repeat=7):
        b = [i for i in range(7) if days[i] == '篮']
        if len(b) != 2 or b[1] - b[0] != g(3): continue
        o = [i for i in range(7) if days[i] == '牛']
        if len(o) != 1 or abs(o[0] - b[0]) != 1: continue
        sk = [i for i in range(7) if days[i] == '滑']
        if len(sk) != 1 or not sk[0] < b[1]: continue
        sd = [i for i in range(7) if days[i] == '凉']
        if len(sd) < 1 or any(abs(x - b[0]) != g(4) for x in sd): continue
        if not any(days[i] == '拖' for i in range(b[0])): continue
        S.append(days)
    print('2023SZ-38', mode, '解数', len(S))
    judge('2023SZ-38[' + mode + ']', S, {'A': lambda d: d[0] == '篮', 'B': lambda d: d[2] == '牛',
                                         'C': lambda d: d[3] == '拖', 'D': lambda d: d[4] == '滑'}, 'must',
          'B' if mode == '中间隔n天' else None)
summary()
