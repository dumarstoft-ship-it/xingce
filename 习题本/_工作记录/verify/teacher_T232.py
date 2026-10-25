# T232 圆锥(底半径10)竖直钻半径2的孔，剩余体积最少是 V 的多少
# 钻掉体积 = ∫∫_{孔截面} h(x,y) dA，h = H(1 - ρ/R)；对孔中心偏移 d 做数值积分找最大值
import math
R, rr, H = 10.0, 2.0, 1.0
V = math.pi * R**2 * H / 3

def removed(d, n=400):
    # 极坐标在孔截面上积分（孔中心距锥轴 d）
    tot = 0.0
    for i in range(n):
        s = (i + 0.5) / n * rr
        for j in range(n):
            th = (j + 0.5) / n * 2 * math.pi
            x = d + s * math.cos(th)
            y = s * math.sin(th)
            rho = math.hypot(x, y)
            hh = H * (1 - rho / R)
            if hh > 0:
                tot += hh * s * (rr / n) * (2 * math.pi / n)
    return tot

best_d, best = max(((d, removed(d, 200)) for d in [0, 0.5, 1, 2, 4, 6, 8]), key=lambda t: t[1])
assert best_d == 0
# 中心钻孔的精确值：圆柱(高 H(1-r/R)) + 顶部小圆锥(高 H*r/R)
exact_removed = math.pi * rr**2 * H * (1 - rr / R) + math.pi * rr**2 * (H * rr / R) / 3
assert abs(removed(0, 400) - exact_removed) / exact_removed < 1e-3
remain_ratio = (V - exact_removed) / V
options = {"A": 0.868, "B": 0.876, "C": 0.892, "D": 0.896}
hits = [k for k, v in options.items() if abs(v - remain_ratio) < 1e-9]
assert len(hits) == 1, (remain_ratio, hits)
print(hits[0])
