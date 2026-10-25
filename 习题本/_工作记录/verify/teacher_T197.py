# T197（2014河北）177吨货物，大卡车载5吨耗油10升，小卡车载2吨耗油5升，最少耗油多少升。
from fractions import Fraction as F

GOODS, (BIG_CAP, BIG_OIL), (SMALL_CAP, SMALL_OIL) = 177, (5, 10), (2, 5)
OPTS = {'A': F(885, 2), 'B': F(356), 'C': F(355), 'D': F(354)}
best = min(BIG_OIL * b + SMALL_OIL * s
           for b in range(GOODS // BIG_CAP + 2)
           for s in range(GOODS // SMALL_CAP + 2)
           if BIG_CAP * b + SMALL_CAP * s >= GOODS)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min oil =', best, 'theoretical bound =', GOODS * F(BIG_OIL, BIG_CAP))
print(hits[0])
