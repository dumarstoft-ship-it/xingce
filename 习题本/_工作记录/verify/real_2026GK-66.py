# real 2026GK-66  甲、乙、丙三种花卉共10公顷；甲是乙的2倍；丙比乙少2公顷。求丙的面积。
from fractions import Fraction as F
OPTS = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
TOTAL = 10
# 以0.01公顷为步长穷举乙的面积
sols = []
for x100 in range(1, TOTAL * 100 + 1):
    y = F(x100, 100)
    a, c = 2 * y, y - 2
    if c > 0 and a + y + c == TOTAL:
        sols.append((a, y, c))
assert len(sols) == 1, sols
a, y, c = sols[0]
hits = [k for k, v in OPTS.items() if v == c]
assert len(hits) == 1, hits
# 干扰项：把“丙比乙少2”写成丙＝乙＋2
bad = [F(t, 100) for t in range(1, 1001) if 2 * F(t, 100) + F(t, 100) + F(t, 100) + 2 == TOTAL]
assert len(bad) == 1 and bad[0] + 2 == OPTS['D']
assert y == OPTS['C']                     # 求成乙的面积
print('jia yi bing', a, y, c)
print(hits[0])
