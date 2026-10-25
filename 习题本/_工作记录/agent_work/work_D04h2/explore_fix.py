import math
from fractions import Fraction as F
print('--- v08 new: D=3000, K=160, h=6')
D, K, h = 3000, 160, 6
cost = lambda x: F(K * D, x) + F(h * x, 2)
xs = math.sqrt(2 * D * K / h); print('theory x* =', xs, 'batches', D / xs)
feas = sorted(D // n for n in range(1, D + 1) if D % n == 0)
best = min(feas, key=cost); print('best feasible', best, cost(best))
for x in (250, 300, 375, 400, 500, 600):
    print(x, 'feasible' if D % x == 0 else 'INFEASIBLE', float(cost(x)))
print('forgot half x =', math.sqrt(D * K / h))
wrong = lambda x: F(K * D, x) + h * x
print('forgot-half costs 250/300/375:', [float(wrong(x)) for x in (250, 300, 375)])
print('n=7 (428.57 bags) cost', float(F(K * 7) + F(h, 2) * F(D, 7)))
print('--- v12 merged: F=120000, p=60, v=40 first 6000, 30 beyond, margin>=20%')
def tc(q, var_beyond_slip=False):
    v = 40 * min(q, 6000) + (30 * q if var_beyond_slip and q > 6000 else 30 * max(q - 6000, 0))
    return 120000 + v
def first(cond):
    return next(q for q in range(1, 10**6) if cond(q))
print('correct', first(lambda q: 5 * (60 * q - tc(q)) >= tc(q)))
print('ignore segments (all 40)', first(lambda q: 5 * (20 * q - 120000) >= 120000 + 40 * q))
print('all at 30', first(lambda q: 5 * (30 * q - 120000) >= 120000 + 30 * q))
print('profit/revenue, segmented', first(lambda q: 5 * (60 * q - tc(q)) >= 60 * q))
print('profit/revenue, ignore segs', first(lambda q: 5 * (20 * q - 120000) >= 60 * q))
print('beyond part not minus 6000', first(lambda q: q > 6000 and 5 * (60 * q - tc(q, True)) >= tc(q, True)))
print('target = 20% of fixed only, segmented', first(lambda q: 60 * q - tc(q) >= 24000))
print('denominator variable only, segmented', first(lambda q: 5 * (60 * q - tc(q)) >= tc(q) - 120000))
