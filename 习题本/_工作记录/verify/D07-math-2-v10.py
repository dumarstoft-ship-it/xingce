# D07-math-2-v10: a quadrilateral orchard is cut by its two diagonal paths into four regions:
# lychee, longan, wampee, carambola; lychee and wampee are opposite (they meet only at the crossing).
# lychee 16 mu, longan 12 mu, wampee 24 mu; yearly output per mu (10k yuan): 0.8, 0.4, 0.6, 1.0.
# Find the orchard's total yearly output.
# Geometry: cyclic order lychee (AOB), longan (BOC), wampee (COD), carambola (DOA) puts lychee opposite
# wampee. With OA = 1 and (1/2)sin(angle) = 1, each given area fixes the next diagonal segment.
from fractions import Fraction as F
import math

area = {'lychee': F(16), 'longan': F(12), 'wampee': F(24)}
price = {'lychee': F(8, 10), 'longan': F(4, 10), 'wampee': F(6, 10), 'carambola': F(1)}
OA = F(1)
OB = area['lychee'] / OA          # area(AOB) = OA*OB
OC = area['longan'] / OB          # area(BOC) = OB*OC
OD = area['wampee'] / OC          # area(COD) = OC*OD
area['carambola'] = OD * OA       # area(DOA)

# cross-check with a real drawing (angle 70 deg between diagonals), shoelace areas
t = math.radians(70)
L = math.sqrt(1 / (0.5 * math.sin(t)))
a, b, c, d = (float(v) * L for v in (OA, OB, OC, OD))
P = [(a, 0.0), (b * math.cos(t), b * math.sin(t)), (-c, 0.0), (-d * math.cos(t), -d * math.sin(t))]


def tri(p1, p2):
    return abs(p1[0] * p2[1] - p2[0] * p1[1]) / 2


geo = [tri(P[0], P[1]), tri(P[1], P[2]), tri(P[2], P[3]), tri(P[3], P[0])]
names = ['lychee', 'longan', 'wampee', 'carambola']
assert all(abs(g - float(area[n])) < 1e-9 for g, n in zip(geo, names)), geo

total = sum(area[n] * price[n] for n in names)
opts = {'A': F(40), 'B': F(50), 'C': F(588, 10), 'D': F(64)}
hit = [k for k, v in opts.items() if v == total]
assert len(hit) == 1, (total, hit)
print('carambola area', area['carambola'], 'total output', total)
print(hit[0])
