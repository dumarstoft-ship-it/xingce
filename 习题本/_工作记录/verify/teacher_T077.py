# 验算 T077：40 台机械需 120A、80B，甲每天 6A 或 3B，乙每天 1A 或 2B，至少几天（线性规划）
import sys
from sympy import symbols
from itertools import combinations
from sympy import Matrix, linear_eq_to_matrix


def lp_opt(obj, cons, vars_, sense="min"):
    """小规模线性规划的精确解：枚举可行顶点（变量均非负，区域有顶点）。"""
    rows = []
    for c in cons:
        expr = (c.lhs - c.rhs) if c.rel_op in ("<=", "<") else (c.rhs - c.lhs)   # expr <= 0
        A, b = linear_eq_to_matrix([expr], vars_)
        rows.append((A.row(0), b[0]))                                           # A x <= b
    best, best_pt = None, None
    for idx in combinations(range(len(rows)), len(vars_)):
        A = Matrix.vstack(*[rows[i][0] for i in idx])
        if A.det() == 0:
            continue
        x = A.LUsolve(Matrix([rows[i][1] for i in idx]))
        if all((r[0] * x)[0] <= r[1] for r in rows):
            val = obj.subs(dict(zip(vars_, x)))
            if best is None or (val < best if sense == "min" else val > best):
                best, best_pt = val, dict(zip(vars_, x))
    return best, best_pt


n, perA, perB = 40, 3, 2
needA, needB = n * perA, n * perB
x, y, T = symbols('x y T')   # 甲、乙生产 A 的天数，总天数 T
cons = [6 * x + 1 * y >= needA, 3 * (T - x) + 2 * (T - y) >= needB,
        x >= 0, y >= 0, x <= T, y <= T, T >= 0]
Tmin, sol = lp_opt(T, cons, [x, y, T])
options = {'A': 24, 'B': 26, 'C': 28, 'D': 30}
ans = [k for k, v in options.items() if v == Tmin]
assert len(ans) == 1
print(f'最少{Tmin}天，方案{sol}', file=sys.stderr)
print(ans[0])
