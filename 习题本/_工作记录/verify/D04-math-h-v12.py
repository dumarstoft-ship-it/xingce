# D04-math-h-v12：售价 60 元/套，每月固定成本 12 万元；每月前 6000 套变动成本 40 元/套，超过 6000 套的部分 30 元/套；
# 产品全部售出。要使当月成本利润率（利润÷总成本）不低于 20%，问当月至少销售多少套。
# 做法：按分段规则逐套累计变动成本，从 1 套起逐一计算利润与总成本，找第一个满足的销量，并确认之后一直满足。
from fractions import Fraction as F

OPTIONS = {'A': 9000, 'B': 10000, 'C': 12000, 'D': 18000}
FIXED, PRICE, TARGET = 120000, 60, F(20, 100)
TIERS = [(6000, 40), (None, 30)]          # (本段上限累计套数, 本段每套变动成本)


def variable_cost(q):
    cost, done = 0, 0
    for cap, unit in TIERS:
        take = (q - done) if cap is None else max(0, min(q, cap) - done)
        cost += take * unit
        done += take
    return cost


def margin(q):
    total_cost = FIXED + variable_cost(q)
    return F(PRICE * q - total_cost, total_cost)


least = next(q for q in range(1, 10 ** 6) if margin(q) >= TARGET)
assert all(margin(q) >= TARGET for q in range(least, least + 30000))
hits = [k for k, v in OPTIONS.items() if v == least]
assert len(hits) == 1
print('least quantity =', least, 'margin there =', margin(least), 'margin one less =', float(margin(least - 1)))
print(hits[0])
