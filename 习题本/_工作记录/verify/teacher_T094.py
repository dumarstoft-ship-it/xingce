# T094 拿铁与美式售价相同，拿铁售价比利润多200%，美式成本比拿铁少1/4，总利润率80%，求销量比
from fractions import Fraction as F
from math import gcd

PRICE = F(3)                      # 任设售价
L_PROFIT = PRICE / (1 + 2)        # 售价比利润多200% → 售价=利润×3
L_COST = PRICE - L_PROFIT
A_COST = L_COST * (1 - F(1, 4))
TARGET = F(80, 100)
OPTS = {'A': (2, 1), 'B': (1, 2), 'C': (2, 3), 'D': (3, 2)}

ratios = set()
for nl in range(1, 61):
    for na in range(1, 61):
        cost = nl * L_COST + na * A_COST
        profit = nl * (PRICE - L_COST) + na * (PRICE - A_COST)
        if profit / cost == TARGET:
            g = gcd(nl, na)
            ratios.add((nl // g, na // g))
assert len(ratios) == 1, ratios
r = ratios.pop()
hits = [k for k, v in OPTS.items() if v == r]
assert len(hits) == 1
# 干扰项：把成本权重比2:3当成销量比
lw = (TARGET - (PRICE - A_COST) / A_COST) / ((PRICE - L_COST) / L_COST - (PRICE - A_COST) / A_COST)
assert (lw / (1 - lw)) == F(2, 3)
print('latte:americano =', r)
print(hits[0])
