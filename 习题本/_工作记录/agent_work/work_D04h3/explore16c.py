# v16 rework, broader search: clearance price given in yuan (a), full price P, full-price share s.
# Correct: (1-x)^2 = c(1+R) / (s*P + (1-s)*a), x = 10%.
# Want the 'forgot clearance revenue' error  (1-x2)^2 = c(1+R)/(s*P)  to give a clean x2 < 10%,
# or the 'profit-rate base' error (1-x3)^2 = c/((1-R)(s*P+(1-s)*a)) clean.
from fractions import Fraction as Fr
from math import isqrt

def sqrt_frac(q):
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    return Fr(rn, rd) if rn * rn == n and rd * rd == d else None

def nice(x):
    return (x * 1000).denominator == 1 and x > 0

out = []
x = Fr(1, 10)
K = (1 - x) ** 2
for sp in range(50, 100, 5):
    s = Fr(sp, 100)
    for P in range(12, 41):
        for a2 in range(1, 2 * P):
            a = Fr(a2, 2)
            rev = s * P + (1 - s) * a          # revenue per sellable jin
            for Rp in range(10, 65, 5):
                R = Fr(Rp, 100)
                c = K * rev / (1 + R)
                if (c * 100).denominator != 1:
                    continue
                K2 = c * (1 + R) / (s * P)
                r2 = sqrt_frac(K2) if K2 < 1 else None
                K3 = c / ((1 - R) * rev)
                r3 = sqrt_frac(K3) if K3 < 1 else None
                hit = {}
                if r2 is not None and nice(1 - r2): hit['noclear'] = float(1 - r2)
                if r3 is not None and nice(1 - r3): hit['base'] = float(1 - r3)
                if hit:
                    out.append((sp, P, float(a), Rp, float(c), hit))
for o in out[:60]:
    print(o)
print(len(out))
