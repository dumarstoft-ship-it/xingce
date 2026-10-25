# -*- coding: utf-8 -*-
"""第5天（C05 首次）改编骨架验算。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bpC_v2')
from lib import *
from itertools import permutations, product, combinations

# ---------- G1-a 一真两假 -> 一假两真：甲去宣传部；乙去组织部；丙不去组织部（只有一个是错的）
P = ['甲', '乙', '丙']; D = ['组织部', '宣传部', '统战部']
S = [dict(zip(P, p)) for p in permutations(D)]
S = [w for w in S if [w['甲'] == '宣传部', w['乙'] == '组织部', w['丙'] != '组织部'].count(False) == 1]
print('G1-a', S)
opts = {'A': ('宣传部', '组织部', '统战部'), 'B': ('统战部', '组织部', '宣传部'), 'C': ('组织部', '统战部', '宣传部'), 'D': ('统战部', '宣传部', '组织部')}
judge('D5-G1a', S, {k: (lambda w, v=v: tuple(w[x] for x in P) == v) for k, v in opts.items()}, 'must', 'B')

# ---------- G1-b 4人4岗，只有一句真：甲在综合岗；乙不在财务岗；丙不在人事岗；丁在信息岗 —— 问"可能是"（选项为完整方案）
P4 = ['甲', '乙', '丙', '丁']; J = ['综合', '财务', '人事', '信息']
S = [dict(zip(P4, p)) for p in permutations(J)]
S = [w for w in S if [w['甲'] == '综合', w['乙'] != '财务', w['丙'] != '人事', w['丁'] == '信息'].count(True) == 1]
print('G1-b 全部可能方案', [tuple(w[x] for x in P4) for w in S])
opts = {'A': ('综合', '信息', '人事', '财务'), 'B': ('人事', '财务', '信息', '综合'), 'C': ('信息', '财务', '人事', '综合'), 'D': ('财务', '综合', '人事', '信息')}
for k, v in opts.items():
    w = dict(zip(P4, v)); print('   ', k, v, '真话数', [w['甲'] == '综合', w['乙'] != '财务', w['丙'] != '人事', w['丁'] == '信息'].count(True))
judge('D5-G1b', S, {k: (lambda w, v=v: tuple(w[x] for x in P4) == v) for k, v in opts.items()}, 'possible', 'B')

# ---------- G1-c 先找矛盾：(1)甲在综合岗 (2)甲不在综合岗 (3)如果乙在财务岗，那么丙在人事岗 (4)丁在人事岗或信息岗；只有一句真
S = [dict(zip(P4, p)) for p in permutations(J)]
S = [w for w in S if [w['甲'] == '综合', w['甲'] != '综合', (w['乙'] != '财务') or (w['丙'] == '人事'), w['丁'] in ('人事', '信息')].count(True) == 1]
print('G1-c', S)
judge('D5-G1c', S, {'A': lambda w: w['甲'] == '综合', 'B': lambda w: w['丙'] == '信息', 'C': lambda w: w['丁'] == '人事', 'D': lambda w: w['乙'] == '人事'}, 'must', 'B')

# ---------- G1-d 真假+计数：3人3部门，猜测(1)甲去组织部(2)乙不去宣传部(3)丙不去组织部；恰有一句为真的方案数
S = [dict(zip(P, p)) for p in permutations(D)]
c1 = [w for w in S if [w['甲'] == '组织部', w['乙'] != '宣传部', w['丙'] != '组织部'].count(True) == 1]
c2 = [w for w in S if [w['甲'] == '组织部', w['乙'] != '宣传部', w['丙'] != '组织部'].count(True) == 2]
print('G1-d 恰1真', c1, '恰2真', len(c2))
count_options('D5-G1d', len(c1), {'A': 0, 'B': 1, 'C': 2, 'D': 3}, 'B')

# ---------- G2-a 每人恰对1句（名次一一对应）
P = ['甲', '乙', '丙']
W = [dict(zip(P, p)) for p in permutations([1, 2, 3])]
V = {'张': [lambda w: w['甲'] == 3, lambda w: w['乙'] != 3, lambda w: w['丙'] == 1],
     '李': [lambda w: w['甲'] != 1, lambda w: w['乙'] == 3, lambda w: w['丙'] != 2],
     '王': [lambda w: w['甲'] == 2, lambda w: w['乙'] == 1, lambda w: w['丙'] == 3]}
S = [w for w in W if all(sum(f(w) for f in fs) == 1 for fs in V.values())]
print('G2-a', S)
judge('D5-G2a', S, {'A': lambda w: w['甲'] == 1, 'B': lambda w: w['乙'] == 1, 'C': lambda w: w['丙'] == 2, 'D': lambda w: w['甲'] == 3}, 'must', 'A')

# ---------- G2-b 4观众预测4人名次：一人全错，其余各对一个 —— 问"全错的是谁"
P4 = ['甲', '乙', '丙', '丁']
VP = {'张': (3, 2, 4, 1), '王': (2, 3, 1, 4), '李': (4, 2, 3, 1), '赵': (3, 4, 1, 2)}
S = []
for p in permutations([1, 2, 3, 4]):
    c = {v: sum(p[i] == g[i] for i in range(4)) for v, g in VP.items()}
    if sorted(c.values()) == [0, 1, 1, 1]:
        S.append((p, [v for v in c if c[v] == 0][0]))
print('G2-b', S)
judge('D5-G2b', S, {k: (lambda s, v=v: s[1] == v) for k, v in zip('ABCD', ['张', '王', '李', '赵'])}, 'must', 'C')

# ---------- G2-c 复合判断各对一半（4位同事各说一句"X是A地人且学B专业"）
G = ['广东', '福建', '湖南']; M = ['法律', '经济', '中文']
W = [(dict(zip(P, g)), dict(zip(P, m))) for g in permutations(G) for m in permutations(M)]
ST = [('乙', '广东', '法律'), ('甲', '湖南', '中文'), ('丙', '广东', '经济'), ('甲', '湖南', '法律')]
S = [w for w in W if all((w[0][x] == g) + (w[1][x] == m) == 1 for x, g, m in ST)]
print('G2-c', S)
judge('D5-G2c', S, {'A': lambda w: w[1]['甲'] == '法律', 'B': lambda w: w[0]['乙'] == '福建', 'C': lambda w: w[1]['丙'] == '经济', 'D': lambda w: w[0]['乙'] == '广东'}, 'must', 'B')

# ---------- G3 一拖二：3社区各选派1人（党员/退役军人/志愿者，可重复）
U = ['A', 'B', 'C']; K = ['党员', '退役军人', '志愿者']
WW = [dict(zip(U, p)) for p in product(K, repeat=3)]
pred = [lambda w: (w['A'] != '志愿者') or w['B'] == '党员',      # ①只有B社区选派党员，A社区才选派志愿者
        lambda w: (w['A'] != '党员') or w['C'] == '退役军人',    # ②除非C社区选派退役军人，否则A社区不选派党员
        lambda w: (w['B'] == '志愿者') or w['C'] == '志愿者']    # ③如果B社区不选派志愿者，那么C社区选派志愿者
S = [w for w in WW if all(f(w) for f in pred)]
print('G3 符合预测的全部情况', [tuple(w.values()) for w in S])
# 小题1：三社区类别各不相同，哪种情况符合预测（选项两条事实）
S1 = [w for w in S if len(set(w.values())) == 3]
def fits(facts, pool):  # 选项描述的情况在 pool 中存在
    return any(all(w[u] == k for u, k in facts) for w in pool)
def realizable(facts):
    return any(all(w[u] == k for u, k in facts) and len(set(w.values())) == 3 for w in WW)
o1 = {'A': [('A', '志愿者'), ('B', '党员')], 'B': [('A', '党员'), ('C', '志愿者')], 'C': [('B', '党员'), ('C', '志愿者')], 'D': [('B', '退役军人'), ('C', '志愿者')]}
assert all(realizable(v) for v in o1.values())
r1 = {k: fits(v, S1) for k, v in o1.items()}
print('G3-小题1', r1); assert [k for k, v in r1.items() if v] == ['C']
# 小题2：如果C社区选派志愿者，以下哪种情况不符合预测
S2 = [w for w in S if w['C'] == '志愿者']
o2 = {'A': [('A', '退役军人')], 'B': [('B', '退役军人')], 'C': [('A', '党员')], 'D': [('A', '志愿者')]}
r2 = {k: not fits(v, S2) for k, v in o2.items()}
print('G3-小题2 不符合？', r2); assert [k for k, v in r2.items() if v] == ['C']
print('[OK] D5-G3a 一拖二：小题1->C，小题2->C')
# G3-b 深化：如果至少有两个社区选派的人员类别相同，以下哪项一定为真
S3 = [w for w in S if len(set(w.values())) < 3]
print('G3-b 情况', [tuple(w.values()) for w in S3])
judge('D5-G3b', S3, {'A': lambda w: w['A'] == '退役军人', 'B': lambda w: w['C'] == '志愿者',
                     'C': lambda w: (w['A'] == '退役军人') or (w['B'] == '党员'), 'D': lambda w: w['B'] != '党员'}, 'must', 'C')

# ---------- G3-c 拓展：4部门各录1人；应聘者博士2、硕士3、本科3（博士最多录2人）
DP = ['生产', '研发', '财务', '行政']; DEG = ['博士', '硕士', '本科']
WW = [dict(zip(DP, p)) for p in product(DEG, repeat=4)]
WW = [w for w in WW if list(w.values()).count('博士') <= 2 and list(w.values()).count('硕士') <= 3 and list(w.values()).count('本科') <= 3]
pred = [lambda w: (w['生产'] != '博士') or w['研发'] == '博士',          # ①如果生产部录用博士，那么研发部也录用博士
        lambda w: (w['行政'] != '硕士') or w['财务'] == '本科',          # ②只有财务部录用本科生，行政部才录用硕士
        lambda w: w['研发'] != w['行政']]                               # ③研发部和行政部录用的学历不同
S = [w for w in WW if all(f(w) for f in pred)]
print('G3-c 情况数', len(S))
judge('D5-G3c', S, {'A': lambda w: w['生产'] == '博士' and w['财务'] == '博士',
                    'B': lambda w: w['行政'] == '硕士' and w['财务'] == '硕士',
                    'C': lambda w: w['生产'] == '博士' and w['行政'] == '博士',
                    'D': lambda w: w['研发'] == '本科' and w['行政'] == '硕士' and w['生产'] == '硕士'}, 'possible', 'D')
