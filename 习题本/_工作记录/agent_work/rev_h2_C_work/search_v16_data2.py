# Broader search: integer prices, cost integer or one decimal, r in {10%, 20%},
# 4th distractor from any of several real error paths that lands exactly on a 0.5% grid.
from fractions import Fraction as F
from math import isqrt

def exact_sqrt(q):
    if q <= 0:
        return None
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    return F(rn, rd) if rn * rn == n and rd * rd == d else None

def clean(r):
    return r is not None and 0 < r < F(1, 2) and (r * 200).denominator == 1

out = []
for r in (F(1, 10), F(1, 5)):
    keep = (1 - r) ** 2
    std = {r, 1 - keep, (1 - keep) / 2}
    for m in (F(1, 5), F(1, 4), F(3, 10), F(2, 5), F(1, 2)):
        for a in (F(3, 5), F(7, 10), F(3, 4), F(4, 5)):
            for p1 in range(8, 41):
                for p2 in range(4, p1):
                    if not (F(2, 5) * p1 <= p2 <= F(4, 5) * p1):
                        continue
                    avg = a * p1 + (1 - a) * p2
                    c = keep * avg / (1 + m)
                    if (c * 10).denominator != 1 or c < 3 or c >= p2:
                        continue
                    R = c * (1 + m)
                    paths = {}
                    s = exact_sqrt(R / (a * p1));               paths["drop clearance"] = None if s is None else 1 - s
                    s = exact_sqrt(R / p1);                     paths["all at full price"] = None if s is None else 1 - s
                    s = exact_sqrt(R / F(p1 + p2, 2));          paths["simple mean price"] = None if s is None else 1 - s
                    s = exact_sqrt(c / avg);                    paths["forget margin"] = None if s is None else 1 - s
                    s = exact_sqrt(c / (1 - m) / avg);          paths["margin on revenue"] = None if s is None else 1 - s
                    # linear-loss variants of the above
                    paths["linear+drop clearance"] = (1 - R / (a * p1)) / 2
                    paths["linear+forget margin"] = (1 - c / avg) / 2
                    paths["linear+margin on revenue"] = (1 - c / (1 - m) / avg) / 2
                    paths["total+drop clearance"] = 1 - R / (a * p1)
                    paths["total+forget margin"] = 1 - c / avg
                    good = {k: v for k, v in paths.items() if clean(v) and v not in std}
                    if good:
                        score = (c.denominator != 1) * 1
                        out.append((score, float(c), float(m), float(a), p1, p2, float(r), float(avg),
                                    {k: float(v * 100) for k, v in good.items()}))
out.sort(key=lambda t: (t[0], t[6], t[1]))
print(len(out), "candidates")
for row in out[:60]:
    print(row)
