# D04-math-h-v04: a convenience store raises the price of a bottled herbal tea by 10%; its daily sales volume
# falls 20%, yet the daily profit from it rises 20%. The purchase price is unchanged. Before the price rise,
# the profit per bottle was what percentage of the purchase price?
# Method: fix an original price and volume, scan purchase prices on a 0.01 grid below the price and keep every
# one for which new daily profit = 1.2 x old daily profit exactly; repeat for several original prices to show
# the answer (profit / purchase price) does not depend on them. Then match against the options.
from fractions import Fraction as F

OPTIONS = {'A': 25, 'B': 37.5, 'C': 50, 'D': 100}
PRICE_UP, VOL_DOWN, PROFIT_UP = F(10, 100), F(20, 100), F(20, 100)

rates = set()
for price in (F(10), F(37), F(100), F(250)):
    volume = F(500)
    found = []
    for k in range(1, int(price * 100)):
        cost = F(k, 100)
        old = (price - cost) * volume
        new = (price * (1 + PRICE_UP) - cost) * volume * (1 - VOL_DOWN)
        if new == old * (1 + PROFIT_UP):
            found.append(cost)
    assert len(found) == 1, (price, found)
    cost = found[0]
    rates.add((price - cost) / cost * 100)
assert len(rates) == 1, rates
rate = rates.pop()
print('profit / purchase price before the rise =', rate, '%')
hits = [k for k, v in OPTIONS.items() if F(str(v)) == rate]
assert len(hits) == 1, hits

# distractors reproduce the error paths named in the 解析 (price 10, cost 8 scale)
p, c = F(10), F(8)
assert (p * (1 + PRICE_UP) - c) / c * 100 == F(str(OPTIONS['B']))   # rate after the price rise
ratio = (1 + PROFIT_UP) / (1 - VOL_DOWN)
assert (ratio - 1) * 100 == OPTIONS['C']                            # growth of the unit profit
# volume change ignored: unit profit taken to rise 20%, so 0.2u = 0.1 x price
u = F(1); p2 = PROFIT_UP * u / PRICE_UP
assert u / (p2 - u) * 100 == OPTIONS['D']
print(hits[0])
