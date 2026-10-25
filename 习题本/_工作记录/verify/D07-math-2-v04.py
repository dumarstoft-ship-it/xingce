# D07-math-2-v04: 60 m of fence, rectangle against a long wall (the wall side needs no fence).
# Maximise the area: brute force over the side perpendicular to the wall (exact rationals).
from fractions import Fraction as F

L = 60
area, x = max((xx * (L - 2 * xx), xx) for xx in (F(k, 100) for k in range(1, 100 * L // 2)))
for k in range(-50, 51):                       # finer local check around the optimum
    y = x + F(k, 10000)
    assert y * (L - 2 * y) <= area
opts = {'A': 225, 'B': 400, 'C': 450, 'D': 900}
hit = [k for k, v in opts.items() if v == area]
assert len(hit) == 1, (area, hit)
print('max area', area, 'perpendicular side', x, 'parallel side', L - 2 * x)
print(hit[0])
