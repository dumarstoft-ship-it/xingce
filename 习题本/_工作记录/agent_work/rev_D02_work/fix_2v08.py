# Check suggested replacement numbers for D02-math-2-v08: +25% efficiency -> 6 days early; switch later -> 4 days early
from fractions import Fraction as F
UP, E_ALL, E_PART = F(5, 4), 6, 4
Ts = [T for T in range(1, 500) if T - F(T) / UP == E_ALL]
assert len(Ts) == 1
T = Ts[0]
def actual(x):
    e = F(1, T)
    return x + (1 - e * x) / (e * UP)
xs = [x for x in range(0, T + 1) if T - actual(x) == E_PART]
assert len(xs) == 1
x = xs[0]
opts = {'A': 6, 'B': 8, 'C': 10, 'D': 20}
hits = [k for k, v in opts.items() if v == x]
assert len(hits) == 1
# distractors
assert T * F(E_PART, E_ALL) == opts['D']                     # proportion reversed
Tw = F(E_ALL) / F(1, 4)                                      # took "+25% efficiency" as "-25% time"
assert Tw - F(E_PART) / F(1, 4) == opts['B']
assert (T - E_PART) - T * F(E_PART, E_ALL) == opts['A']     # 26 - 20
print('T', T, 'x', x, hits)
