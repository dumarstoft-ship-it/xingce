# D03-math-h-v02: teams 甲 and 乙 leave together for a village 18 km away along one road. One minibus
# (36 km/h) can carry one team at a time: it carries 甲 to some point, drops it (甲 walks on), turns back at
# once, meets 乙 (walking since the start), and drives 乙 to the village. Both teams arrive together.
# Walking speed 4 km/h; boarding and turning take no time. Find the total time in minutes.
# Method: simulate the whole trip for every drop-off point d = k/100 km (0 < d < 18) with exact rationals
# (bus to d; bus back until it meets 乙 at closing speed 36 + 4; bus on to the village; 甲 walks from d),
# keep the d where both arrival times are equal, and convert the common arrival time to minutes.
from fractions import Fraction as F

S, V_BUS, V_WALK = F(18), F(36), F(4)
OPTIONS = {'A': 45, 'B': 50, 'C': 54, 'D': 70}


def simulate(d):
    t_drop = d / V_BUS                              # 甲 gets off at d
    yi_at_drop = V_WALK * t_drop                    # 乙 has been walking
    t_pick = t_drop + (d - yi_at_drop) / (V_BUS + V_WALK)
    p = V_WALK * t_pick                             # where 乙 boards
    assert 0 < p < d
    t_yi = t_pick + (S - p) / V_BUS
    t_jia = t_drop + (S - d) / V_WALK
    return t_jia, t_yi, p, t_pick


good = [F(k, 100) for k in range(1, 1800) if simulate(F(k, 100))[0] == simulate(F(k, 100))[1]]
assert len(good) == 1, good
d = good[0]
# the arrival-time difference is linear in d: solve it exactly from two points as a cross-check
g = lambda x: simulate(x)[0] - simulate(x)[1]
x0, x1 = F(1), F(17)
assert x0 - g(x0) * (x1 - x0) / (g(x1) - g(x0)) == d
t_jia, t_yi, p, t_pick = simulate(d)
assert S - d == p                                   # both teams walk the same distance
total = t_jia * 60
hits = [k for k, v in OPTIONS.items() if v == total]
assert len(hits) == 1, (total, hits)
# distractors: only up to the pick-up; loaded legs only (empty return forgotten); x from S - x = 9x
assert t_pick * 60 == OPTIONS['A']
assert 2 * (S - p) / V_BUS * 60 == OPTIONS['B']
xa = S / (V_BUS / V_WALK + 1)
assert (xa / V_WALK + (S - xa) / V_BUS) * 60 == OPTIONS['C']
print('drop-off at', d, 'km; each team walks', S - d, 'km; total', total, 'min')
print(hits[0])
