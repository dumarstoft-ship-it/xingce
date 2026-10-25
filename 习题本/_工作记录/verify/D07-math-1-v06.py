# D07-math-1-v06: 圆锥铅块（底面半径 6、高 8）熔铸成半径 2 的小球，损耗 10%，最多铸几个
import math

CONE_R, CONE_H, BALL_R, LOSS = 6, 8, 2, 0.10

def solid_of_revolution(radius_at, height, n=20000):
    """圆盘法求旋转体体积：radius_at(z) 为高度 z 处截面半径"""
    dz = height / n
    return sum(math.pi * radius_at((i + 0.5) * dz) ** 2 * dz for i in range(n))

v_cone = solid_of_revolution(lambda z: CONE_R * (1 - z / CONE_H), CONE_H)
v_ball = solid_of_revolution(lambda z: math.sqrt(max(BALL_R ** 2 - (z - BALL_R) ** 2, 0.0)), 2 * BALL_R)
usable = v_cone * (1 - LOSS)
n = 0
while (n + 1) * v_ball <= usable:
    n += 1
opts = {'A': 8, 'B': 9, 'C': 24, 'D': 27}
hit = [k for k, v in opts.items() if v == n]
assert len(hit) == 1, (n, hit)
print('可用体积/单球体积 ≈', round(usable / v_ball, 4), '最多', n, '个')
print(hit[0])
