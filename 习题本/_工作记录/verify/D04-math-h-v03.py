# D04-math-h-v03: trade-in subsidies for a grade-1 air conditioner. National subsidy = 20% of the final price,
# at most 2000 yuan; then the city subsidy = 10% of (final price - national subsidy), at most 1000 yuan.
# After both subsidies the buyer paid 8100 yuan. Find the final price.
# Method: implement the two capped subsidies literally, scan every final price from 1 to 40000 yuan (and every
# half yuan as well), and keep the prices whose payment is exactly 8100; confirm the payment is strictly
# increasing in the price (so the solution is unique, integer or not). Then match against the options.
from fractions import Fraction as F

OPTIONS = {'A': 11000, 'B': 11100, 'C': 11250, 'D': 11375}
PAID = 8100


def subsidies(price):
    national = min(price * F(20, 100), F(2000))
    city = min((price - national) * F(10, 100), F(1000))
    return national, city


def pay(price):
    n, c = subsidies(price)
    return price - n - c


sols = [p for p in (F(k, 2) for k in range(1, 80001)) if pay(p) == PAID]
assert len(sols) == 1, sols
# strictly increasing: each linear piece has a positive slope, so no other real price pays 8100
prev = pay(F(0))
for k in range(1, 40001):
    cur = pay(F(k))
    assert cur > prev
    prev = cur
price = sols[0]
hits = [k for k, v in OPTIONS.items() if F(v) == price]
assert len(hits) == 1, (price, hits)

# which caps bind at the answer, and why each distractor fails
n, c = subsidies(price)
print('price', price, 'national', n, 'city', c, 'paid', pay(price))
for k, v in OPTIONS.items():
    print(k, v, '-> paid', pay(F(v)), 'subsidies', subsidies(F(v)))
# distractors reproduce the wrong "which cap binds" guesses named in the 解析
assert PAID + 2000 + 1000 == OPTIONS['B']                       # both capped assumed
assert F(PAID) / (F(8, 10) * F(9, 10)) == OPTIONS['C']          # neither capped assumed
assert (F(PAID) + 1000) / F(8, 10) == OPTIONS['D']              # only the city subsidy capped assumed
print(hits[0])
