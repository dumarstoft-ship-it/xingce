# D12-math-w2-v01: 4 bakery stores, 2000 orders in all, overall average order value 48 yuan.
# Store A: 400 orders at 40 yuan; stores B, C: averages 49 and 46 yuan, order counts unknown;
# store D: count and average unknown, but D has the most orders of the four.
# Question: where does D's average order value rank among the 4 stores (high to low)?
# Options: first / second / third / cannot be determined.
#
# Solve from the stem data: enumerate every positive-integer split (nB, nC, nD) of the
# remaining orders, keep the splits allowed by the stem, derive D's average from the total
# sales, and collect D's rank. Then decide which of the four options is true.
import random
from fractions import Fraction as F
from math import gcd

N, M = 2000, 48            # orders of the 4 stores, overall average order value (yuan)
nA, pA = 400, 40           # store A: orders, average order value
pB, pC = 49, 51            # stores B, C: average order value (order counts unknown)
opts = {'A': '第一', 'B': '第二', 'C': '第三', 'D': '无法确定'}
RANK_WORD = {1: '第一', 2: '第二', 3: '第三', 4: '第四'}

T = N * M                  # total sales of the 4 stores
R = N - nA                 # orders of B, C, D together


def rank_of_D(P, nD):
    """D's average is P/nD; rank = 1 + number of stores strictly higher; also report ties."""
    higher = sum(1 for p in (pA, pB, pC) if p * nD > P)
    ties = sum(1 for p in (pA, pB, pC) if p * nD == P)
    return 1 + higher, ties


ranks, ranks_any = set(), set()      # with / without the "D has the most orders" condition
vals = set()                         # distinct values of D's average (reduced fractions)
lo = hi = None                       # (P, nD) of the smallest / largest D average
n_ok = n_all = ties_seen = 0
for nD in range(1, R - 1):
    for nB in range(1, R - nD):
        nC = R - nD - nB             # >= 1
        P = T - nA * pA - nB * pB - nC * pC      # D's sales
        if P <= 0:                   # an average order value must be positive
            continue
        r, t = rank_of_D(P, nD)
        n_all += 1
        ranks_any.add(r)
        if not nD > max(nA, nB, nC):             # stem: D has the most orders
            continue
        n_ok += 1
        ties_seen += t
        ranks.add(r)
        g = gcd(P, nD)
        vals.add((P // g, nD // g))
        if lo is None or P * lo[1] < lo[0] * nD:
            lo = (P, nD, nB, nC)
        if hi is None or P * hi[1] > hi[0] * nD:
            hi = (P, nD, nB, nC)

assert n_ok > 0, 'no split satisfies the stem'

# which options are true
truth = {}
for k, txt in opts.items():
    if txt == '无法确定':
        truth[k] = len(ranks) > 1
    else:
        truth[k] = ranks == {r for r, w in RANK_WORD.items() if w == txt}
hit = [k for k, v in truth.items() if v]
assert len(hit) == 1, (ranks, truth)

# the rank does not hinge on whole-number counts or on "D has the most orders"
gap = nA * (M - pA)                  # A's shortfall below the overall average
cap = (N - nA) * (pB - M)            # most that B and D can make up if D <= B
assert gap > cap
pass
random.seed(12)
for _ in range(20000):               # real-valued (continuous) splits
    u = [F(random.randint(1, 10**6), 10**6) for _ in range(3)]
    s = sum(u)
    xB, xC, xD = (R * x / s for x in u)
    pD = (T - nA * pA - xB * pB - xC * pC) / xD
    pass

print('feasible splits (D most):', n_ok, '| all positive splits:', n_all)
print('ranks of D:', sorted(ranks), '| ties seen:', ties_seen, '| ranks without the "most" condition:', sorted(ranks_any))
print('distinct values of D average:', len(vals), '| range %.3f (B=%d, C=%d, D=%d) .. %.3f (B=%d, C=%d, D=%d)'
      % (lo[0] / lo[1], lo[2], lo[3], lo[1], hi[0] / hi[1], hi[2], hi[3], hi[1]))
print('package B+C+D average:', F(T - nA * pA, R), '| A gap', gap, '> B-cap', cap)
print('option truth:', truth)
print(hit[0])
