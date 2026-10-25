# D04-math-h-v14：共享会议室三种月度计费方案，求“选乙方案比另外两种都省钱”的月使用时长范围。
# 独立求解：把三种方案的月费用写成分段线性函数，收集所有分段点和两两相等的点，
# 在相邻关键点之间取中点检验“乙严格最便宜”，再检验关键点本身，拼出精确的解集，与四个选项逐一比对。
from fractions import Fraction as Fr
import re

# 题面数据
A_RATE = 80                              # 甲：不收月费，每小时 80 元
B_FEE, B_INC, B_OVER = 1200, 20, 60      # 乙：月费 1200 元含 20 小时，超出每小时 60 元
C_FEE, C_INC, C_OVER = 2400, 50, 40      # 丙：月费 2400 元含 50 小时，超出每小时 40 元

OPTIONS = {'A': '大于15且小于40', 'B': '大于15且小于50', 'C': '大于20且小于40', 'D': '大于20且小于50'}


def cost_a(t):
    return A_RATE * t


def cost_b(t):
    return B_FEE + B_OVER * max(Fr(0), t - B_INC)


def cost_c(t):
    return C_FEE + C_OVER * max(Fr(0), t - C_INC)


def b_cheapest(t):
    return cost_b(t) < cost_a(t) and cost_b(t) < cost_c(t)


T_MAX = Fr(200)
# 关键点：0、两个含时长、上限，以及每段内两两费用相等的点（在细网格上找变号，再用线性插值求精确交点）
keys = {Fr(0), Fr(B_INC), Fr(C_INC), T_MAX}
grid = sorted(keys)
funcs = [cost_a, cost_b, cost_c]
for i in range(len(grid) - 1):
    lo, hi = grid[i], grid[i + 1]
    for f in range(3):
        for g in range(f + 1, 3):
            # 在 [lo, hi] 内两个函数都是一次函数，差值也是一次函数
            d_lo = funcs[f](lo) - funcs[g](lo)
            d_hi = funcs[f](hi) - funcs[g](hi)
            if d_lo == d_hi:
                continue
            root = lo + (hi - lo) * d_lo / (d_lo - d_hi)
            if lo <= root <= hi:
                keys.add(root)
pts = sorted(keys)

# 逐段判断（开区间取中点，关键点单独判断），得到解集的各个开/闭片段
pieces = []
for i in range(len(pts) - 1):
    mid = (pts[i] + pts[i + 1]) / 2
    pieces.append(('open', pts[i], pts[i + 1], b_cheapest(mid)))
point_ok = {p: b_cheapest(p) for p in pts}

# 合并：解集应是一个开区间 (L, R)
good = [(a, b) for kind, a, b, ok in pieces if ok]
assert good, 'no t makes plan B cheapest'
L, R = good[0][0], good[-1][1]
for (a1, b1), (a2, b2) in zip(good, good[1:]):
    assert b1 == a2 and point_ok[b1], 'solution set is not one interval'
assert not point_ok[L] and not point_ok[R], 'endpoints should be excluded'
print('选乙最省的月使用时长：大于', L, '且小于', R)
print('端点处费用：t=%s 时 甲=%s 乙=%s；t=%s 时 乙=%s 丙=%s' % (L, cost_a(L), cost_b(L), R, cost_b(R), cost_c(R)))

hits = []
for k, txt in OPTIONS.items():
    lo, hi = map(Fr, re.findall(r'\d+', txt))
    if (lo, hi) == (L, R):
        hits.append(k)
assert len(hits) == 1, hits
print(hits[0])
