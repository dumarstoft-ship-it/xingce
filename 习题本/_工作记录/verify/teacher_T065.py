# 验算 T065：出门时把时针分针看反，到公司时真实时间正是看错的时间（8 点多），求路上用时
import sys
from itertools import product
from sympy import symbols, Eq, solve, Rational
T1, T2 = symbols('T1 T2')   # 出门、到达的真实时刻（从 0:00 起的分钟数）
sols = []
for a, b in product(range(0, 40), range(0, 60)):
    # 到达时时针位置 = 出门时分针位置；到达时分针位置 = 出门时时针位置（均 mod 360）
    s = solve([Eq(Rational(1, 2) * T2, 6 * T1 - 360 * a),
               Eq(6 * T2 - 360 * b, Rational(1, 2) * T1)], [T1, T2], dict=True)
    if not s:
        continue
    t1, t2 = s[0][T1], s[0][T2]
    if 480 <= t2 < 540 and 0 <= 6 * T1.subs(T1, t1) - 360 * a < 360 \
            and 0 <= 6 * t2 - 360 * b < 360 and 0 < t2 - t1 <= 90:
        sols.append((t1, t2, t2 - t1))
assert len(sols) == 1
t1, t2, d = sols[0]
options = {'A': 48, 'B': 55, 'C': 60, 'D': 63}
best = min(options, key=lambda k: abs(options[k] - d))
print(f'出门{float(t1)/60:.4f}h，到达{float(t2)/60:.4f}h，用时{d}≈{float(d):.2f}分', file=sys.stderr)
print(best)
