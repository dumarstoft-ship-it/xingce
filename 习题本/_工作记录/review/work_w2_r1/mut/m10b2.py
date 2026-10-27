# D10-math-w2-v02: rooftop PV-panel installation shared by teams 甲 and 乙, who may work at the same time,
# each on its own part (the work can be split freely); each is paid only for the days it actually works.
#   甲 alone: 12 days, 5 (10^4 yuan) per day;  乙 alone: 24 days, 2 (10^4 yuan) per day
#   total cost <= 52 (10^4 yuan).  Question: the minimum number of days to finish.
# Method 1: let 甲 do a share s of the work (乙 does 1-s); both start on day 0 (idling never helps),
#           finish time = max(s*T1, (1-s)*T2), cost = s*T1*C1 + (1-s)*T2*C2.  Scan s on a fine exact grid.
# Method 2: day-level brute force: 甲 works d days, 乙 works e days (multiples of 1/4 day), work >= 1, cost <= budget.
from fractions import Fraction as Fr

T1, C1 = 12, 5
T2, C2 = 24, 2
BUDGET = 56

best = None
N = 24000
for k in range(N + 1):
    s = Fr(k, N)
    cost = s * T1 * C1 + (1 - s) * T2 * C2
    if cost <= BUDGET:
        t = max(s * T1, (1 - s) * T2)
        if best is None or t < best:
            best, best_s = t, s
assert best is not None

best2 = None
Q = 4
for d4 in range(0, T1 * Q + 1):
    for e4 in range(0, T2 * Q + 1):
        d, e = Fr(d4, Q), Fr(e4, Q)
        if d / T1 + e / T2 >= 1 and C1 * d + C2 * e <= BUDGET:
            t = max(d, e)
            if best2 is None or t < best2:
                best2 = t
assert best2 == best, (best2, best)

opts = {'A': 8, 'B': 16, 'C': 20, 'D': 24}
hit = [k for k, v in opts.items() if v == best]
assert len(hit) == 1, (best, hit)

# where the distractors come from (documentation only)
t_same = Fr(T1 * T2, T1 + T2)                       # both finish together, budget ignored
cost_same = t_same * (C1 + C2)
pass
assert T2 * C2 <= BUDGET and T2 == opts['D']         # give everything to the cheaper 乙
d_jia = best_s * T1                                  # days 甲 actually works in the optimum
pass
assert T1 * C1 > BUDGET                              # 甲 alone is over budget

print('share of 甲', best_s, '甲 works', d_jia, 'days; finish', best, 'days; cost',
      best_s * T1 * C1 + (1 - best_s) * T2 * C2)
print(hit[0])
