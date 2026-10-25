# D03-math-2-v11: cyclist rides along a bus route; a bus overtakes him every 18 min and one comes towards him
# every 9 min; all buses same constant speed, both terminals dispatch at the same interval T. Find T.
# Method: for each option T, the overtaking interval fixes the bus speed (cyclist speed = 1); then simulate a
# route of length 3000 with buses dispatched from both terminals (k*T), find every bus/cyclist meeting that
# happens on the route during minutes 300..700, and measure the intervals. Keep T only if they are 18 and 9.
from fractions import Fraction as F

A_OVER, B_ONCOMING = F(18), F(9)
OPTIONS = {'A': F(6), 'B': F(9), 'C': F(12), 'D': F(27, 2)}
ROUTE, X0 = F(3000), F(500)         # route length; cyclist position at t = 0 (moves towards the far end)
v = F(1)                            # cyclist speed (distance units per minute)
T0, T1 = 300, 700                   # observation window (cyclist stays on the route: 500+700 < 3000)


def pass_times(T, V, direction):
    out = []
    for k in range(-3000, 3000):
        dep = k * T
        if direction > 0:      # bus from terminal 0: x = V (t - dep); cyclist: x = X0 + v t
            t = (X0 + V * dep) / (V - v)
            x = V * (t - dep)
        else:                  # bus from terminal ROUTE: x = ROUTE - V (t - dep)
            t = (ROUTE - X0 + V * dep) / (V + v)
            x = ROUTE - V * (t - dep)
        if t >= dep and 0 <= x <= ROUTE and T0 <= t <= T1:
            assert x == X0 + v * t
            out.append(t)
    return sorted(out)


def intervals(ts):
    assert len(ts) >= 3
    return {b - a for a, b in zip(ts, ts[1:])}


ok = []
for k, T in OPTIONS.items():
    if T >= A_OVER:
        continue
    V = A_OVER * v / (A_OVER - T)                  # makes the overtaking interval equal 18 (checked below)
    over = intervals(pass_times(T, V, +1))
    onc = intervals(pass_times(T, V, -1))
    assert over == {A_OVER}, (k, over)
    if onc == {B_ONCOMING}:
        ok.append(k)
assert len(ok) == 1, ok
hit = ok[0]
# distractors: arithmetic mean; formula without the factor 2; "oncoming interval = dispatch interval"
assert (A_OVER + B_ONCOMING) / 2 == OPTIONS['D'] and A_OVER * B_ONCOMING / (A_OVER + B_ONCOMING) == OPTIONS['A']
assert B_ONCOMING == OPTIONS['B']
print('dispatch interval', OPTIONS[hit], 'min')
print(hit)
