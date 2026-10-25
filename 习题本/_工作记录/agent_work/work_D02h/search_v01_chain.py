# chain progress: each line Q, start 8:00. C finishes at tc=Q/c; then B has r1 left; B finishes at tb=Q/b; then A has r2 left.
# next day: M items, C starts d hours late, all finish together. Ask C's share.
from fractions import Fraction as F
from math import gcd
res = []
for c in range(40, 121, 5):
    for b in range(20, c, 5):
        for a in range(10, b, 5):
            if a + b == c: continue                      # avoid AP option sets
            g = gcd(gcd(a, b), c); ratio = (a // g, b // g, c // g)
            if max(ratio) > 12 or ratio in [(2, 3, 4), (2, 3, 5)]: continue
            for Q in range(100, 601, 10):
                tc = F(Q, c)
                if (tc * 60).denominator != 1 or (tc * 60) % 10: continue   # finish on a 10-minute mark
                r1 = Q - b * tc
                tb = F(Q, b)
                r2 = Q - a * tb
                if r1.denominator != 1 or r2.denominator != 1 or r1 <= 0 or r2 <= 0: continue
                for d in (F(1), F(1, 2), F(3, 2)):
                    for M in range(200, 1201, 10):
                        S = a + b + c
                        T = (M + c * d) / S
                        if T <= d or (T * 2).denominator != 1: continue
                        C = c * (T - d)
                        R = F(M * c, S); naive = R - c * d; forget = c * T
                        aw = (Q - r2) / tc                     # chain error: A's remainder read at C's finish time
                        Tw = (M + c * d) / (aw + b + c); Cw = c * (Tw - d)
                        vals = {'C': C, 'R': R, 'naive': naive, 'forget': forget, 'chain': Cw}
                        if any(v.denominator != 1 or v <= 0 for v in vals.values()): continue
                        if len(set(vals.values())) < 5: continue
                        res.append((Q, a, b, c, ratio, tc, r1, tb, r2, d, M, T, {k: int(v) for k, v in vals.items()}))
print(len(res))
for r in res[:60]:
    Q, a, b, c, ratio, tc, r1, tb, r2, d, M, T, v = r
    print(f"Q={Q} rates={a},{b},{c} {ratio} tc={tc}h r1={r1} tb={tb}h r2={r2} d={d} M={M} T={T}", v)
