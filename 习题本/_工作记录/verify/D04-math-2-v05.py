# D04-math-2-v05 民宿定价：成本只对入住房计（枚举提价档数，并用连续价格复核）
from fractions import Fraction as F
rooms, base, step, drop, svc = 40, 200, 20, 2, 40
def profit_step(x):
    occ = rooms - drop * x
    return (base + step * x - svc) * occ
xs = range(0, rooms // drop + 1)
best = max(xs, key=profit_step)
vals = sorted(((profit_step(x), x) for x in xs), reverse=True)
assert vals[0][0] > vals[1][0]          # 最优唯一
price = base + step * best
# 连续价格复核：入住 = 40 - (p-200)/10
def profit_cont(pp):
    return (pp - svc) * (rooms - (pp - base) * F(drop, step))
grid = [F(base) + F(i, 10) for i in range(0, 4001)]
pc = max(grid, key=profit_cont)
assert pc == price
no_cost = base + step * max(xs, key=lambda x: (base + step * x) * (rooms - drop * x))
print('best price =', price, 'profit =', profit_step(best), 'ignore cost ->', no_cost)
options = {'A': 280, 'B': 300, 'C': 320, 'D': 340}
hits = [k for k, v in options.items() if v == price]
assert len(hits) == 1, hits
print(hits[0])
