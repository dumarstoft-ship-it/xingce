# D07-math-h-v01: a 600 m^2 rectangular sheep pen in front of a 50 m old stone wall.
# - the side along the wall uses the wall only (no fence) and may not run past it  -> that side <= 50 m
# - a canal parallel to the wall lies 15 m in front of it; the pen must stay between -> depth <= 15 m
# - fence: the side facing the wall 200 yuan/m (gate included), the two other sides 150 yuan/m each
# Question: the minimum total fence cost.
# Method: scan the depth x over its whole feasible range with exact fractions, then confirm the minimiser
# analytically (end points of the feasible interval + interior stationary points), and match the options.
from fractions import Fraction as Fr
import sympy as sp

AREA, WALL, CANAL = 600, 50, 15
P_FRONT, P_SIDE = 200, 150


def cost(x):                      # x = depth (the two sides perpendicular to the wall)
    y = Fr(AREA) / x              # y = side along the wall = the fenced side facing it
    return P_FRONT * y + 2 * P_SIDE * x


def feasible(x):
    y = Fr(AREA) / x
    return 0 < x <= CANAL and 0 < y <= WALL


grid = [Fr(k, 1000) for k in range(1, CANAL * 1000 + 1)]
cands = [x for x in grid if feasible(x)]
assert cands, 'no feasible pen'
best_x = min(cands, key=cost)
best = cost(best_x)

# analytic cross-check: C(x) = 200*600/x + 300x on the feasible interval [600/50, 15]
x = sp.symbols('x', positive=True)
C = P_FRONT * AREA / x + 2 * P_SIDE * x
lo, hi = sp.Rational(AREA, WALL), sp.Integer(CANAL)
stationary = [s for s in sp.solve(sp.diff(C, x), x) if s.is_positive]
checkpoints = [lo, hi] + [s for s in stationary if lo <= s <= hi]
exact = min(C.subs(x, p) for p in checkpoints)
assert exact == best, (exact, best)

opts = {'A': 10250, 'B': 12000, 'C': 12500, 'D': 13600}
hit = [k for k, v in opts.items() if v == best]
assert len(hit) == 1, (best, hit)

# where the distractors come from (documentation only; the answer above does not use these)
unconstrained = min(C.subs(x, s) for s in stationary)            # take the equality point, ignore limits
full_wall = cost(Fr(AREA, WALL))                                 # "use the whole old wall"
one_side = P_FRONT * Fr(AREA) / best_x + P_SIDE * best_x         # fence only one perpendicular side
assert [unconstrained, full_wall, one_side] == [opts['B'], opts['D'], opts['A']], (unconstrained, full_wall, one_side)
assert stationary == [20] and not feasible(Fr(20))               # the equality point (depth 20) is infeasible

print('best depth', best_x, 'side along wall', Fr(AREA) / best_x, 'min cost', best)
print(hit[0])
