# D04-math-2-v11 盈亏平衡+目标利润：降价后销量需增加的百分比
from fractions import Fraction as F
import math
Fix, vc, p0, p1, target = 60000, 30, 50, 46, 40000
q0 = F(Fix + target, p0 - vc)
assert q0.denominator == 1
# 降价后满足利润>=目标的最小整数销量
q1 = math.ceil(F(Fix + target, p1 - vc))
assert (p1 - vc) * q1 - Fix >= target and (p1 - vc) * (q1 - 1) - Fix < target
inc = (q1 - q0) / q0 * 100
alloc = Fix / q0
print('q0 =', q0, 'q1 =', q1, 'inc% =', inc, 'alloc-err% =', float((F(target, p1 - vc - alloc) - q0) / q0 * 100))
options = {'A': 8, 'B': 20, 'C': 25, 'D': 100}
hits = [k for k, v in options.items() if v == inc]
assert len(hits) == 1, hits
print(hits[0])
