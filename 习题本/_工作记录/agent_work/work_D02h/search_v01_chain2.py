from fractions import Fraction as F
from math import gcd
res = []
for c in range(40, 121, 5):
    for b in range(20, c, 5):
        for a in range(10, b, 5):
            if a + b == c: continue
            g = gcd(gcd(a, b), c); ratio = (a // g, b // g, c // g)
            if max(ratio) > 9 or ratio in [(2, 3, 4), (2, 3, 5)]: continue
            if c > 3 * a: continue
            for Q in range(150, 451, 10):
                tc = F(Q, c); tb = F(Q, b)
                if (tc * 60).denominator != 1 or (tc * 60) % 10 or (tb * 60).denominator != 1 or (tb * 60) % 2: continue
                r1 = Q - b * tc; r2 = Q - a * tb
                if r1.denominator != 1 or r2.denominator != 1 or r1 <= 0 or r2 <= 0: continue
                if r1 * 2 == Q or r2 * 4 == Q or r2 * 2 == Q: continue
                for d in (F(1),):
                    for M in range(300, 1001, 10):
                        S = a + b + c
                        T = (M + c * d) / S
                        if T <= d or T.denominator != 1: continue
                        C = c * (T - d); R = F(M * c, S); naive = R - c * d; forget = c * T
                        vals = [C, R, naive, forget]
                        if any(v.denominator != 1 for v in vals) or len(set(vals)) < 4: continue
                        res.append((Q, a, b, c, ratio, tc, r1, tb, r2, d, M, T, [int(v) for v in vals]))
print(len(res))
for r in res[:40]:
    Q, a, b, c, ratio, tc, r1, tb, r2, d, M, T, v = r
    print(f"Q={Q} rates={a},{b},{c} {ratio} tc={float(tc)}h r1={r1} tb={float(tb)}h r2={r2} M={M} T={T} [C,R,naive,forget]={v}")
