# D06-math-2-v06: each day independently choose metro (0.6) / bus (0.4);
# on time: metro 0.9, bus 0.6; days independent. P(on time both of two days).
from fractions import Fraction as F
from itertools import product

modes = {'metro': (F(6, 10), F(9, 10)), 'bus': (F(4, 10), F(6, 10))}

P = F(0)
for m1, m2 in product(modes, repeat=2):
    pm1, ok1 = modes[m1]
    pm2, ok2 = modes[m2]
    P += pm1 * pm2 * ok1 * ok2

opts = {'A': F(3492, 10000), 'B': F(6084, 10000), 'C': F(6300, 10000), 'D': F(7800, 10000)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('P =', float(P))
print(hit[0])
