# pumps: (n1,h1),(n2,h2) -> inflow x, stock S. Then N pumps for a h, k removed, b more h -> done. find N.
from fractions import Fraction as F
out = []
for n1 in range(4, 21):
    for h1 in range(3, 25):
        for n2 in range(n1 + 1, 25):
            for h2 in range(2, h1):
                x = F(n1 * h1 - n2 * h2, h1 - h2)
                if x.denominator != 1 or x <= 0: continue
                S = (n1 - x) * h1
                if S <= 0: continue
                x = int(x); S = int(S)
                for a in range(1, 12):
                    for b in range(1, 16):
                        for k in range(1, 8):
                            Nf = F(S + x * (a + b) + k * b, a + b)
                            if Nf.denominator != 1: continue
                            N = int(Nf)
                            if N - k <= x: continue
                            if N in (n1, n2): continue
                            e1 = F(S + k * b, a + b)                 # ignore inflow entirely
                            e2 = F(S + (k + x) * b, a + b)           # inflow only in phase 2
                            e4 = F(S + x * a + k * b, a + b)         # inflow only in phase 1
                            e5 = N - k                               # answer after removal
                            ints = {'N': N}
                            for nm, v in (('e1', e1), ('e2', e2), ('e4', e4), ('e5', F(e5))):
                                if v.denominator == 1 and v > 0: ints[nm] = int(v)
                            if not all(k_ in ints for k_ in ('e1', 'e2')): continue
                            if len(set(ints.values())) < len(ints): continue
                            if any(v in (n1, n2) for v in ints.values()): continue
                            out.append((n1, h1, n2, h2, x, S, N, a, k, b, ints))
print(len(out))
# prefer small numbers, a+b moderate, distinct and not too far apart
out.sort(key=lambda r: (r[5] > 200, r[6], r[7] + r[9]))
for r in out[:120]:
    print(r)
