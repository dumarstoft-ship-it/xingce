from fractions import Fraction as F
from math import ceil, sqrt
# D04-v08: options 400/500/300/375
f = lambda n, hold: 160 * n + hold * F(3000, n)        # hold = per-batch-size coefficient
print('v08 theoretical (half stock):', sqrt(160 * 3000 * 2 / 6))
print('v08 one-side rounding 6 batches ->', 3000 // 6)
print('v08 forgot half: continuous', sqrt(160 * 3000 / 6), 'integer-n best (n|3000):',
      min((f(n, 6), 3000 // n) for n in range(1, 3001) if 3000 % n == 0))
# D04-v09: options 6/7/8/5
print('v09 all at 3 yuan:', F(24, 3), '| all at 5 yuan rounded up:', ceil(F(24, 5)), '| billed 6h misread as up to 7h: 7')
# D04-v12: options 9000/10000/12000/18000
first = next(q for q in range(1, 10**6) if 60 * q >= F(6, 5) * (120000 + 40 * q))
rev = next(q for q in range(6001, 10**6) if 60 * q - (180000 + 30 * q) >= F(1, 5) * 60 * q)
nosub = next(q for q in range(1, 10**6) if 60 * q >= F(6, 5) * (360000 + 30 * q))
print('v12 all at 40:', first, '| profit/revenue:', rev, '| forgot to subtract 6000:', nosub)
