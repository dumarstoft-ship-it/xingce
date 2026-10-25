# T249x2（2024副省）AB 南北 100，BC 东西，AC=200，BCD 正三角形（D 在 BC 南侧），求 AD
import math
B = (0.0, 0.0); A = (0.0, 100.0)
BC = math.sqrt(200**2 - 100**2)
C = (BC, 0.0)
D = (BC / 2, -BC * math.sqrt(3) / 2)
AD = math.hypot(A[0]-D[0], A[1]-D[1])
s3, s7 = math.sqrt(3), math.sqrt(7)
options = {"A": 150*s3, "B": 50*(s3+1), "C": 100*s7, "D": 200*math.sqrt(2)}
hits = [k for k, v in options.items() if abs(v - AD) < 1e-6]
assert len(hits) == 1, (AD, hits)
print(hits[0])
