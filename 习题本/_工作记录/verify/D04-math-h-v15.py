# D04-math-h-v15：服装厂月产能 10000 件，现每月产销 8000 件、售价 60 元；按现产量核算单件成本 45 元，
# 其中变动成本 30 元，其余为按产量分摊的固定成本（月固定成本总额不变）。外贸客户要求当月加订 3000 件，
# 产能不足时要减少常规销售。求：接单后当月利润不减少时，订单单价的最低值。
# 独立求解：先由题面算出月固定成本总额，再分别计算不接单、接单（常规销售降为产能减订单量）的当月总利润，
# 按 0.01 元逐档枚举单价，找出使接单后利润不低于原利润的最低单价，与选项比对。
from fractions import Fraction as Fr

CAPACITY = 10000
REGULAR_NOW, PRICE = 8000, 60
UNIT_COST_NOW, VAR_COST = 45, 30
ORDER = 3000

OPTIONS = {'A': 30, 'B': 35, 'C': 40, 'D': 45}

FIXED = (UNIT_COST_NOW - VAR_COST) * REGULAR_NOW          # 分摊的固定成本 × 现产量 = 月固定成本总额


def month_profit(regular, order_qty, order_price):
    produced = regular + order_qty
    assert produced <= CAPACITY
    return PRICE * regular + order_price * order_qty - VAR_COST * produced - FIXED


before = month_profit(REGULAR_NOW, 0, 0)
regular_after = min(REGULAR_NOW, CAPACITY - ORDER)       # 产能不足时只能减少常规销售
best = None
for cents in range(0, 20001):
    p = Fr(cents, 100)
    if month_profit(regular_after, ORDER, p) >= before:
        best = p
        break
print('月固定成本', FIXED, '；不接单利润', before, '；接单后常规销售', regular_after, '件；最低单价', best)
for k, v in OPTIONS.items():
    print(k, v, '接单后利润', month_profit(regular_after, ORDER, v))

hits = [k for k, v in OPTIONS.items() if v == best]
assert len(hits) == 1, hits
print(hits[0])
