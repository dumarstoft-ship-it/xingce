# D04-math-2-v13 滞销含处理价：已知10天总利润，反求剩余斤数（枚举）
buy, cost, price, salvage = 100, 5, 10, 2
def day_profit(left):
    return price * (buy - left) + salvage * left - cost * buy
sols = [r for r in range(0, buy + 1) if 6 * day_profit(0) + 4 * day_profit(r) == 4520]
assert len(sols) == 1, sols
r = sols[0]
# 干扰项路径
no_salv = [x for x in range(0, 101) if 6 * 500 + 4 * (price * (buy - x) - cost * buy) == 4520]
sold_cost = [x for x in range(0, 101) if 6 * 500 + 4 * ((price - cost) * (buy - x)) == 4520]
sold_cost_salv = [x for x in range(0, 101) if 6 * 500 + 4 * ((price - cost) * (buy - x) + salvage * x) == 4520]
print('r =', r, no_salv, sold_cost, sold_cost_salv)
options = {'A': 12, 'B': 15, 'C': 24, 'D': 40}
hits = [k for k, v in options.items() if v == r]
assert len(hits) == 1, hits
print(hits[0])
