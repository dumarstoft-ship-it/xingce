# teacher_T008  2024浙江A-60：甲乙合作20天完工；合作4天，乙退出6天，回归时完成40%；带丙三队再干10天完工。求效率比
from fractions import Fraction as F
from math import gcd

DAYS_PLAN, D_CO, D_OUT, DONE, D_LAST = 20, 4, 6, F(2, 5), 10
OPTS = {'A': (3, 6, 10), 'B': (4, 8, 15), 'C': (6, 3, 2), 'D': (10, 5, 3)}

b = F(1)                                     # 乙效率赋 1
# D_CO*(a+b) + D_OUT*a = DONE*DAYS_PLAN*(a+b)  → 关于 a 的一次方程
lhs = lambda a: D_CO * (a + b) + D_OUT * a - DONE * DAYS_PLAN * (a + b)
a = -lhs(F(0)) / (lhs(F(1)) - lhs(F(0)))
total = DAYS_PLAN * (a + b)
c = (total * (1 - DONE)) / D_LAST - a - b
assert c > 0
vals = [a, b, c]
den = 1
for v in vals:
    den = den * v.denominator // gcd(den, v.denominator)
ints = [int(v * den) for v in vals]
g = gcd(gcd(ints[0], ints[1]), ints[2])
ans = tuple(x // g for x in ints)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('甲:乙:丙 =', ans)
print(hits[0])
