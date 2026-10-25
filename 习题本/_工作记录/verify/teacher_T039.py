# 验算 T039：大巴晚到 12 公里、出租车早到 24 分钟，求学校到机场距离
import sys
from sympy import symbols, Eq, solve, Rational
D, T = symbols('D T', positive=True)  # D 距离(千米)，T 出发到起飞的时间(小时)
sol = solve([Eq(40 * T, D - 12), Eq(D / 50, T - Rational(24, 60))], [D, T], dict=True)
assert len(sol) == 1
dist = sol[0][D]
options = {'A': 100, 'B': 132, 'C': 140, 'D': 160}
ans = [k for k, v in options.items() if v == dist]
assert len(ans) == 1
print(f'D={dist}, T={sol[0][T]}', file=sys.stderr)
print(ans[0])
