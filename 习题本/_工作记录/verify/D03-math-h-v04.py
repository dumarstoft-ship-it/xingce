# D03-math-h-v04: a freighter 100 km due west of port O sails due east towards O at 32 km/h; at the same
# moment a fishing boat leaves O due north at 24 km/h. Find the minimum distance between the two ships (km).
# Method: coordinates (x east, y north, O at the origin); the freighter stops when it reaches O. Evaluate the
# exact squared distance on a rational time grid (1/1000 h) over the first 10 hours, take the minimum, check
# it is a strict local minimum, cross-check with a golden-section search in floats, then match the options
# by comparing squares exactly.
from fractions import Fraction as F
import math

D0, V_FREIGHT, V_FISH = F(100), F(32), F(24)
OPTIONS = {'A': 48, 'B': 60, 'C': 75, 'D': 80}


def d2(t):
    x = -D0 + V_FREIGHT * min(t, D0 / V_FREIGHT)   # freighter, stops at O
    y = V_FISH * t                                 # fishing boat
    return x * x + y * y


grid = [F(k, 1000) for k in range(0, 10001)]
vals = [d2(t) for t in grid]
i = min(range(len(vals)), key=vals.__getitem__)
t_best, best = grid[i], vals[i]
assert 0 < i < len(vals) - 1 and vals[i - 1] > best < vals[i + 1]
lo, hi = 0.0, 10.0
for _ in range(200):
    m1, m2 = lo + (hi - lo) * 0.382, lo + (hi - lo) * 0.618
    if float(d2(F(m1))) < float(d2(F(m2))):
        hi = m2
    else:
        lo = m1
assert abs(math.sqrt(float(d2(F(lo)))) - math.sqrt(best)) < 1e-6
hits = [k for k, v in OPTIONS.items() if v * v == best]
assert len(hits) == 1, (best, hits)
# distractors: distance when the freighter reaches O; boat's distance from O at the closest moment;
# relative distance travelled until the closest moment
assert d2(D0 / V_FREIGHT) == OPTIONS['C'] ** 2
assert V_FISH * t_best == OPTIONS['A']
rel = math.hypot(V_FREIGHT, V_FISH)
assert rel * t_best == OPTIONS['D']
print('closest at t =', t_best, 'h, distance^2 =', best)
print(hits[0])
