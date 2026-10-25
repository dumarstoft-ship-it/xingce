# T266 9:30–10:00 两人随机到达，先到者等 10 分钟，成功概率（精确几何概型 + 网格校验）
from fractions import Fraction as F
T, w = 30, 10
p = 1 - F(T - w, T) ** 2                 # 1 - 两个角上三角形面积
N = 600
cnt = sum(1 for i in range(N) for j in range(N) if abs((i + .5) - (j + .5)) * T / N <= w)
assert abs(cnt / N**2 - float(p)) < 0.01
options = {"A": F(1, 3), "B": F(2, 3), "C": F(5, 9), "D": F(7, 9)}
hits = [k for k, v in options.items() if v == p]
assert len(hits) == 1, (p, hits)
print(hits[0])
