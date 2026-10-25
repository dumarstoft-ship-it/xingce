# 验算 T038：两种速度到达时刻不同、出发时刻相同，求出发时刻
import sys
from fractions import Fraction as F
v1, arrive1 = 18, 17   # 18 千米/时，17:00 到达
v2, arrive2 = 20, 16   # 20 千米/时，16:00 到达
# 路程相同：v1*(arrive1-d) = v2*(arrive2-d)
d = F(v1 * arrive1 - v2 * arrive2, v1 - v2)
dist = v1 * (arrive1 - d)
assert dist == v2 * (arrive2 - d) and dist > 0
options = {'A': 6, 'B': 7, 'C': 8, 'D': 12}
ans = [k for k, v in options.items() if v == d]
assert len(ans) == 1
print(f'出发时刻={d}点，路程={dist}千米', file=sys.stderr)
print(ans[0])
