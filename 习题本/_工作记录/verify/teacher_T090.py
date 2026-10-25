# T090 2021湖北选调：营收降10%、成本降20%，2019年利润率20%，求2020年利润率
from fractions import Fraction as F

REV_CHG, COST_CHG, R0 = F(-10, 100), F(-20, 100), F(20, 100)
OPTS = {'A': F(25, 100), 'B': F(30, 100), 'C': F(35, 100), 'D': F(40, 100)}

rates = set()
for cost in range(1, 201):           # 任取2019年成本，结果应一致
    cost = F(cost)
    rev = cost * (1 + R0)
    rev2, cost2 = rev * (1 + REV_CHG), cost * (1 + COST_CHG)
    rates.add((rev2 - cost2) / cost2)
assert len(rates) == 1
r = rates.pop()
hits = [k for k, v in OPTS.items() if v == r]
assert len(hits) == 1, (r, hits)
print('2020 profit rate =', r)
print(hits[0])
