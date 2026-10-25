# D07-math-2-v06: rectangular car park along a straight river; the river side is not fenced.
# Side parallel to the river: 300 yuan/m; the two sides perpendicular to it: 200 yuan/m.
# Budget 24000 yuan. Maximise the area: brute force over the perpendicular side x (exact).
from fractions import Fraction as F

budget, p_par, p_perp = 24000, 300, 200
best = None
k = 0
while True:
    k += 1
    x = F(k, 100)                               # perpendicular side, metres
    y = (budget - 2 * p_perp * x) / p_par       # the rest of the budget buys the parallel side
    if y <= 0:
        break
    a = x * y
    if best is None or a > best[0]:
        best = (a, x, y)
area, x, y = best
opts = {'A': 600, 'B': 1200, 'C': 1800, 'D': 2400}
hit = [kk for kk, v in opts.items() if v == area]
assert len(hit) == 1, (best, hit)
print('max area', area, 'x', x, 'y', y, 'spend', 2 * p_perp * x, p_par * y)
print(hit[0])
