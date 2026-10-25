# 验算 T067：2008 年三人年龄和 60，2010 年甲是丙 2 倍，2011 年乙是丙 2 倍，求甲出生年份
import sys
from sympy import symbols, Eq, solve
a, b, c = symbols('a b c')     # 2008 年的年龄
sol = solve([Eq(a + b + c, 60), Eq(a + 2, 2 * (c + 2)), Eq(b + 3, 2 * (c + 3))], [a, b, c], dict=True)
assert len(sol) == 1
birth = 2008 - sol[0][a]
options = {'A': 1988, 'B': 1986, 'C': 1984, 'D': 1982}
ans = [k for k, v in options.items() if v == birth]
assert len(ans) == 1
print(f'2008年 甲{sol[0][a]} 乙{sol[0][b]} 丙{sol[0][c]}，甲生于{birth}', file=sys.stderr)
print(ans[0])
