# T249x1（2024地市）∠A=∠C=∠E=90°，∠B=135°，AB=40，CD=50，EA=60，求整圈道路长度范围
import math
s2 = math.sqrt(2)
# 坐标：A(0,0)，AB 向右，AE 向下；BC 方向(1,-1)/√2，CD 方向(-1,-1)/√2（在 C 处右转 90°），DE 水平
AB, CD, EA = 40.0, 50.0, 60.0
# 竖直：BC/√2 + CD/√2 = EA
BC = (EA - CD / s2) * s2
C = (AB + BC / s2, -BC / s2)
D = (C[0] - CD / s2, C[1] - CD / s2)
assert abs(D[1] + EA) < 1e-9
DE = D[0]
# 校验 B、C、E 处的角
def ang(p, q, r):
    v1 = (p[0]-q[0], p[1]-q[1]); v2 = (r[0]-q[0], r[1]-q[1])
    return math.degrees(math.acos((v1[0]*v2[0]+v1[1]*v2[1]) / math.hypot(*v1) / math.hypot(*v2)))
A, B, E = (0.0, 0.0), (AB, 0.0), (0.0, -EA)
assert abs(ang(A, B, C) - 135) < 1e-9 and abs(ang(B, C, D) - 90) < 1e-9 and abs(ang(D, E, A) - 90) < 1e-9
total = AB + BC + CD + DE + EA
ranges = {"A": (200, 210), "B": (210, 220), "C": (0, 200), "D": (220, 1e9)}
hits = [k for k, (lo, hi) in ranges.items() if lo < total < hi]
assert len(hits) == 1, (total, hits)
print(hits[0])
