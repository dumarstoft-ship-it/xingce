# teacher_T028  2024国考-66：甲速比乙快20%；乙行驶1小时后提速30千米/小时，又3小时与甲同时到达。AB距离
from fractions import Fraction as F

FAST, T1, T2, DV = F(6, 5), 1, 3, 30
OPTS = {'A': 540, 'B': 510, 'C': 600, 'D': 570}
# 甲: FAST*v*(T1+T2) ；乙: v*T1 + (v+DV)*T2 ；两者相等，解 v
g = lambda v: FAST * v * (T1 + T2) - (v * T1 + (v + DV) * T2)
v = -g(F(0)) / (g(F(1)) - g(F(0)))
dist = FAST * v * (T1 + T2)
assert v > 0 and g(v) == 0
hits = [k for k, val in OPTS.items() if val == dist]
assert len(hits) == 1, (dist, hits)
print('乙原速 =', v, ' 距离 =', dist)
print(hits[0])
