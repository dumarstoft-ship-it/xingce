# 验算 T074：效率相同先后开工，9:38 甲是乙 4 倍，9:53 甲是乙 1.5 倍，求甲早开工几分钟
import sys
from sympy import symbols, Eq, solve, Rational
s, d = symbols('s d')   # 乙在 9 点后第 s 分钟开工，甲早 d 分钟
sol = solve([Eq(38 - s + d, 4 * (38 - s)), Eq(53 - s + d, Rational(3, 2) * (53 - s))], [s, d], dict=True)
assert len(sol) == 1
ss, dd = sol[0][s], sol[0][d]
assert 0 <= ss - dd < ss < 38      # 两人都在 9 点多、9:38 前开工
options = {'A': 4, 'B': 6, 'C': 8, 'D': 9}
ans = [k for k, v in options.items() if v == dd]
assert len(ans) == 1
print(f'乙9:{ss}开工，甲9:{ss-dd}开工，早{dd}分钟', file=sys.stderr)
print(ans[0])
