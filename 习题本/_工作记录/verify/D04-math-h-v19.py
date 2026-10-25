# D04-math-h-v19：鲜牛奶进价 8 元/瓶、售价 12 元/瓶，当天卖不完的晚上按 2 元/瓶处理。
# 过去 20 天日需求：80 瓶 3 天、100 瓶 6 天、120 瓶 7 天、140 瓶 4 天。
# 每天订购量固定，只能取 80、100、120、140 之一，求 20 天总利润最大的订购量。
# 独立求解：对每个可选订购量，逐天按“卖出 min(订购量, 需求)，剩余按处理价”算利润并求和，取最大者。
# （选项按轮转升序排列：120、140、80、100。）

PRICE, COST, SALVAGE = 12, 8, 2
DEMAND = {80: 3, 100: 6, 120: 7, 140: 4}
CHOICES = [80, 100, 120, 140]

OPTIONS = {'A': 120, 'B': 140, 'C': 80, 'D': 100}

days = [d for d, n in DEMAND.items() for _ in range(n)]
assert len(days) == 20


def total_profit(q):
    s = 0
    for d in days:
        sold = min(q, d)
        s += PRICE * sold + SALVAGE * (q - sold) - COST * q
    return s


totals = {q: total_profit(q) for q in CHOICES}
print('各订购量 20 天总利润', totals)
best = max(totals.values())
arg = [q for q, t in totals.items() if t == best]
assert len(arg) == 1, arg
print('最优订购量', arg[0])

hits = [k for k, v in OPTIONS.items() if v == arg[0]]
assert len(hits) == 1, hits
print(hits[0])
