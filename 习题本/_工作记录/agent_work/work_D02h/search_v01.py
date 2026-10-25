# search parameters for: three lines same quantity Q; after t hours A left r1, B left r2, C finished m minutes ago;
# new task M, C starts d hours late, all finish together; ask C's (or A's) share
from fractions import Fraction as F
from math import gcd
res = []
for t in [F(2), F(3), F(5,2), F(3,2)]:
    for m in [10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 48, 50]:
        tc = t - F(m, 60)
        if tc <= 0: continue
        for Q in range(60, 601, 10):
            c = F(Q) / tc
            if c.denominator != 1: continue
            for a in range(10, int(c), 5):
                for b in range(a + 5, int(c), 5):
                    r1 = Q - a * t; r2 = Q - b * t
                    if r1 <= 0 or r2 <= 0 or r1.denominator != 1 or r2.denominator != 1: continue
                    g = gcd(gcd(a, b), int(c))
                    ratio = (a // g, b // g, int(c) // g)
                    if ratio in [(2, 3, 4), (2, 3, 5)]: continue
                    if max(ratio) > 12: continue
                    for d in [F(1, 2), F(1), F(3, 2), F(2)]:
                        for M in range(100, 1201, 10):
                            T = (M + c * d) / (a + b + c)
                            if T <= d or T.denominator > 2: continue
                            C = c * (T - d); A = a * T; B = b * T
                            if any(x.denominator != 1 for x in (C, A, B)): continue
                            d1 = F(M) * c / (a + b + c)            # ratio split ignoring delay
                            cw = F(Q) / t                          # wrong C rate ignoring early finish
                            Tw = (M + cw * d) / (a + b + cw)
                            d2 = cw * (Tw - d)
                            d4 = F(M) * cw / (a + b + cw)
                            T3 = (M + (a + b) * d) / (a + b + c)  # delay applied to A,B instead
                            d3 = c * T3
                            cand = {'C': C, 'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4}
                            ints = {k: v for k, v in cand.items() if v.denominator == 1}
                            if not all(k in ints for k in ('d1', 'd3')): continue
                            if len(set(ints.values())) < len(ints): continue
                            res.append((t, m, Q, a, b, int(c), ratio, r1, r2, d, M, T, A, B, C, ints))
print(len(res))
import random
random.seed(1)
for r in res:
    t, m, Q, a, b, c, ratio, r1, r2, d, M, T, A, B, C, ints = r
    if 'd2' in ints or 'd4' in ints:
        print(f"t={t} m={m} Q={Q} rates={a},{b},{c} ratio={ratio} left={r1},{r2} d={d} M={M} T={T} A={A} B={B} C={C} ", {k: str(v) for k, v in ints.items()})
