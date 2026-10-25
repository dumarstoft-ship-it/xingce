# D03-math-h-v03: from 6:30 on, terminals 甲 and 乙 each dispatch a bus every 8 minutes, simultaneously;
# every bus runs at the same constant speed and needs 48 minutes one way. How many buses coming from 乙
# does the 3rd bus leaving 甲 meet on the road (meetings inside a terminal do not count)?
# Method: build the timetable (minutes after midnight), give every bus its exact trajectory on a route of
# length L, and for each bus leaving 乙 look for a crossing with our bus strictly between the terminals
# (scan the overlap of the two trips on a 1/4-minute grid plus the exact crossing time).
from fractions import Fraction as F

FIRST, GAP, TRIP, N_BUS = 6 * 60 + 30, 8, 48, 120
OPTIONS = {'A': 8, 'B': 9, 'C': 11, 'D': 12}
L = F(1)


def x_from_jia(dep, t):           # position of a bus that left 甲 at dep (0 at 甲, L at 乙)
    return L * F(t - dep, TRIP)


def x_from_yi(dep, t):
    return L - L * F(t - dep, TRIP)


def meets_on_road(our_dep, their_dep, first=FIRST):
    if their_dep < first:
        return False              # no such bus in the timetable
    lo, hi = max(our_dep, their_dep), min(our_dep, their_dep) + TRIP
    if lo > hi:
        return False              # never on the road at the same time
    grid = [F(lo) + F(i, 4) for i in range(int((hi - lo) * 4) + 1)]
    diff = [x_from_jia(our_dep, t) - x_from_yi(their_dep, t) for t in grid]
    t_star = F(our_dep + their_dep + TRIP, 2)  # where the two linear positions coincide
    crossing = lo <= t_star <= hi and x_from_jia(our_dep, t_star) == x_from_yi(their_dep, t_star)
    assert crossing == (min(diff) <= 0 <= max(diff))
    return crossing and 0 < x_from_jia(our_dep, t_star) < L


deps = [FIRST + GAP * k for k in range(N_BUS)]
ours = deps[2]                                     # 3rd bus from 甲
met = [s for s in deps if meets_on_road(ours, s)]
count = len(met)
hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
# distractors: no first-bus limit; a meeting inside the 乙 terminal also counted; 2 x trip / gap
no_first = [ours - TRIP + GAP * k for k in range(-5, 20)]
assert sum(meets_on_road(ours, s, first=0) for s in no_first) == OPTIONS['C']
assert count + sum(1 for s in deps if s == ours + TRIP) == OPTIONS['B']
assert 2 * TRIP // GAP == OPTIONS['D']
print('our bus leaves', divmod(ours, 60), 'meets buses that left 乙 at', [divmod(s, 60) for s in met])
print(hits[0])
