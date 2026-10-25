# real 2026GD-40: rainstorm day prob 30%; congestion 70% on rainstorm days, 20% otherwise.
from fractions import Fraction as F

p_storm = F(30, 100)
P = p_storm * F(70, 100) + (1 - p_storm) * F(20, 100)

opts = {'A': F(25, 100), 'B': F(35, 100), 'C': F(45, 100), 'D': F(55, 100)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('P =', P)
print(hit[0])
