# Numeric checks for the deepening suggestions written into the review (not part of the key).
from fractions import Fraction as F

print('--- v01 idea: 20% target measured on ALL cost incl. mall share')
C = F(200) * F(11, 10) + 26          # freight 26 -> cost 246
d, k, r = F(9, 10), F(15, 100), F(1, 5)
# profit = 0.9P*0.85 - C >= r*(C + 0.9P*0.15)
P = C * (1 + r) / (d * (1 - k - r * k))
naive = C * (1 + r) / (d * (1 - k))
print('cost', C, 'P =', P, '; naive (share not in base) =', float(naive))
deal = d * P
assert (deal - deal * k - C) / (C + deal * k) == r

# search clean combos where both the right answer and the naive one are integers
hits = []
for C0 in range(150, 401):
    for d0 in (F(8, 10), F(9, 10)):
        for k0 in (F(1, 10), F(15, 100), F(2, 10)):
            for r0 in (F(1, 5), F(1, 4)):
                P0 = C0 * (1 + r0) / (d0 * (1 - k0 - r0 * k0))
                N0 = C0 * (1 + r0) / (d0 * (1 - k0))
                if P0.denominator == 1 and N0.denominator == 1:
                    hits.append((C0, float(d0), float(k0), float(r0), int(P0), int(N0)))
print('clean combos (cost, disc, share, rate, P, naive):', hits[:8])

print('--- v12+v15 merge idea: tiered variable cost + 成本利润率>=20%')
def ok_m(n):
    var = 40 * min(n, 6000) + 30 * max(n - 6000, 0)
    cost = 120000 + var
    return F(60 * n - cost, cost) >= F(1, 5)
nmin = next(n for n in range(1, 100000) if ok_m(n))
print('min n =', nmin)
# distractors: ignore tier (all 40) ; all at 30 ; profit/revenue>=20%
print('ignore tier:', next(n for n in range(1, 10**6) if F(60*n-(120000+40*n), 120000+40*n) >= F(1,5)))
print('all at 30:', next(n for n in range(1, 10**6) if F(60*n-(120000+30*n), 120000+30*n) >= F(1,5)))
def ok_rev(n):
    var = 40 * min(n, 6000) + 30 * max(n - 6000, 0)
    return 60 * n - 120000 - var >= F(1, 5) * 60 * n
print('profit/revenue reading:', next(n for n in range(1, 10**6) if ok_rev(n)))

print('--- v17 idea: same delivered quantity (960 sellable), loss 20% vs 4%')
S = 960
ship_o, ship_c = F(S) / F(8, 10), F(S) / F(96, 100)
cost_o = ship_o * (10 + 1)
cmax = (cost_o - ship_c * 10) / ship_c
print('ship ordinary', ship_o, 'cold', ship_c, 'cold freight max', cmax)
print('trap per-shipped logic: 0.16*30+1 =', F(16, 100) * 30 + 1, '; trap freight-only: ', F(1200, 1000))

print('--- v18 idea: buyout may return up to 300 unsold boxes at 12 each')
def buy(kk):
    return 60 * kk - 24 * 1500 + 12 * min(1500 - kk, 300)
def con(kk):
    return 30 * kk
kmin = next(kk for kk in range(0, 1501) if buy(kk) >= con(kk))
assert all(buy(kk) >= con(kk) for kk in range(kmin, 1501))
naive18 = next(kk for kk in range(0, 1501) if 60 * kk - 36000 + 12 * (1500 - kk) >= 30 * kk)
print('min sold =', kmin, '; ignore 300 cap =', naive18, '; ignore return = 1200')

print('--- v16 idea: reverse, find daily loss x given price 24 and 40%')
# (1-x)^2 * 0.875 * 24 = 1.4 * 12.15
val = F(1215, 100) * F(14, 10) / (F(7, 8) * 24)
print('(1-x)^2 =', val, '-> x = 10% ; linear trap (1-2x) gives x =', (1 - val) / 2)

print('--- v08 idea: integer batches where the EOQ is infeasible')
D, K, h = 3000, 160, 6
import math
x_star = math.sqrt(2 * D * K / h)
cands = {q: F(K * D, q) + F(h * q, 2) for q in range(1, D + 1) if D % q == 0}
best = min(cands, key=cands.get)
print('EOQ', x_star, 'feasible best', best, cands[best], 'neighbours', {q: float(cands[q]) for q in (300, 375, 500, 600)})
