# T253 半径 R 的钢珠放在圆柱孔口，钢珠顶到工件顶端面距离 X，求孔径
import math
X, R = 5.0, 3.0
d_center = X - R                          # 球心到顶端面的距离
half = math.sqrt(R**2 - d_center**2)      # 接触点到孔轴的距离 = 孔半径
diam = 2 * half
options = {"A": 2*math.sqrt(5), "B": math.sqrt(5), "C": math.sqrt(10), "D": 4.0}
hits = [k for k, v in options.items() if abs(v - diam) < 1e-9]
assert len(hits) == 1, (diam, hits)
print(hits[0])
