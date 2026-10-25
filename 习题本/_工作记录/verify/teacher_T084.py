# T084 2009江西：40%酒精加4千克水变30%，再加M千克纯酒精变50%，求M
from fractions import Fraction as F

C0, WATER, C1, C2 = F(40, 100), F(4), F(30, 100), F(50, 100)
OPTS = {'A': F(8), 'B': F(12), 'C': F(46, 10), 'D': F(64, 10)}

# 第一步：在0.1千克精度上搜索原溶液质量 m，使 C0*m/(m+4)=C1
ms = [F(i, 10) for i in range(1, 10001) if C0 * F(i, 10) / (F(i, 10) + WATER) == C1]
assert len(ms) == 1
m = ms[0]
alc, tot = C0 * m, m + WATER
# 第二步：搜索加入的纯酒精 M（0.1千克精度），使 (alc+M)/(tot+M)=C2
Ms = [F(i, 10) for i in range(0, 10001) if (alc + F(i, 10)) / (tot + F(i, 10)) == C2]
assert len(Ms) == 1
M = Ms[0]
hits = [k for k, v in OPTS.items() if v == M]
assert len(hits) == 1, (M, hits)
assert tot * C2 == OPTS['A']          # 干扰项：只算出50%时应有的酒精量8
print('original mass', m, 'alcohol', alc, 'M =', M)
print(hits[0])
