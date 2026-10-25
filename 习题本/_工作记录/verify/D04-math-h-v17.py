# D04-math-h-v17：花卉合作社须按 30 元/扎交付 960 扎完好的鲜切花，收购价 12 元/扎。
# 普通物流运费 1 元/扎、途中损耗 20%；冷链物流损耗 4%、运费待定；运费按发运扎数计，损耗的花不能交付。
# 求：冷链利润不低于普通物流时，冷链运费的最高值。
# 独立求解：对每种物流，从小到大找出“发运后完好数量不少于 960 扎”的最少发运扎数，
# 再算两种方式的利润（收入 − 收购费 − 运费）；冷链运费按 0.01 元逐档枚举，找出满足条件的最大值，与选项比对。
from fractions import Fraction as Fr

NEED, SETTLE = 960, 30
BUY = 12
NORMAL_FREIGHT, NORMAL_LOSS = 1, Fr(20, 100)
COLD_LOSS = Fr(4, 100)

OPTIONS = {'A': '1.2', 'B': '2.4', 'C': '3', 'D': '3.6'}


def min_ship(loss):
    n = NEED
    while n * (1 - loss) < NEED:
        n += 1
    return n


def profit(freight, loss):
    ship = min_ship(loss)
    return SETTLE * NEED - BUY * ship - freight * ship


ship_n, ship_c = min_ship(NORMAL_LOSS), min_ship(COLD_LOSS)
base = profit(NORMAL_FREIGHT, NORMAL_LOSS)
best = None
for cents in range(0, 3001):
    f = Fr(cents, 100)
    if profit(f, COLD_LOSS) >= base:
        best = f
print('普通物流发运', ship_n, '扎，利润', base, '；冷链发运', ship_c, '扎；冷链运费最高', best, '元/扎')
for k, v in OPTIONS.items():
    print(k, v, '冷链利润', profit(Fr(v), COLD_LOSS))

hits = [k for k, v in OPTIONS.items() if Fr(v) == best]
assert len(hits) == 1, hits
print(hits[0])
