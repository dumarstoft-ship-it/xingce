# D03-math-2-v12: high-speed elevator starts from rest, accelerates uniformly for 10 s, cruises at top speed for
# 30 s, decelerates uniformly for 10 s and stops exactly at the 240 m observation floor. Top speed in m/s?
# Method: for each option, integrate the speed-time profile numerically (midpoint rule with exact fractions,
# exact for piecewise-linear speed) and keep the option whose travelled distance is 240 m.
from fractions import Fraction as F

T_ACC, T_CRUISE, T_DEC, DIST = F(10), F(30), F(10), F(240)       # seconds, metres
OPTIONS = {'A': F(24, 5), 'B': F(6), 'C': F(8), 'D': F(48, 5)}


def speed(t, vmax):
    if t <= T_ACC:
        return vmax * t / T_ACC
    if t <= T_ACC + T_CRUISE:
        return vmax
    return vmax * (T_ACC + T_CRUISE + T_DEC - t) / T_DEC


def distance(vmax, n=500):
    total = T_ACC + T_CRUISE + T_DEC
    h = total / n
    return sum(speed((i + F(1, 2)) * h, vmax) * h for i in range(n))


hits = [k for k, v in OPTIONS.items() if distance(v) == DIST]
assert len(hits) == 1, hits
total = T_ACC + T_CRUISE + T_DEC
# distractors: average speed; cruise segment only; triangle formula over the whole 50 s
assert DIST / total == OPTIONS['A'] and DIST / T_CRUISE == OPTIONS['C'] and 2 * DIST / total == OPTIONS['D']
print('top speed', OPTIONS[hits[0]], 'm/s')
print(hits[0])
