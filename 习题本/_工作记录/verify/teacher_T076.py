# 验算 T076：甲生产 A、B 的效率分别是乙的 2 倍、3 倍，最快完成各 X 件时甲共产 1.5X 件；
# 对每个选项（乙的 A 效率 / 乙的 B 效率）解线性规划，看哪个选项使最优方案中甲的产量恰为 1.5X（且唯一）
import sys
from sympy import symbols, Rational
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


X = 1
t1, t2, s1, s2, T = symbols('t1 t2 s1 s2 T')   # 甲做 A/B 的时间，乙做 A/B 的时间，总时间


def check(r):
    aA, aB = r, 1                 # 乙：A 效率 r，B 效率 1
    jA, jB = 2 * aA, 3 * aB       # 甲：分别为乙的 2 倍、3 倍
    base = [t1 >= 0, t2 >= 0, s1 >= 0, s2 >= 0]
    cons = base + [T >= 0, jA * t1 + aA * s1 >= X, jB * t2 + aB * s2 >= X, t1 + t2 <= T, s1 + s2 <= T]
    Tmin, _ = lp_opt(T, cons, [t1, t2, s1, s2, T])
    # 在最短时间内恰好完成任务时，甲的产量可能的范围
    cons2 = base + [jA * t1 + aA * s1 >= X, jA * t1 + aA * s1 <= X,
                    jB * t2 + aB * s2 >= X, jB * t2 + aB * s2 <= X,
                    t1 + t2 <= Tmin, s1 + s2 <= Tmin]
    out = jA * t1 + jB * t2
    lo, _ = lp_opt(out, cons2, [t1, t2, s1, s2], 'min')
    hi, _ = lp_opt(out, cons2, [t1, t2, s1, s2], 'max')
    return Tmin, lo, hi


options = {'A': Rational(3, 4), 'B': Rational(3, 5), 'C': Rational(4, 3), 'D': Rational(5, 3)}
hits = []
for k, r in options.items():
    Tmin, lo, hi = check(r)
    print(f'{k}: r={r} 最短时间={Tmin} 甲产量∈[{lo},{hi}]', file=sys.stderr)
    if lo == hi == Rational(3, 2) * X:
        hits.append(k)
assert len(hits) == 1
print(hits[0])
