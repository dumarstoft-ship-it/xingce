# 验算 T078：张做甲、乙文件各需 2、8 小时，王各需 1、6 小时，合作至少几小时（线性规划）
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


z1, z2, w1, w2, T = symbols('z1 z2 w1 w2 T')   # 张、王分别用在甲、乙文件上的时间
cons = [z1 / 2 + w1 / 1 >= 1, z2 / 8 + w2 / 6 >= 1,
        z1 + z2 <= T, w1 + w2 <= T, z1 >= 0, z2 >= 0, w1 >= 0, w2 >= 0, T >= 0]
Tmin, sol = lp_opt(T, cons, [z1, z2, w1, w2, T])
options = {'A': 3, 'B': 4, 'C': 5, 'D': 6}
ans = [k for k, v in options.items() if v == Tmin]
assert len(ans) == 1
print(f'至少{Tmin}小时，方案{sol}', file=sys.stderr)
print(ans[0])
