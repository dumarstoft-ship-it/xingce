# D07-math-1-v02: 8 条分道、道宽 1.25 米，第 1 道内沿弯道半径 36 米、直道 85 米；
# 各沿本道内沿跑一整圈，第 8 道比第 1 道约多跑多少米（π 取 3.14）
PI = 3.14
LANES, WIDTH, R1, STRAIGHT = 8, 1.25, 36, 85

def lap(k):
    """第 k 道内侧边线一整圈：两条直道 + 两个半圆弯道"""
    r = R1 + (k - 1) * WIDTH
    return 2 * STRAIGHT + 2 * (PI * r)

diff = lap(LANES) - lap(1)
opts = {'A': 27.5, 'B': 47.1, 'C': 55, 'D': 62.8}
best = min(opts, key=lambda k: abs(opts[k] - diff))
assert abs(opts[best] - diff) < 0.5, diff                       # “约”：与计算值相差不到 0.5
assert all(abs(v - diff) > 5 for k, v in opts.items() if k != best)
print('多跑 =', round(diff, 4))
print(best)
