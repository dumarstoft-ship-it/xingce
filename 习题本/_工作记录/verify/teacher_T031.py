# teacher_T031  1300千米，两种路段平均速度250、300千米/小时，4.5小时走完。两种路段里程差
from fractions import Fraction as F

DIST, V1, V2, T = 1300, 250, 300, F(9, 2)
OPTS = {'A': 600, 'B': 700, 'C': 800, 'D': 1050}
# 设250千米/小时路段用时 t1，则 V1*t1 + V2*(T-t1) = DIST
t1 = (V2 * T - DIST) / (V2 - V1)
t2 = T - t1
d1, d2 = V1 * t1, V2 * t2
assert t1 > 0 and t2 > 0 and d1 + d2 == DIST
ans = abs(d2 - d1)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['D'] == max(d1, d2)          # 求出较长路段就交卷
print('路段 =', d1, d2, ' 差 =', ans)
print(hits[0])
