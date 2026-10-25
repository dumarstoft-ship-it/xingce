# Search cleaner data for the bayberry (v16) item: cost c, margin m, fraction a sold at p1, rest at p2,
# 2-day compounding loss r. Want c with <=1 decimal, prices integer / .5, and a 4th distractor that is a
# real error path giving a clean percentage (multiple of 0.5%).
from fractions import Fraction as F
from math import isqrt

def exact_sqrt(q):
    """sqrt of a positive Fraction if rational, else None"""
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return F(rn, rd)
    return None

def clean_pct(r):
    """r as a fraction of 1; clean if multiple of 0.5% and in (0, 50%)"""
    if r is None or r <= 0 or r >= F(1, 2):
        return False
    return (r * 200).denominator == 1

def nice_money(x, places=1):
    return (x * 10 ** places).denominator == 1

results = []
for r in (F(1, 10), F(1, 5), F(1, 20)):
    keep = (1 - r) ** 2
    for m in (F(1, 10), F(1, 5), F(1, 4), F(3, 10), F(2, 5), F(1, 2)):
        for a in (F(3, 5), F(7, 10), F(3, 4), F(4, 5), F(9, 10)):
            for p1x2 in range(16, 81):          # p1 from 8 to 40 step .5
                p1 = F(p1x2, 2)
                for p2x2 in range(8, p1x2):     # p2 from 4 up to < p1
                    p2 = F(p2x2, 2)
                    if p2 > p1 * F(4, 5):       # clearance should be a real discount
                        continue
                    if p2 < p1 * F(2, 5):
                        continue
                    avg = a * p1 + (1 - a) * p2
                    c = keep * avg / (1 + m)
                    if not nice_money(c, 1) or c < 3 or c >= p2:
                        continue
                    need = keep
                    errs = {}
                    s = exact_sqrt(c * (1 + m) / (a * p1));            errs["drop_clearance"] = None if s is None else 1 - s
                    s = exact_sqrt(c * (1 + m) / p1);                  errs["all_at_p1"] = None if s is None else 1 - s
                    s = exact_sqrt(c * (1 + m) / ((p1 + p2) / 2));     errs["simple_mean"] = None if s is None else 1 - s
                    s = exact_sqrt(c / avg);                           errs["forget_margin"] = None if s is None else 1 - s
                    s = exact_sqrt(c / (1 - m) / avg);                 errs["margin_on_rev"] = None if s is None else 1 - s
                    good = {k: v for k, v in errs.items() if clean_pct(v)}
                    std = {1 - keep, (1 - keep) / 2, r}
                    good = {k: v for k, v in good.items() if v not in std}
                    if good:
                        p1_int = p1.denominator == 1
                        p2_int = p2.denominator == 1
                        c_int = c.denominator == 1
                        score = (not c_int) * 2 + (not p1_int) + (not p2_int)
                        results.append((score, float(c), float(m), float(a), float(p1), float(p2), float(r),
                                        {k: float(v * 100) for k, v in good.items()}))

results.sort(key=lambda t: (t[0], t[1]))
print(len(results), "candidates; best 40:")
for row in results[:40]:
    print(row)
