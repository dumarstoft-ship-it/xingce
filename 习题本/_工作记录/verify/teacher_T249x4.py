# T249x4（2023副省）AE=EF=FB，AD=DC，O=EC∩FD，人工湖 △EOD，求 S△ABC/S△EOD
from fractions import Fraction as F
def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))
def tri(p, q, r):
    return abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
res = set()
for A, B, C in [((F(3), F(7)), (F(0), F(0)), (F(10), F(0))), ((F(1), F(5)), (F(0), F(0)), (F(9), F(1)))]:
    E = (A[0] + (B[0]-A[0])/3, A[1] + (B[1]-A[1])/3)
    Fp = (A[0] + 2*(B[0]-A[0])/3, A[1] + 2*(B[1]-A[1])/3)
    D = ((A[0]+C[0])/2, (A[1]+C[1])/2)
    O = inter(E, C, Fp, D)
    res.add(tri(A, B, C) / tri(E, O, D))
assert len(res) == 1, res
k = res.pop()
options = {"A": 9, "B": 12, "C": 16, "D": 18}
hits = [key for key, v in options.items() if v == k]
assert len(hits) == 1, (k, hits)
print(hits[0])
