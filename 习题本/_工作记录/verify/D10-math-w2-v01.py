# D10-math-w2-v01: a cooperative plants crops 甲 / 乙 on at most 60 mu.
#   per mu of 甲: water 300 m^3, labour 10 work-days, profit 2000 yuan
#   per mu of 乙: water 100 m^3, labour 20 work-days, profit 3000 yuan
#   water available <= 15000 m^3, labour available <= 1000 work-days
# Question: the maximum profit (in 10^4 yuan).
# Method: exact vertex enumeration of the feasible polygon (every pair of boundary lines, incl. the axes),
# cross-checked by a brute-force scan of a 0.5-mu grid; then match the options.
from fractions import Fraction as Fr
import itertools

AREA = 60
WATER = (300, 100, 15000)          # a*x + b*y <= r
LABOUR = (10, 20, 1000)
PROFIT = (2000, 3000)

CONS = [(1, 1, AREA), WATER, LABOUR, (-1, 0, 0), (0, -1, 0)]   # last two: x >= 0, y >= 0


def feasible(x, y):
    return all(a * x + b * y <= r for a, b, r in CONS)


def profit(x, y):
    return PROFIT[0] * x + PROFIT[1] * y


def meet(c1, c2):
    (a1, b1, r1), (a2, b2, r2) = c1, c2
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    return Fr(r1 * b2 - r2 * b1, det), Fr(a1 * r2 - a2 * r1, det)


vertices = set()
for c1, c2 in itertools.combinations(CONS, 2):
    p = meet(c1, c2)
    if p is not None and feasible(*p):
        vertices.add(p)
best_pt = max(vertices, key=lambda p: profit(*p))
best = profit(*best_pt)
assert sum(1 for p in vertices if profit(*p) == best) == 1, 'optimum vertex not unique'

# brute-force cross-check on a half-mu grid (any planting plan in 0.5-mu steps)
grid_best = max(profit(Fr(i, 2), Fr(j, 2))
                for i in range(0, 2 * AREA + 1) for j in range(0, 2 * AREA + 1)
                if feasible(Fr(i, 2), Fr(j, 2)))
assert grid_best == best, (grid_best, best)

ans = best / 10000                 # in 10^4 yuan
opts = {'A': Fr(27, 2), 'B': Fr(15), 'C': Fr(16), 'D': Fr(17)}
hit = [k for k, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)

# where the distractors come from (documentation only; the answer above does not use them)
wl = meet(WATER, LABOUR)                                   # "join the two technical constraints"
assert not feasible(*wl) and wl[0] + wl[1] > AREA          # ... violates the area limit
aw = meet((1, 1, AREA), WATER)                             # area & water
only_y = (Fr(0), min(Fr(AREA), Fr(WATER[2], WATER[1]), Fr(LABOUR[2], LABOUR[1])))   # plant only 乙
assert [profit(*wl) / 10000, profit(*aw) / 10000, profit(*only_y) / 10000] == [opts['D'], opts['A'], opts['B']]

print('vertices', sorted((float(x), float(y), float(profit(x, y))) for x, y in vertices))
print('optimum', best_pt, 'profit', best)
print(hit[0])
