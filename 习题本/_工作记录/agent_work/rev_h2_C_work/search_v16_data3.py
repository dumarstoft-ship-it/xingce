# r = 10% with INTEGER cost and integer prices; list error-path values to judge distractors.
from fractions import Fraction as F
from math import sqrt
r = F(1, 10); keep = (1 - r) ** 2
rows = []
for mp in range(10, 65, 5):
    m = F(mp, 100)
    for a in (F(7, 10), F(3, 4), F(4, 5)):
        for p1 in range(10, 31):
            for p2 in range(5, p1):
                if not (F(1, 2) * p1 <= p2 <= F(4, 5) * p1):
                    continue
                avg = a * p1 + (1 - a) * p2
                c = keep * avg / (1 + m)
                if c.denominator != 1 or c >= p2 or c < 5:
                    continue
                R = c * (1 + m)
                e = {
                    "drop_clear": 1 - sqrt(R / (a * p1)),
                    "forget_m": 1 - sqrt(c / avg),
                    "m_on_rev": 1 - sqrt(c / (1 - m) / avg),
                    "mean_px": 1 - sqrt(R / F(p1 + p2, 2)),
                }
                rows.append((int(c), mp, float(a), p1, p2, float(avg), {k: round(v * 100, 2) for k, v in e.items()}))
for row in rows:
    print(row)
