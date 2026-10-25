# 验算 T075：三台收割机每小时 2 亩，先后开工，求乙开工时刻
import sys
from sympy import symbols, Eq, solve, Rational
ta, tb, tc = symbols('ta tb tc')   # 开工时刻（小时）
r = 2
A, B, C = r * (12 - ta), r * (12 - tb), r * (12 - tc)
sol = solve([Eq(A, Rational(3, 2) * B), Eq(A - C, 6),
             Eq(r * (16 - ta) + r * (16 - tb) + r * (16 - tc), 50)], [ta, tb, tc], dict=True)
assert len(sol) == 1
s = sol[0]
assert all(0 <= s[x] < 12 for x in (ta, tb, tc))   # 都在上午开工
options = {'A': 6, 'B': 7, 'C': 8, 'D': 9}
ans = [k for k, v in options.items() if v == s[tb]]
assert len(ans) == 1
print(f'甲{s[ta]}点 乙{s[tb]}点 丙{s[tc]}点开工', file=sys.stderr)
print(ans[0])
