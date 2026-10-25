# D06-math-2-v03: best-of-three (first to 2 wins, match stops), p = 0.6 per game.
from fractions import Fraction as F
from functools import lru_cache

p = F(6, 10)
NEED = 2

@lru_cache(maxsize=None)
def win(a, b):
    if a == NEED:
        return F(1)
    if b == NEED:
        return F(0)
    return p * win(a + 1, b) + (1 - p) * win(a, b + 1)

P = win(0, 0)
opts = {'A': F(360, 1000), 'B': F(504, 1000), 'C': F(648, 1000), 'D': F(792, 1000)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('P =', float(P))
print(hit[0])
