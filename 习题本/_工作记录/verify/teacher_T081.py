# 验算 T081：甲按时、乙延后 5 天、丙提前 3 天；甲做 6 天后乙做 12 天恰好完成，求乙单独天数
import sys
from sympy import symbols, Eq, solve
n = symbols('n', positive=True)   # 规定工期 = 甲单独天数
sol = solve(Eq(6 / n + 12 / (n + 5), 1), n)
assert len(sol) == 1 and sol[0] - 3 > 0   # 丙的天数也须为正
yi = sol[0] + 5
options = {'A': 12, 'B': 15, 'C': 18, 'D': 20}
ans = [k for k, v in options.items() if v == yi]
assert len(ans) == 1
print(f'工期={sol[0]}，乙单独={yi}天', file=sys.stderr)
print(ans[0])
