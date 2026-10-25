# 验算 T043：下坡 3 小时、上坡 4 小时，下坡比上坡快 15 千米/小时，求距离
import sys
from sympy import symbols, Eq, solve
vd, D = symbols('vd D', positive=True)
sol = solve([Eq(D, 3 * vd), Eq(D, 4 * (vd - 15))], [vd, D], dict=True)
assert len(sol) == 1
dist = sol[0][D]
options = {'A': 120, 'B': 180, 'C': 240, 'D': 300}
ans = [k for k, v in options.items() if v == dist]
assert len(ans) == 1
print(f'下坡速度={sol[0][vd]}，距离={dist}', file=sys.stderr)
print(ans[0])
