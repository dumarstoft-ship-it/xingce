# D11-math-w2-v07: three liner routes at a port; route ships call "every other 7 / 9 / 11 days"
# (i.e. there are 7 / 9 / 11 days between two calls), all three called on 1 June.
# Question: in 1 June - 31 July (both ends included), on how many days did exactly one route's ship call?
# Method: walk the calendar day by day; a route calls on day d iff (d - 1 June) is a multiple of (gap + 1).
from datetime import date, timedelta
from math import lcm

GAPS = (6, 9, 11)
START, END = date(2026, 6, 1), date(2026, 7, 31)
periods = [g + 1 for g in GAPS]

def exactly_one_days(pers):
    n, d = 0, START
    while d <= END:
        k = sum((d - START).days % p == 0 for p in pers)
        n += (k == 1)
        d += timedelta(days=1)
    return n

ans = exactly_one_days(periods)

opts = {'A': 10, 'B': 15, 'C': 18, 'D': 19}
hit = [k for k, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)

# distractors (documentation only)
L = (END - START).days                      # offsets 0..L
cnt = lambda p: L // p + 1
singles = sum(cnt(p) for p in periods)
pairs_lcm = [cnt(lcm(a, b)) for a, b in ((8, 10), (8, 12), (10, 12))]
triple = cnt(lcm(*periods))
assert singles - 2 * sum(pairs_lcm) + 3 * triple == ans
pairs_prod = [cnt(a * b) for a, b in ((8, 10), (8, 12), (10, 12))]
use_product = singles - 2 * sum(pairs_prod) + 3 * cnt(8 * 10 * 12)
at_least_one = singles - sum(pairs_lcm) + triple
gap_as_period = exactly_one_days(list(GAPS))  # read "every other 7 days" as every 7 days
assert [at_least_one, use_product, gap_as_period] == [opts['B'], opts['C'], opts['D']], (at_least_one, use_product, gap_as_period)
# 31 July is day offset 60: routes with periods 10 and 12 meet there (a common period), 1 June has all three
assert [(L % p == 0) for p in periods] == [False, True, True]

print('days', L + 1, 'singles', singles, 'pairs', pairs_lcm, 'triple', triple, 'exactly one', ans)
print(hit[0])
