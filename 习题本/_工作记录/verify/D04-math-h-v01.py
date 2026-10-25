# D04-math-h-v01: imported electric toothbrushes. Purchase price 200 yuan each, import duty = 10% of the
# purchase price, freight 8 yuan each. Sold at a mall counter: during the promotion every sale is made at
# 90% of the list price, and the mall keeps 20% of each actual transaction amount. The profit per brush must
# be at least 20% of its FULL cost = purchase price + duty + freight + the mall's share. Find the lowest
# admissible list price.
# Method: model profit = deal price - full cost and full cost (which itself grows with the price) with exact
# rationals, scan list prices in steps of 0.01 yuan for the first one that meets the requirement, and check
# the requirement keeps holding above it (so that first price is the minimum). Then match the options.
from fractions import Fraction as F

OPTIONS = {'A': 304, 'B': 360, 'C': 380, 'D': 400}

PURCHASE = F(200)
DUTY = PURCHASE * F(10, 100)
FREIGHT = F(8)
GOODS = PURCHASE + DUTY + FREIGHT         # 228
DISCOUNT = F(90, 100)                     # deal price = list price x 0.9
SHARE = F(20, 100)                        # mall share, charged on the actual deal price
RATE = F(20, 100)


def full_cost(list_price):
    return GOODS + list_price * DISCOUNT * SHARE


def profit(list_price):
    return list_price * DISCOUNT - full_cost(list_price)


def ok(list_price):
    return profit(list_price) >= RATE * full_cost(list_price)


lowest = None
for cents in range(1, 100001):            # 0.01 .. 1000.00 yuan
    p = F(cents, 100)
    if ok(p):
        lowest = p
        break
assert lowest is not None and not ok(lowest - F(1, 100))
assert all(ok(lowest + F(k, 4)) for k in range(1, 2001))   # keeps holding for higher prices

hits = [k for k, v in OPTIONS.items() if F(v) == lowest]
assert len(hits) == 1, (lowest, hits)
for k, v in OPTIONS.items():               # every other option fails the requirement
    if k != hits[0]:
        assert not ok(F(v)), (k, v)

# distractors reproduce the error paths named in the 解析
need = GOODS * (1 + RATE)                                           # 273.6
assert need / (DISCOUNT * (1 - SHARE)) == OPTIONS['C']             # share deducted but left out of the cost base
assert need / DISCOUNT == OPTIONS['A']                             # share forgotten altogether
assert lowest * DISCOUNT == OPTIONS['B']                           # stopped at the deal price
print('goods cost', GOODS, 'lowest list price', lowest, 'deal price', lowest * DISCOUNT,
      'full cost', full_cost(lowest), 'profit', profit(lowest))
print(hits[0])
