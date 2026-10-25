# 验算 T070：完成一半后维修 20 分钟，效率提高 1/3，提前 40 分钟完成，求维修后每小时产量
import sys
from sympy import symbols, Eq, solve, Rational
e = symbols('e', positive=True)     # 原效率（个/小时）
total = 480
plan = total / e
actual = Rational(total, 2) / e + Rational(20, 60) + Rational(total, 2) / (e * Rational(4, 3))
sol = solve(Eq(plan - actual, Rational(40, 60)), e)
assert len(sol) == 1
new = sol[0] * Rational(4, 3)
options = {'A': 80, 'B': 87, 'C': 94, 'D': 102}
ans = [k for k, v in options.items() if v == new]
assert len(ans) == 1
print(f'原效率={sol[0]}，新效率={new}', file=sys.stderr)
print(ans[0])
