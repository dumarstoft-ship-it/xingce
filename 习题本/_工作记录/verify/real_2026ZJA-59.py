# real 2026ZJA-59: 操场 = 矩形 ABCD + 以 AD、BC 为直径的两个半圆；两半圆面积和是矩形面积的 π/6 倍，
# 矩形周长 500 米，求外轮廓长度。设直线边 AB=CD=L，半圆直径 AD=BC=W。
from fractions import Fraction as F
import math

sols = []
for W in range(1, 250):                       # 先在整数上穷举，再验证比例关系（π 两边约去）
    L = 250 - W                               # 2(L+W)=500
    semis_over_pi = F(W * W, 4)               # 两个半圆面积和 / π = (W/2)²
    rect_times_1_6 = F(L * W, 6)              # 矩形面积 × (π/6) / π
    if semis_over_pi == rect_times_1_6:
        sols.append((L, W))
assert len(sols) == 1, sols
L, W = sols[0]
assert L > W                                   # 与原图一致：直线边更长
contour = 2 * L + math.pi * W                  # 两条直线边 + 两段半圆弧（合成一个整圆周）
opts = {'A': 200 + 100 * math.pi, 'B': 300 + 100 * math.pi, 'C': 100 + 300 * math.pi, 'D': 200 + 300 * math.pi}
hit = [k for k, v in opts.items() if abs(v - contour) < 1e-9]
assert len(hit) == 1, (contour, hit)
print('L =', L, 'W =', W, '外轮廓 =', contour)
print(hit[0])
