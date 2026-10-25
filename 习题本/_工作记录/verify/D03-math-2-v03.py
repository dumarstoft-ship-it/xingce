# D03-math-2-v03: loop ride; 甲 16 min/lap, 乙 24 min/lap, start half a lap apart, ride towards each other.
# How many laps has 乙 ridden at their 3rd meeting?
# Method: loop length 48 units (so speeds are integers 3 and 2 units/min); step time exactly by 1/10 min and
# record the instants when the two positions coincide on the loop.
from fractions import Fraction as F

T1, T2 = 16, 24
L = 48
v1, v2 = F(L, T1), F(L, T2)          # 甲 clockwise, 乙 counter-clockwise
x1_0, x2_0 = F(0), F(L, 2)
OPTIONS = {'A': F(1), 'B': F(6, 5), 'C': F(3, 2), 'D': F(5, 2)}

meet, t, step = [], F(0), F(1, 10)
while len(meet) < 3:
    t += step
    p1 = (x1_0 + v1 * t) % L
    p2 = (x2_0 - v2 * t) % L
    if p1 == p2:
        meet.append(t)
t3 = meet[2]
laps_yi = v2 * t3 / L
hits = [k for k, v in OPTIONS.items() if v == laps_yi]
assert len(hits) == 1, (laps_yi, hits)
# distractors: 3 laps together (x 2/5); 甲's laps; laps of both together
assert 3 * F(2, 5) == OPTIONS['B'] and v1 * t3 / L == OPTIONS['C'] and (v1 + v2) * t3 / L == OPTIONS['D']
print('meeting times', [float(x) for x in meet], '乙 laps', laps_yi)
print(hits[0])
