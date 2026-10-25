# D03-math-2-v07: ports A (upstream) and B, 72 km apart. Downstream A->B 3 h, upstream B->A 4 h.
# New engine: still-water speed becomes 30 km/h, current unchanged. Time for B->A upstream?
# Method: solve the 2x2 linear system boat+current = 72/3, boat-current = 72/4 (Cramer's rule), then recompute;
# cross-check by stepping the upstream trip minute by minute.
from fractions import Fraction as F

D, t_down, t_up, new_boat = F(72), F(3), F(4), F(30)
OPTIONS = {'A': F(144), 'B': F(160), 'C': F(168), 'D': F(180)}       # minutes: 2h24, 2h40, 2h48, 3h
LABEL = {'A': '2小时24分', 'B': '2小时40分', 'C': '2小时48分', 'D': '3小时'}
for k, v in OPTIONS.items():
    h, m = divmod(v, 60)
    assert LABEL[k] == (f'{h}小时{m}分' if m else f'{h}小时')

# [1 1; 1 -1] [b; w] = [D/t_down; D/t_up]
r1, r2 = D / t_down, D / t_up
det = F(1) * (-1) - F(1) * 1
b = (r1 * (-1) - 1 * r2) / det
w = (1 * r2 - r1 * 1) / det
assert b + w == r1 and b - w == r2 and w > 0
up_new = new_boat - w
T = D / up_new * 60                                       # minutes
# minute-by-minute check
pos, minutes = F(0), 0
while pos < D:
    pos += up_new / 60
    minutes += 1
assert minutes == T
hits = [k for k, v in OPTIONS.items() if v == T]
assert len(hits) == 1, (T, hits)
# distractors: ignore current; current taken as (24-18) without halving; time inversely prop. to boat speed
assert D / new_boat * 60 == OPTIONS['A'] and D / (new_boat - (r1 - r2)) * 60 == OPTIONS['D']
assert t_up * b / new_boat * 60 == OPTIONS['C']
print('boat', b, 'current', w, 'new upstream', up_new, 'time', T, 'min')
print(hits[0])
