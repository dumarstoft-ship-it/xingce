# -*- coding: utf-8 -*-
"""第4天（C04 首次）改编骨架验算。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bpC_v2')
from lib import *
from itertools import permutations, product, combinations

R = range(1, 13)
# ---------- G1-a A+B=C+D, A+C>B+D, A+D>B+C（门店利润）
S = [v for v in product(R, repeat=4) if v[0] + v[1] == v[2] + v[3] and v[0] + v[2] > v[1] + v[3] and v[0] + v[3] > v[1] + v[2]]
A, B, C, D = 0, 1, 2, 3
judge('D4-G1a', S, {'A': lambda v: v[C] > v[D], 'B': lambda v: v[A] > max(v[B], v[C], v[D]) and v[B] < min(v[C], v[D]),
                    'C': lambda v: v[B] > v[D], 'D': lambda v: v[A] + v[D] > 2 * v[C]}, 'must', 'B')

# ---------- G1-b 反向：不能推出（甲+乙>丙+丁；甲+丁=乙+丙；丙>丁）
S = [v for v in product(R, repeat=4) if v[0] + v[1] > v[2] + v[3] and v[0] + v[3] == v[1] + v[2] and v[2] > v[3]]
J, Y, B_, D_ = 0, 1, 2, 3
for a, b in permutations(range(4), 2):
    if all(v[a] > v[b] for v in S): print('   G1-b 可推出', '甲乙丙丁'[a], '>', '甲乙丙丁'[b])
judge('D4-G1b', S, {'A': lambda v: v[J] > v[B_], 'B': lambda v: v[J] > v[D_], 'C': lambda v: v[Y] > v[D_], 'D': lambda v: v[Y] > v[B_]}, 'notmust', 'D')

# ---------- G1-c 甲−乙>丙−丁；乙+丁>甲+丙
S = [v for v in product(R, repeat=4) if v[0] - v[1] > v[2] - v[3] and v[1] + v[3] > v[0] + v[2]]
judge('D4-G1c', S, {'A': lambda v: v[3] > v[2], 'B': lambda v: v[0] > v[1], 'C': lambda v: v[1] > v[0], 'D': lambda v: v[0] > v[2]}, 'must', 'A')

# ---------- G1-d 天平：A+B 与 C+D 平衡；A+C 比 B+D 重；B+C 比 A+D 重；E 比 C 轻（问最重）
S = [v for v in product(R, repeat=5) if v[0] + v[1] == v[2] + v[3] and v[0] + v[2] > v[1] + v[3] and v[1] + v[2] > v[0] + v[3] and v[4] < v[2]]
heav = lambda v, i: all(v[i] > v[j] for j in range(5) if j != i)
print('G1-d 可推出的两两关系', [f"{'ABCDE'[a]}>{'ABCDE'[b]}" for a, b in permutations(range(5), 2) if all(v[a] > v[b] for v in S)])
judge('D4-G1d', S, {k: (lambda v, i=i: heav(v, i)) for k, i in zip('ABCD', [0, 1, 2, 3])}, 'must', 'C')

# ---------- G1-e 和差等式：甲+乙比丙+丁多20；甲+丁=乙+丙；丁=30 -> 乙
S = [v for v in product(range(0, 101), repeat=3) if v[0] + v[1] - (v[2] + 30) == 20 and v[0] + 30 == v[1] + v[2]]
print('G1-e 乙的取值', sorted({v[1] for v in S}))
count_options('D4-G1e', S[0][1], {'A': 30, 'B': 40, 'C': 50, 'D': 60}, 'B')

# ---------- G2-a 交叉分类（已知/所求互换）：已知 本地生源医生总数少于外地；补哪项可推出 女>男
#   a=本地女 b=本地男 c=外地女 d=外地男
W = [v for v in product(range(0, 8), repeat=4) if v[0] + v[1] < v[2] + v[3]]
concl = lambda v: v[0] + v[2] > v[1] + v[3]
opts = {'A': lambda v: v[0] > v[3], 'B': lambda v: v[1] > v[2], 'C': lambda v: v[2] > v[1], 'D': lambda v: v[3] > v[0]}
res = {k: all(concl(v) for v in W if f(v)) for k, f in opts.items()}
print('G2-a 补充后结论必然成立？', res)
assert [k for k, v in res.items() if v] in (['A'], ['C']) and sum(res.values()) == 1, res

# ---------- G2-b 选非：以下哪项不能使"女>男"成立（已知 本地女 > 外地男）
W = [v for v in product(range(0, 8), repeat=4) if v[0] > v[3]]
opts = {'A': lambda v: v[0] + v[1] < v[2] + v[3], 'B': lambda v: v[0] + v[1] == v[2] + v[3], 'C': lambda v: v[2] >= v[1], 'D': lambda v: v[0] + v[1] > v[2] + v[3]}
res = {k: all(concl(v) for v in W if f(v)) for k, f in opts.items()}
print('G2-b 能保证结论？', res)
assert [k for k, v in res.items() if not v] == ['D'], res
print('[OK] D4-G2b -> D（"本地多于外地"不能保证）')

# ---------- G2-c 车间×用工：已知 一车间临时工多于二车间正式工；补哪项可推出 临时工总数多于正式工
#   a=一临 b=一正 c=二临 d=二正
W = [v for v in product(range(0, 8), repeat=4) if v[0] > v[3]]
concl2 = lambda v: v[0] + v[2] > v[1] + v[3]
opts = {'A': lambda v: v[0] + v[1] > v[2] + v[3], 'B': lambda v: v[0] + v[1] == v[2] + v[3], 'C': lambda v: v[1] > v[2], 'D': lambda v: v[3] < v[1]}
res = {k: all(concl2(v) for v in W if f(v)) for k, f in opts.items()}
print('G2-c 补充后结论必然成立？', res)
assert [k for k, v in res.items() if v] == ['B'], res
print('[OK] D4-G2c -> B（两车间人数相等即可；"一车间多于二车间"是反向陷阱）')

# ---------- G3-a 报数误差：1236、1250、1229；一人多计14件、一人少计7件、一人准确
vals = {'甲': 1236, '乙': 1250, '丙': 1229}
S = []
for acc in vals:
    others = [x for x in vals if x != acc]
    for p in permutations([14, -7]):
        if all(vals[o] - d == vals[acc] for o, d in zip(others, p)): S.append(acc)
print('G3-a 准确者', S)
assert S == ['甲']; print('[OK] D4-G3a -> 甲（真实1236）')

# ---------- G3-b 投篮：每次命中得3或5分，投6次全中；报 16、23、26、30
feas = {sum(c) for c in product([3, 5], repeat=6)}
wrong = [x for x in (16, 23, 26, 30) if x not in feas]
count_options('D4-G3b', len(wrong), {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')

# ---------- G3-c 只卖6元和9元，共卖40件；报 237、250、261、273
feas = {6 * a + 9 * (40 - a) for a in range(0, 41)}
wrong = [x for x in (237, 250, 261, 273) if x not in feas]
print('G3-c 报错', wrong)
count_options('D4-G3c', len(wrong), {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')

# ---------- 循环赛工具
def rr(teams, win=3, draw=1):
    M = list(combinations(teams, 2))
    for out in product('WDL', repeat=len(M)):
        pts = {t: 0 for t in teams}
        for (a, b), o in zip(M, out):
            if o == 'W': pts[a] += win
            elif o == 'L': pts[b] += win
            else: pts[a] += draw; pts[b] += draw
        yield dict(zip(M, out)), pts
T4 = ['甲', '乙', '丙', '丁']
# G4-a 甲7 乙5 丙4 丁0
S = [o for o, p in rr(T4) if (p['甲'], p['乙'], p['丙'], p['丁']) == (7, 5, 4, 0)]
print('G4-a 赛果', S)
draws = {sum(1 for v in o.values() if v == 'D') for o in S}
print('   平局数', draws, '甲乙之战', {o[('甲', '乙')] for o in S})
assert len(S) == 1
count_options('D4-G4a', list(draws)[0], {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')

# G4-b 积分各不相同、冠军全胜、第三名比第四名多2分 -> 第二名积分
res = set()
for o, p in rr(T4):
    v = sorted(p.values(), reverse=True)
    if len(set(v)) != 4: continue
    if v[0] != 9: continue
    if v[2] - v[3] != 2: continue
    res.add(tuple(v))
print('G4-b 积分组合', res)
assert len({v[1] for v in res}) == 1
count_options('D4-G4b', list(res)[0][1], {'A': 3, 'B': 4, 'C': 5, 'D': 6}, 'B')
