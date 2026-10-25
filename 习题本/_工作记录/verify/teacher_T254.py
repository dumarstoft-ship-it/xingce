# T254 边长 10 正方形，以左下、右上两顶点为圆心作半径 10 的扇形，阴影在对角线两侧的两个角上
# 按图形区域定义做网格数值积分，再与选项比对
import math
a = 10.0
N = 2000
cnt = 0
for i in range(N):
    x = (i + 0.5) * a / N
    for j in range(N):
        y = (j + 0.5) * a / N
        up = y > x and x * x + y * y > a * a                       # 对角线上方、左下圆心扇形外
        down = y < x and (x - a) ** 2 + (y - a) ** 2 > a * a       # 对角线下方、右上圆心扇形外
        if up or down:
            cnt += 1
area = cnt * (a / N) ** 2
options = {"A": 100 - 25*math.pi, "B": 200 - 35*math.pi, "C": 200 - 50*math.pi, "D": 100*math.pi - 100}
best = min(options, key=lambda k: abs(options[k] - area))
assert abs(options[best] - area) < 0.05, (area, options[best])
print(best)
