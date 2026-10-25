# D07-math-2-v09: trapezoid ABCD, AD // BC, AD = 16 m, BC = 24 m, height 15 m; diagonals meet at O.
# Find area(AOB). Use exact coordinates for several horizontal offsets of the top base.
from fractions import Fraction as F


def inter(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def tri(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2


AD, BC, h = F(16), F(24), F(15)
vals = set()
for off in (F(0), F(4), F(-3), F(37, 7)):
    A, D = (off, h), (off + AD, h)
    B, C = (F(0), F(0)), (BC, F(0))
    O = inter(A, C, B, D)
    vals.add(tri(A, O, B))
assert len(vals) == 1
s_aob = vals.pop()
opts = {'A': 72, 'B': 90, 'C': 108, 'D': 120}
hit = [k for k, v in opts.items() if v == s_aob]
assert len(hit) == 1, (s_aob, hit)
print('area AOB', s_aob)
print(hit[0])
