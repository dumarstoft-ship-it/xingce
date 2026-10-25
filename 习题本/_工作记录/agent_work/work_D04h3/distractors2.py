# reproduce every distractor's error path for round-2 v15-v18
from fractions import Fraction as Fr
from math import sqrt
# v15
print('v15 only variable cost:', 30)
print('v15 displaced valued at profit 15:', 30 + Fr(1000 * (60 - 45), 3000))
print('v15 price >= unit cost:', 45)
print('v15 correct:', 30 + Fr(1000 * (60 - 30), 3000))
# v16
c, R, s, P, a = Fr('10.53'), Fr(3, 10), Fr(8, 10), Fr(18), Fr('12.5')
K = c * (1 + R) / (s * P + (1 - s) * a)
print('v16 K', K, 'correct x', 1 - sqrt(K), 'linear x', (1 - K) / 2, 'two-day total', 1 - K)
K2 = c * (1 + R) / (s * P)
print('v16 forgot clearance revenue: K2', K2, 'x', 1 - sqrt(K2))
# v17
b, f1 = 12, 1
print('v17 correct', Fr(1200 * (b + f1), 1000) - b)
print('v17 freight only', Fr(1200 * f1, 1000))
print('v17 forgot normal freight', Fr(1200 * b, 1000) - b)
ship_n, ship_c = Fr(960) * Fr(12, 10), Fr(960) * Fr(104, 100)
print('v17 ship = 960*(1+loss):', ship_n * (b + f1) / ship_c - b)
print('v17 same-batch (old idea) at price 30:', Fr(16, 100) * 30 + 1, ' at cost:', Fr(16, 100) * 12 + 1)
# v18
print('v18 correct (left>=300):', Fr(36000 - 3600, 30))
print('v18 ignore cap (all left returnable): x >=', Fr(36000 - 12 * 1500, 60 - 12 - 30))
print('v18 remaining at correct:', 1500 - 1080)
print('v18 buyout break-even with 300 returned:', Fr(36000 - 3600, 60))
print('v18 ignore returns:', Fr(36000, 30))
