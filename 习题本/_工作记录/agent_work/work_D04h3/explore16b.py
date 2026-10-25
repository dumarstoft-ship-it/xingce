# v16 rework: reverse-solve the daily loss rate x from price/profit data.
# Look for data where (besides the linear-approx error and the 'answered two-day total' error)
# a third real error path gives a clean x below the correct one.
from fractions import Fraction as Fr
from math import isqrt

def sqrt_frac(q):
    # exact sqrt of a Fraction if it is a perfect square, else None
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return Fr(rn, rd)
    return None

def nice_pct(x):
    # percentage with at most one decimal
    v = x * 1000
    return v.denominator == 1

res = []
for xp in (5, 10, 15, 20):
    x = Fr(xp, 100)
    K = (1 - x) ** 2
    for Rp in range(10, 65, 5):
        R = Fr(Rp, 100)
        for sp in range(50, 95, 5):
            s = Fr(sp, 100)
            for kp in range(30, 90, 10):
                k = Fr(kp, 100)
                avg = s + (1 - s) * k
                errs = {}
                # profit-rate base error: cost = (1-R) * revenue
                K1 = K / (1 - R * R)
                if K1 < 1:
                    r1 = sqrt_frac(K1)
                    if r1 is not None and nice_pct(1 - r1):
                        errs['base'] = 1 - r1
                # forgot clearance revenue
                K2 = K * avg / s
                if K2 < 1:
                    r2 = sqrt_frac(K2)
                    if r2 is not None and nice_pct(1 - r2):
                        errs['noclear'] = 1 - r2
                # ignored the clearance discount (all at full price): gives larger x
                K3 = K * avg
                r3 = sqrt_frac(K3)
                if r3 is not None and nice_pct(1 - r3):
                    errs['nodisc'] = 1 - r3
                if any(k_ in errs for k_ in ('base', 'noclear')):
                    # find c (2 decimals) and P (integer) with K = c(1+R)/(P avg)
                    for P in range(10, 61):
                        c = K * P * avg / (1 + R)
                        if (c * 100).denominator == 1:
                            res.append((xp, Rp, sp, kp, P, float(c), {k_: float(v) for k_, v in errs.items()}))
                            break
for r in res:
    print(r)
print(len(res))
