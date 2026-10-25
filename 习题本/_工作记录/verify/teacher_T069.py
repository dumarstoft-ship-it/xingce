# 验算 T069：年龄与工龄双重关系，求李某参加工作时年龄
import sys
from sympy import symbols, Eq, solve, Rational
L, sL, Z, sZ = symbols('L sL Z sZ')   # 2020 年：李年龄、李工龄、张年龄、张工龄
sol = solve([Eq(L, 4 * sL),
             Eq(L, Rational(2, 3) * Z),
             Eq(Z + 4, 2 * (sZ + 4)),     # 2024 年张年龄 = 2 × 张工龄
             Eq(L - sZ, 10)],             # 张参加工作（sZ 年前）时李 10 岁
            [L, sL, Z, sZ], dict=True)
assert len(sol) == 1
age = sol[0][L] - sol[0][sL]
options = {'A': 18, 'B': 21, 'C': 24, 'D': 27}
ans = [k for k, v in options.items() if v == age]
assert len(ans) == 1
print(f'{sol[0]}，李参加工作时{age}岁', file=sys.stderr)
print(ans[0])
