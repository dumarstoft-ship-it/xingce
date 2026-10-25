# 验算 T080：甲乙合作 10 小时 + 丙单干 1 小时完成；乙比甲多 4 小时，丙是甲的 1/2 多 2 小时；求甲单干时间
import sys
from sympy import symbols, Eq, solve
a = symbols('a', positive=True)
sol = solve(Eq(10 / a + 10 / (a + 4) + 1 / (a / 2 + 2), 1), a)
assert len(sol) == 1
options = {'A': 20, 'B': 25, 'C': 30, 'D': 35}
ans = [k for k, v in options.items() if v == sol[0]]
assert len(ans) == 1
print(f'甲单干={sol[0]}小时', file=sys.stderr)
print(ans[0])
