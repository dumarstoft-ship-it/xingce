# D01-math-1-v06  产业园区总产值：电子信息占30%，生物医药占比比电子信息低10个百分点，其余为高端装备制造；
# 高端装备比生物医药多48亿元。求总产值（亿元）。
from fractions import Fraction as F

EI, PTS, DIFF = F(30, 100), F(10, 100), 48
OPTS = {'A': 96, 'B': 160, 'C': 300, 'D': 480}

bio = EI - PTS                 # “低10个百分点”：占比直接相减
equip = 1 - EI - bio
# 以0.01亿元为步长穷举总产值，找出使两产业差额恰为48亿元的值
sols = [F(t, 100) for t in range(1, 200001) if (equip - bio) * F(t, 100) == DIFF]
assert len(sols) == 1, sols
T = sols[0]
hits = [k for k, v in OPTS.items() if v == T]
assert len(hits) == 1, hits

# 干扰项来源核对
bio_bad = EI * (1 - PTS)                         # 把“低10个百分点”当成“低10%”：27%
equip_bad = 1 - EI - bio_bad                     # 43%
assert DIFF / (equip_bad - bio_bad) == OPTS['C']
assert DIFF / PTS == OPTS['D']                   # 48亿元对应到10个百分点上
assert DIFF / equip == OPTS['A']                 # 48亿元当成高端装备的产值
print('shares', bio, equip, 'total', T)
print(hits[0])
