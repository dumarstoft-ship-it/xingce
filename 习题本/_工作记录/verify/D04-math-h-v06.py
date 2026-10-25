# D04-math-h-v06: a swimming hall charged the same ticket price every day; now it sells weekday tickets at 50%
# and weekend tickets at 80% of that original price. Afterwards the weekday daily attendance becomes 3 times
# the old one, the weekend daily attendance
# rises 25%, and one week's ticket revenue (5 weekdays + 2 weekend days, no holidays) rises 20%.
# Before the change, the weekend daily attendance was how many times the weekday daily attendance?
# Method: weekday daily attendance w = 1 and original price 1 (both scale out); scan the weekend daily
# attendance v = 0.01 .. 50.00 with exact rationals and keep every v for which new weekly revenue
# = 1.2 x old weekly revenue. Then match against the options.
from fractions import Fraction as F

OPTIONS = {'A': 1.5, 'B': 2.5, 'C': 3.75, 'D': 7.5}
WD_PRICE, WE_PRICE = F(5, 10), F(8, 10)
WD_FACTOR, WE_FACTOR = F(3), F(125, 100)
REV_UP = F(20, 100)


def weekly(w, v, wd_price=F(1), we_price=F(1), wd_factor=F(1), we_factor=F(1)):
    return 5 * w * wd_factor * wd_price + 2 * v * we_factor * we_price


w = F(1)
sols = []
for k in range(1, 5001):
    v = F(k, 100)
    old = weekly(w, v)
    new = weekly(w, v, WD_PRICE, WE_PRICE, WD_FACTOR, WE_FACTOR)
    if new == old * (1 + REV_UP):
        sols.append(v)
assert len(sols) == 1, sols
ratio = sols[0] / w
print('weekend / weekday daily attendance before =', ratio)
hits = [k for k, x in OPTIONS.items() if F(str(x)) == ratio]
assert len(hits) == 1, hits

# the weekend revenue is unchanged (1.25 x 0.8 = 1)
assert WE_FACTOR * WE_PRICE == 1
# distractors reproduce the error paths named in the 解析
# (A) no 5-day / 2-day weighting: 0.5w = 0.2(w + v)
assert (WD_FACTOR * WD_PRICE - 1 - REV_UP) / REV_UP == F(str(OPTIONS['A']))
# (B) 20% taken of the new revenue: 2.5w = 0.2(7.5w + 2v)
inc = 5 * (WD_FACTOR * WD_PRICE - 1)
assert (inc - REV_UP * 5 * WD_FACTOR * WD_PRICE) / (2 * REV_UP) == F(str(OPTIONS['B']))
# (D) the two weekend days together
assert 2 * ratio == F(str(OPTIONS['D']))
print(hits[0])
