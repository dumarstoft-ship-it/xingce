# explore numbers for need #15: two-tier variable cost, target profit
from fractions import Fraction as Fr
res = []
for p in range(30, 201, 5):
    for m1 in range(10, 80, 5):          # margin first tier
        v1 = p - m1
        if v1 <= 0: continue
        for dm in range(2, 21, 1):       # cost drop beyond Q1
            v2 = v1 - dm
            m2 = p - v2
            if v2 <= 0: continue
            for Q1 in range(2000, 10001, 1000):
                for F in range(100000, 500001, 10000):
                    node = m1 * Q1 - F
                    if node >= 0: continue          # still losing at tier boundary
                    for T in range(50000, 400001, 10000):
                        need = T - node
                        if need % m2: continue
                        Q = Q1 + need // m2
                        if Q % 500: continue
                        E1 = Fr(F + T, m1)
                        E2 = Fr(F + T, m2)
                        if E1.denominator != 1 or E1 % 100: continue
                        if E2 <= Q1: continue
                        if E2.denominator != 1 or E2 % 100: continue
                        G = Q1 + E2
                        opts = sorted({int(Q), int(E1), int(E2), int(G)})
                        if len(opts) < 4: continue
                        # avoid collisions with other needs' numbers
                        if p == 50 or v1 == 30 or F in (70000, 200000, 90000): continue
                        res.append((p, v1, v2, Q1, F, T, int(Q), int(E1), int(E2), int(G), node))
print(len(res))
import random
random.seed(1)
# prefer "nice" ones: F multiple of 50000, T multiple of 10000, Q multiple of 1000
nice = [r for r in res if r[4] % 50000 == 0 and r[6] % 1000 == 0 and r[0] % 10 == 0 and r[1] % 10 == 0]
print(len(nice))
for r in random.sample(nice, min(60, len(nice))):
    print(r)
