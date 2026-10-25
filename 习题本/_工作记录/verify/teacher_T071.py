# 验算 T071：池中原有水，1 台 6 小时到半满，3 台 8 小时到满；排空后 4 台几小时灌满
import sys
from sympy import symbols, Eq, solve
W0, C = symbols('W0 C')
sol = solve([Eq(W0 + 1 * 6, C / 2), Eq(W0 + 3 * 8, C)], [W0, C], dict=True)
assert len(sol) == 1 and sol[0][W0] >= 0
t = sol[0][C] / 4
options = {'A': 6, 'B': 7, 'C': 8, 'D': 9}
ans = [k for k, v in options.items() if v == t]
assert len(ans) == 1
print(f'原有水={sol[0][W0]}，满池={sol[0][C]}，4台={t}小时', file=sys.stderr)
print(ans[0])
