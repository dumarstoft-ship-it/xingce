# Verify suggested cleaner data sets for v16 (same structure: 2-day compounding loss, 80% full price, rest clearance)
from fractions import Fraction as F
from math import sqrt

def check(name, c, m, a, p1, p2, opts):
    c, m, a, p1, p2 = F(c), F(m), F(a), F(p1), F(p2)
    avg = a * p1 + (1 - a) * p2
    keep = c * (1 + m) / avg
    print(f"--- {name}: cost {float(c)}, margin {float(m)*100:.0f}%, {float(a)*100:.0f}% @ {float(p1)}, rest @ {float(p2)}")
    print(f"    avg = {float(avg)}, avg/(1+m) = {float(avg/(1+m)):.4f}, (1-r)^2 = c(1+m)/avg = {keep} = {float(keep)}")
    hits = []
    for k, v in opts.items():
        r = F(v) / 100
        rate = (1 - r) ** 2 * avg / c - 1
        if rate == m:
            hits.append(k)
        print(f"    {k} {v}%: margin {float(rate)*100:.3f}%")
    print("    correct options:", hits)
    print(f"    error paths: linear {(1-float(keep))/2*100:.2f}%, total {(1-float(keep))*100:.2f}%, "
          f"drop-clearance {(1-sqrt(float(c*(1+m)/(a*p1))))*100:.2f}%, forget-margin {(1-sqrt(float(c/avg)))*100:.2f}%")

check("original", "10.53", "0.3", "0.8", 18, "12.5", {"A": "2.5", "B": "9.5", "C": "10", "D": "19"})
check("alt-1 integer", 9, "0.35", "0.8", 16, 11, {"A": "2.5", "B": "9.5", "C": "10", "D": "19"})
check("alt-2 keep 30%", "8.1", "0.3", "0.8", 14, 9, {"A": "3", "B": "9.5", "C": "10", "D": "19"})
