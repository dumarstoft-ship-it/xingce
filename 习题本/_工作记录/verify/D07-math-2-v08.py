# D07-math-2-v08: an irregular quadrilateral is cut by its two diagonals into four regions, clockwise
# from the top (as in the figure): jia (top), yi (right), bing (bottom), ding (left).
# Given: yi is 20% smaller than jia; bing is 25 m^2 smaller than ding; yi is 20 m^2 larger than bing.
# Find the total area.
# Geometry: with O the intersection of the diagonals, OA=p, OB=q, OC=r, OD=s and angle t between them,
# region areas are (1/2)sin(t) times p*q, q*r, r*s, s*p (in clockwise order). Solve for these
# unknowns directly (no area-product shortcut), then rebuild a real quadrilateral and check it.
import math
import sympy as sp

q, r, s = sp.symbols('q r s', positive=True)
p, k = sp.Integer(1), sp.Integer(1)      # scale freedom: fix OA = 1 and (1/2)sin(t) = 1
jia, yi, bing, ding = k * p * q, k * q * r, k * r * s, k * s * p
eqs = [sp.Eq(yi, sp.Rational(8, 10) * jia),
       sp.Eq(ding - bing, 25),
       sp.Eq(yi - bing, 20)]
sols = sp.solve(eqs, [q, r, s], dict=True)
sols = [d for d in sols if all(v.is_positive for v in d.values())]
assert len(sols) == 1, sols
d = sols[0]
A = [sp.nsimplify(x.subs(d)) for x in (jia, yi, bing, ding)]
total = sum(A)

# rebuild an actual quadrilateral (angle 75 deg between the diagonals) and check by the shoelace formula
t = math.radians(75)
kk = 1.0                                   # (1/2) sin(t) * (scale)^2 must equal 1 -> choose a length scale
L = math.sqrt(kk / (0.5 * math.sin(t)))
pp, qq, rr, ss = (float(v) * L for v in (p, d[q], d[r], d[s]))
O = (0.0, 0.0)
PA = (pp * math.cos(math.pi - 0.3), pp * math.sin(math.pi - 0.3))
PB = (qq * math.cos(math.pi - 0.3 - t), qq * math.sin(math.pi - 0.3 - t))
PC = (-rr * math.cos(math.pi - 0.3), -rr * math.sin(math.pi - 0.3))
PD = (-ss * math.cos(math.pi - 0.3 - t), -ss * math.sin(math.pi - 0.3 - t))


def tri(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2


geo = [tri(O, PA, PB), tri(O, PB, PC), tri(O, PC, PD), tri(O, PD, PA)]
assert all(abs(g - float(a)) < 1e-6 for g, a in zip(geo, A)), (geo, A)

# reading the figure wrongly (other "opposite" pairings) gives no positive solution
J, Y, B, D = sp.symbols('J Y B D', positive=True)
base = [sp.Eq(Y, sp.Rational(8, 10) * J), sp.Eq(D - B, 25), sp.Eq(Y - B, 20)]
assert sp.solve(base + [sp.Eq(J * Y, B * D)], [J, Y, B, D], dict=True) == []
assert sp.solve(base + [sp.Eq(J * D, Y * B)], [J, Y, B, D], dict=True) == []

opts = {'A': 370, 'B': 410, 'C': 495, 'D': 594}
hit = [kk2 for kk2, v in opts.items() if v == total]
assert len(hit) == 1, (total, hit)
print('jia, yi, bing, ding =', A, 'total', total)
print(hit[0])
