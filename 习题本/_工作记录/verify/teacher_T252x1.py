# T252x1（2019浙江A）梯形 AD∥BC，BC-AD=16，S△ABC-S△ACD=200，求两底距离 h
from fractions import Fraction as F
diff_base, diff_area = F(16), F(200)
# 两三角形高都是 h：S△ABC - S△ACD = h(BC-AD)/2
h = 2 * diff_area / diff_base
# 用具体坐标复核
AD = F(10); BC = AD + diff_base
C = (F(0), h); B = (BC, h); D = (F(3), F(0)); A = (F(3) + AD, F(0))
tri = lambda p, q, r: abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
assert tri(A, B, C) - tri(A, C, D) == diff_area
options = {"A": F(25, 2), "B": F(37, 2), "C": F(20), "D": F(25)}
hits = [k for k, v in options.items() if v == h]
assert len(hits) == 1, (h, hits)
print(hits[0])
