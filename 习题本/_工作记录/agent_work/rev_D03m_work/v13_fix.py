from fractions import Fraction as F
def min_gap_after_rest_start(vb, dt=F(1, 600), horizon=F(12)):
    va = vb + 4; t = F(5, 2); best = None
    while t <= horizon:
        if t <= F(5, 2) + F(2, 3):
            pa = va * F(5, 2)
        else:
            pa = va * F(5, 2) + va * (t - F(5, 2) - F(2, 3))
        gap = pa - vb * t
        best = gap if best is None else min(best, gap)
        t += dt
    return best
for vb in [14, F(299, 20), 15, 16, 19, 25]:
    print('1-v13 v乙=', vb, 'min gap from 2.5h on =', float(min_gap_after_rest_start(F(vb))))
# 2-v02 dense float scan using closed-form head-on rule (combined=(2k-1)L) cross-checked by event sim
def tri(x, L):
    x %= 2 * L
    return x if x <= L else 2 * L - x
hits = []
L = 40.01
while L < 1000:
    if abs(tri(120, L) - 60) < 1e-6:
        hits.append(round(L, 4))
    L += 0.01
print('2-v02 dense scan hits:', sorted(set(hits)))
