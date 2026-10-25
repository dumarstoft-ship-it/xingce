# 验算 T055：360 米环道三人同向，求出发时甲在乙身后多少米（乙参考系 + 模拟复核）
import sys
from sympy import symbols, Eq, solve, Rational
u1, u3, d1, d3 = symbols('u1 u3 d1 d3', positive=True)  # 甲、丙相对乙的速度；出发时在乙身后距离
L = 360
t_jy = 3                                  # 甲追上乙
t_by = t_jy + Rational(3, 2)              # 丙第一次追上乙
t_bj = t_by + Rational(7, 2)              # 丙追上甲
t_by2 = t_bj + Rational(11, 2)            # 丙第二次追上乙
sol = solve([Eq(d1, u1 * t_jy), Eq(d3, u3 * t_by),
             Eq(d3 - d1, (u3 - u1) * t_bj), Eq(d3 + L, u3 * t_by2)],
            [u1, u3, d1, d3], dict=True)
assert len(sol) == 1
s = sol[0]
assert 0 < s[d1] < s[d3] < L
# 模拟复核：乙固定在 0，甲在 -d1，丙在 -d3，按相对速度前进，求各事件的首次发生时刻
def first_catch(gap, rel, n=1):
    return (gap + (n - 1) * L) / rel
assert first_catch(s[d1], s[u1]) == t_jy
assert first_catch(s[d3], s[u3]) == t_by
assert first_catch(s[d3] - s[d1], s[u3] - s[u1]) == t_bj
assert first_catch(s[d3], s[u3], 2) == t_by2
options = {'A': 48, 'B': 84, 'C': 108, 'D': 144}
ans = [k for k, v in options.items() if v == s[d1]]
assert len(ans) == 1
print(f'甲相对速度={s[u1]}，丙相对速度={s[u3]}，甲在乙身后{s[d1]}米', file=sys.stderr)
print(ans[0])
