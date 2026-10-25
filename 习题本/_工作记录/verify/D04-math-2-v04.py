# D04-math-2-v04 限价下上调售价的最大日利润（枚举提价额，0.01元细分）
from fractions import Fraction as F
cost, p0, q0, k, cap = 45, 65, 180, 3, 75
def profit(x):
    return (p0 + x - cost) * (q0 - k * x)
xs = [F(i, 100) for i in range(0, (cap - p0) * 100 + 1)]      # 允许提价 0~10 元（含限价）
best = max(xs, key=profit)
maxp = profit(best)
assert all(profit(x) <= maxp for x in xs)
# 不考虑限价时的最优（顶点），用于确认顶点在区间外
free = [F(i, 100) for i in range(0, (q0 // k) * 100 + 1)]
vtx = max(free, key=profit)
assert p0 + vtx > cap
err = {'忽略限价取顶点': profit(vtx), '维持原价': profit(0), '限价单件利润×原销量': (cap - cost) * q0}
print('best x =', best, 'price =', p0 + best, 'max =', maxp, 'vertex price =', p0 + vtx, {k2: float(v) for k2, v in err.items()})
options = {'A': 3600, 'B': 4500, 'C': 4800, 'D': 5400}
hits = [k2 for k2, v in options.items() if v == maxp]
assert len(hits) == 1, hits
print(hits[0])
