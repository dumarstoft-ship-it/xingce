from fractions import Fraction as F
from math import gcd
out = []
for t in [F(2), F(3)]:
    for m in [15, 24, 30, 36, 40, 45]:
        tc = t - F(m, 60)
        for Q in range(60, 361, 10):
            c = F(Q) / tc
            if c.denominator != 1: continue
            c = int(c)
            for a in range(5, c, 5):
                for b in range(a + 5, c, 5):
                    r1 = Q - a * t; r2 = Q - b * t
                    if r2 < 10 or r1.denominator != 1 or r2.denominator != 1: continue
                    if c > 3 * a: continue
                    g = gcd(gcd(a, b), c)
                    ratio = (a // g, b // g, c // g)
                    if ratio in [(2, 3, 4), (2, 3, 5)] or max(ratio) > 8: continue
                    for d in [F(1), F(3, 2), F(1, 2)]:
                        for M in range(200, 1001, 10):
                            T = (M + c * d) / (a + b + c)
                            if T <= d or T.denominator != 1: continue
                            C = c * (T - d); A = a * T; B = b * T
                            d1 = F(M) * c / (a + b + c)
                            cw = F(Q) / t
                            Tw = (M + cw * d) / (a + b + cw); d2 = cw * (Tw - d)
                            d4 = F(M) * cw / (a + b + cw)
                            T3 = (M + (a + b) * d) / (a + b + c); d3 = c * T3
                            A1 = F(M) * a / (a + b + c)   # A share if ratio split ignoring delay
                            cand = dict(C=C, d1=d1, d2=d2, d3=d3, d4=d4, A=A, A1=A1, A3=a*(T3-d))
                            ints = {k: v for k, v in cand.items() if v.denominator == 1}
                            if not all(k in ints for k in ('d1', 'd3')): continue
                            if not ('d2' in ints or 'd4' in ints): continue
                            out.append((float(T), t, m, Q, a, b, c, ratio, r1, r2, d, M, T, A, B, C, {k: str(v) for k, v in ints.items()}))
out.sort(key=lambda r: (max(r[7]), r[3]))
for r in out[:120]:
    _, t, m, Q, a, b, c, ratio, r1, r2, d, M, T, A, B, C, ints = r
    print(f"t={t} m={m} Q={Q} rates={a},{b},{c} ratio={ratio} left={r1},{r2} d={d} M={M} T={T} A={A} B={B} C={C}", ints)
print(len(out))
