# 验算 T046：环形同点出发，追及时间是相遇时间的 3 倍，求速度比
import sys
from sympy import symbols, Eq, solve, Rational
r = symbols('r', positive=True)   # 甲速/乙速（乙速取 1）
S = 1                              # 一圈
sol = [x for x in solve(Eq(S / (r - 1), 3 * S / (r + 1)), r) if x > 1]
assert len(sol) == 1
options = {'A': 3, 'B': Rational(5, 2), 'C': 2, 'D': Rational(3, 2)}
ans = [k for k, v in options.items() if v == sol[0]]
assert len(ans) == 1
print(f'速度比={sol[0]}:1', file=sys.stderr)
print(ans[0])
