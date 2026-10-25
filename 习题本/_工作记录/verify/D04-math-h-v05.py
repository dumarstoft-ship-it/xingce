# D04-math-h-v05: unit cost of a dining chair rises 20%, the factory raises its ex-factory price 10%, and the
# profit rate (profit / cost) ends up 10 percentage points lower than before. Find the original profit rate.
# Method: scan original profit rates r = 0.1%, 0.2%, ..., 300% with exact rationals (cost 100, price
# 100(1+r)), recompute the new profit rate from the new cost and new price, keep every r whose drop is
# exactly 10 percentage points. Then check each option directly.
from fractions import Fraction as F

OPTIONS = {'A': 10, 'B': 15, 'C': 20, 'D': 25}
COST_UP, PRICE_UP, DROP = F(20, 100), F(10, 100), F(10, 100)


def new_rate(r):
    cost, price = F(100), F(100) * (1 + r)
    cost2, price2 = cost * (1 + COST_UP), price * (1 + PRICE_UP)
    return (price2 - cost2) / cost2


sols = [F(k, 1000) for k in range(1, 3001) if F(k, 1000) - new_rate(F(k, 1000)) == DROP]
assert len(sols) == 1, sols
r = sols[0]
print('original rate', r * 100, '% ; new rate', new_rate(r) * 100, '%')
hits = []
for k, v in OPTIONS.items():
    rv = F(v, 100)
    drop_pts = (rv - new_rate(rv)) * 100
    print(k, v, '% -> drop', float(drop_pts), 'points')
    if drop_pts == 10:
        hits.append(k)
assert len(hits) == 1 and F(OPTIONS[hits[0]], 100) == r, hits
# distractor A is the new rate; B and D drop by about 9.6 / 10.4 points (near misses for rough substitution)
assert new_rate(r) * 100 == OPTIONS['A']
assert abs((F(15, 100) - new_rate(F(15, 100))) * 100 - F(96, 10)) < F(5, 100)
assert abs((F(25, 100) - new_rate(F(25, 100))) * 100 - F(104, 10)) < F(5, 100)
print(hits[0])
