# D03-math-2-v01: straight walkway AB = 900 m; 甲 (70 m/min) and 乙 (50 m/min) both start at A, walk back and
# forth between A and B, turning instantly at the ends. Where (distance from A) is their 2nd head-on meeting?
# Method: event-based simulation of two bouncing walkers (exact fractions); every meeting is classified as
# head-on (opposite directions) or overtaking (same direction); take the 2nd head-on one.
from fractions import Fraction as F

S, V1, V2 = F(900), F(70), F(50)
OPTIONS = {'A': 300, 'B': 600, 'C': 675, 'D': 750}


def state(d):
    """position (from A) and direction just after having walked distance d from A, bouncing at both ends"""
    k, r = divmod(d, S)
    return (r, 1) if k % 2 == 0 else (S - r, -1)


horizon = F(300)
events = {F(0), horizon}
for v in (V1, V2):
    k = 1
    while k * S / v <= horizon:
        events.add(k * S / v)
        k += 1
ts = sorted(events)
meet = []
for a, b in zip(ts, ts[1:]):
    (p1, d1), (p2, d2) = state(V1 * a), state(V2 * a)
    rel = d1 * V1 - d2 * V2
    if rel == 0:
        continue
    t = a + (p2 - p1) / rel
    if a <= t <= b and t > 0 and (not meet or meet[-1][0] != t):
        meet.append((t, p1 + d1 * V1 * (t - a), 'head-on' if d1 != d2 else 'overtake'))

head_on = [m for m in meet if m[2] == 'head-on']
t2, pos2, _ = head_on[1]
# cross-check: both walkers really are at the same point at t2
assert state(V1 * t2)[0] == state(V2 * t2)[0] == pos2
assert all(m[2] == 'head-on' for m in meet if m[0] <= t2)   # no overtaking happens before it
hits = [k for k, v in OPTIONS.items() if v == pos2]
assert len(hits) == 1, (pos2, hits)
# distractor sources: distance from B; first head-on point; "(2n-1) full lengths" misuse (乙's position)
assert S - pos2 == OPTIONS['B'] and head_on[0][1] == OPTIONS['D']
assert state(V2 * 3 * S / (V1 + V2))[0] == OPTIONS['C']
print('meetings:', [(float(t), float(p), k) for t, p, k in meet[:4]])
print(hits[0])
