# D04-math-h-v08：年供应大米 3000 袋，分若干批进货，每批袋数相同；每批运输装卸费 160 元（与批量无关）；
# 每袋年仓储费 6 元，全年平均库存按每批进货量的一半计。问每批进货多少袋时，全年运输装卸费与仓储费之和最少。
# 做法：只有能把 3000 袋等分的批量才可行（批数、每批袋数都是整数），枚举全部可行批量逐一算费用取最小；
# 另验证连续情形的理论最优点不能等分（这正是本题要比较两侧可行解的原因）。选项中不可行的批量一律不成立。
import math
from fractions import Fraction as F

OPTIONS = {'A': 400, 'B': 500, 'C': 300, 'D': 375}
DEMAND, FEE_PER_BATCH, HOLD_PER_BAG_YEAR = 3000, 160, 6


def annual_cost(batch):
    batches = F(DEMAND, batch)                   # 全年进货批数
    avg_stock = F(batch, 2)                      # 平均库存
    return FEE_PER_BATCH * batches + HOLD_PER_BAG_YEAR * avg_stock


feasible = [DEMAND // n for n in range(1, DEMAND + 1) if DEMAND % n == 0]
costs = {b: annual_cost(b) for b in feasible}
best = min(costs.values())
argmin = [b for b, c in costs.items() if c == best]
assert len(argmin) == 1, argmin

x_star = math.sqrt(2 * DEMAND * FEE_PER_BATCH / HOLD_PER_BAG_YEAR)   # 连续情形的理论最优
assert x_star not in costs and DEMAND % round(x_star) != 0            # 理论最优不能等分

correct = [k for k, v in OPTIONS.items() if v in costs and costs[v] == best]
assert len(correct) == 1, correct
print('theoretical optimum =', x_star, 'batches =', DEMAND / x_star)
print('best feasible batch =', argmin[0], 'cost =', best)
print('options:', {k: (int(costs[v]) if v in costs else 'infeasible') for k, v in OPTIONS.items()})
print(correct[0])
