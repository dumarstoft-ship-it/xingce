# D12-math-w2-v01: 4 bakery stores, 2000 orders in all, overall average order value 48 yuan.
# Store A: 400 orders at 40 yuan; stores B, C: averages 49 and 51 yuan, order counts unknown;
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


def rank_of(p, others):
    """rank (high to low) of value p among p and others = 1 + number strictly higher; plus ties."""
    return 1 + sum(1 for q in others if q > p), sum(1 for q in others if q == p)


ranks, ranks_any = set(), set()      # with / without the "D has the most orders" condition
vals = set()                         # distinct values of D's average (reduced fractions)
lo = hi = None                       # (P, nD, nB, nC) of the smallest / largest D average
n_ok = n_all = ties_seen = 0
for nD in range(1, R - 1):
    for nB in range(1, R - nD):
        nC = R - nD - nB             # >= 1
        P = T - nA * pA - nB * pB - nC * pC      # D's sales
        if P <= 0:                   # an average order value must be positive
            continue
        pD = F(P, nD)
        r, t = rank_of(pD, (pA, pB, pC))
        n_all += 1
        ranks_any.add(r)
        if not nD > max(nA, nB, nC):             # stem: D has the most orders
            continue
        n_ok += 1
        ties_seen += t
        ranks.add(r)
        vals.add(pD)
        if lo is None or pD < lo[0]:
            lo = (pD, nB, nC, nD)
        if hi is None or pD > hi[0]:
            hi = (pD, nB, nC, nD)

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
assert ties_seen == 0

# "D has the most orders" is needed: without it D's rank is not fixed
assert len(ranks_any) > 1
# the rank does not hinge on whole-number counts: real-valued splits with D the largest
random.seed(12)
checked = 0
while checked < 20000:
    u = [F(random.randint(1, 10**6), 10**6) for _ in range(3)]
    s = sum(u)
    xB, xC, xD = (R * x / s for x in u)
    if not xD > max(nA, xB, xC):
        continue
    pD = (T - nA * pA - xB * pB - xC * pC) / xD
    assert rank_of(pD, (pA, pB, pC)) == (min(ranks), 0)
    checked += 1

# where the wrong options come from
pkg = F(T - nA * pA, R)                                   # B+C+D taken as one block
near_overall = rank_of(F(M), (pA, pB, pC))[0]             # "the biggest store sits at the overall average"
plain_mean = 4 * M - (pA + pB + pC)                       # misreading 48 as a plain mean of 4 stores
print('feasible splits (D most):', n_ok, '| all positive splits:', n_all)
print('ranks of D:', sorted(ranks), '| ranks without the "most" condition:', sorted(ranks_any))
print('distinct values of D average:', len(vals), '| range %.4f (B=%d, C=%d, D=%d) .. %.4f (B=%d, C=%d, D=%d)'
      % (float(lo[0]), lo[1], lo[2], lo[3], float(hi[0]), hi[1], hi[2], hi[3]))
print('block B+C+D average:', pkg, '| B, C are', pB - pkg, pC - pkg, 'off it, so D = %s + (nB - nC)/nD' % pkg)
print('distractors: D at overall %d -> rank %d (%s); plain mean gives D=%d -> rank %d (%s); no "most" -> %s'
      % (M, near_overall, RANK_WORD[near_overall], plain_mean, rank_of(plain_mean, (pA, pB, pC))[0],
         RANK_WORD[rank_of(plain_mean, (pA, pB, pC))[0]], '无法确定'))
print('option truth:', truth)
print(hit[0])
