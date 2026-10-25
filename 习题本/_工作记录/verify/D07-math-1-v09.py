# D07-math-1-v09: 边长 13 的正方形 ABCD 内一点 E，AE=5、BE=12，求三角形 BCE 的面积
import math

S, AE, BE = 13, 5, 12
A, B, C, D = (0, 0), (S, 0), (S, S), (0, S)
# 两圆交点：|EA|=5、|EB|=12
x = (AE ** 2 - BE ** 2 + S ** 2) / (2 * S)
cands = [(x, y) for y in (math.sqrt(AE ** 2 - x ** 2), -math.sqrt(AE ** 2 - x ** 2))]
inside = [p for p in cands if 0 < p[0] < S and 0 < p[1] < S]
assert len(inside) == 1, cands
E = inside[0]

def area(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) / 2

s_bce = area(B, C, E)
opts = {'A': 12.5, 'B': 30, 'C': 54.5, 'D': 72}
hit = [k for k, v in opts.items() if abs(v - s_bce) < 1e-9]
assert len(hit) == 1, (s_bce, hit)
print('E =', E, 'S_BCE =', s_bce)
print(hit[0])
