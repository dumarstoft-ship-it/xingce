# T088 2013浙江B：1000克20%酒精中倒入200克A、400克B，浓度变15%，A浓度是B的2倍，求A浓度
from fractions import Fraction as F

M0, C0, MA, MB, CM, K = F(1000), F(20, 100), F(200), F(400), F(15, 100), F(2)
OPTS = {'A': F(5, 100), 'B': F(6, 100), 'C': F(8, 100), 'D': F(10, 100)}

# 在0.1%精度上搜索B的浓度
sols = []
for i in range(0, 1001):
    cb = F(i, 1000)
    ca = K * cb
    if ca <= 1 and M0 * C0 + MA * ca + MB * cb == CM * (M0 + MA + MB):
        sols.append((ca, cb))
assert len(sols) == 1
ca, cb = sols[0]
hits = [k for k, v in OPTS.items() if v == ca]
assert len(hits) == 1, (ca, hits)
assert cb == OPTS['A']             # 干扰项：求成了B的浓度
print('A =', ca, 'B =', cb)
print(hits[0])
