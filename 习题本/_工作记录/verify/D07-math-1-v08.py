# D07-math-1-v08: 半圆形隧道宽 10 米，车须在中线右侧（可贴中线），车厢顶离地 4 米，求车厢最大宽度
# 做法：枚举车宽 w 与车身左侧到中线的距离 x0≥0，凸图形只需检查车厢四个角都在半圆内
R = 10 / 2
H = 4

def fits(x0, w):
    corners = [(x0, 0), (x0 + w, 0), (x0, H), (x0 + w, H)]
    return all(x * x + y * y <= R * R + 1e-12 for x, y in corners)

best = 0.0
for wi in range(1, 1001):                 # 车宽 0.01 ~ 10 米
    w = wi / 100
    if any(fits(xi / 100, w) for xi in range(0, 501)):
        best = max(best, w)
opts = {'A': 3, 'B': 4, 'C': 5, 'D': 6}
hit = [k for k, v in opts.items() if abs(v - best) < 1e-9]
assert len(hit) == 1, (best, hit)
print('最大车宽 =', best)
print(hit[0])
