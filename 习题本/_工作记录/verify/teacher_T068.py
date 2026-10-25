# 验算 T068：2013 年女儿是母亲 1/4，40 年后为 2/3，何年女儿是母亲 1/2
import sys
from sympy import symbols, Eq, solve, Rational
d, m, y = symbols('d m y')
s = solve([Eq(d, m / 4), Eq(d + 40, Rational(2, 3) * (m + 40))], [d, m], dict=True)[0]
yy = solve(Eq(s[d] + y, Rational(1, 2) * (s[m] + y)), y)
assert len(yy) == 1
year = 2013 + yy[0]
options = {'A': 2021, 'B': 2022, 'C': 2026, 'D': 2029}
ans = [k for k, v in options.items() if v == year]
assert len(ans) == 1
print(f'2013年 女{s[d]} 母{s[m]}，{year}年', file=sys.stderr)
print(ans[0])
