# -*- coding: utf-8 -*-
# M08 自解真题（无官方答案）的独立验算：从题面数据出发求解，最后检查四个选项恰好一个成立。
import math, itertools
from fractions import Fraction as F

def pick(val, opts, tol=1e-9):
    hits = [k for k, v in opts.items() if abs(v - val) <= tol]
    assert len(hits) == 1, (val, opts, hits)
    return hits[0]

res = {}

# ---- 2026ZJA-55：东偏南方向 60 → 左转90° 走 45 到营地正东 → 再走 35，求与营地距离
# 不预设"直角三角形"，用二分法求出发方向（使第二段终点恰在营地正东），再计算。
def walk(theta):                       # theta：东偏南角度（度）
    t = math.radians(theta)
    d1 = (math.cos(t), -math.sin(t))   # 东为 x，北为 y
    d2 = (-d1[1], d1[0])               # 左转 90°（逆时针）
    P = (60*d1[0], 60*d1[1]); Q = (P[0] + 45*d2[0], P[1] + 45*d2[1])
    return P, Q, d2
lo, hi = 1e-6, 90 - 1e-6
for _ in range(200):
    mid = (lo + hi)/2
    _, Q, _ = walk(mid)
    if Q[1] > 0: lo = mid               # 偏南角太小：第二段终点仍在东线以北，需加大偏南角
    else: hi = mid
P, Q, d2 = walk(lo)
assert abs(Q[1]) < 1e-7 and Q[0] > 0
Rpt = (Q[0] + 35*d2[0], Q[1] + 35*d2[1])
res['2026ZJA-55'] = pick(math.hypot(*Rpt), {'A': 80, 'B': 90, 'C': 100, 'D': 120}, 1e-6)

# ---- 2026GK-75：梯形 AB∥CD（AB 上底），对角线 AD、BC 交于 O，OA=0.6·OD；扩成长方形，面积至少增加？
# 用原图像素坐标（A(200,0) C(80,330) D(475,330)，B 按 AB=0.6·CD 定位，与原图吻合），
# 对凸四边形做"最小外接矩形"穷举（旋转卡壳 + 3600 个方向暴力），不预设"矩形一边沿底边"。
A = (200.0, 0.0); C = (80.0, 330.0); D = (475.0, 330.0); B = (A[0] + 0.6*(D[0] - C[0]), 0.0)
O_ratio = None
# 先验证 OA/OD = 0.6 由图形自然成立（AB∥CD 时 OA/OD = AB/CD）
def inter(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))
O = inter(A, D, B, C)
assert abs(math.dist(O, A)/math.dist(O, D) - 0.6) < 1e-9
poly = [A, B, D, C]
def area(p): return abs(sum(p[i][0]*p[(i+1) % 4][1] - p[(i+1) % 4][0]*p[i][1] for i in range(4)))/2
def box(p, t):
    ux, uy = math.cos(t), math.sin(t); vx, vy = -uy, ux
    us = [x*ux + y*uy for x, y in p]; vs = [x*vx + y*vy for x, y in p]
    return (max(us) - min(us))*(max(vs) - min(vs))
cands = [math.atan2(poly[(i+1) % 4][1] - poly[i][1], poly[(i+1) % 4][0] - poly[i][0]) for i in range(4)]
best = min([box(poly, t) for t in cands] + [box(poly, math.pi*k/3600) for k in range(3600)])
res['2026GK-75'] = pick(best/area(poly) - 1, {'A': 0.20, 'B': 0.25, 'C': 0.40, 'D': 0.50}, 1e-6)
# 一般性检查：任意"两腰内倾"的梯形（AB:CD=3:5），最小外接矩形都 = 下底×高 → 增加 25%
for ax in [10, 50, 100, 150]:
    for h in [80, 200, 330]:
        P2 = [(ax, 0.0), (ax + 0.6*395, 0.0), (395.0, h), (0.0, h)]
        if not (0 <= ax and ax + 0.6*395 <= 395): continue
        b2 = min([box(P2, math.pi*k/7200) for k in range(7200)])
        assert abs(b2/area(P2) - 1.25) < 1e-3, (ax, h, b2/area(P2))

# ---- 2026ZJA-59：两个半圆面积和 = π/6 × 矩形面积，矩形周长 500，求外轮廓长
sols = [(L, W) for W in range(1, 250) for L in [250 - W] if F(W*W, 4) == F(L*W, 6)]   # π 两边约去
assert len(sols) == 1
L, W = sols[0]
outer = (2*L, W)                                   # 外轮廓 = 2L + πW，记为 (常数项, π 的系数)
opts = {'A': (200, 100), 'B': (300, 100), 'C': (100, 300), 'D': (200, 300)}
res['2026ZJA-59'] = [k for k, v in opts.items() if v == outer][0]

# ---- 2026GD-41：对角线分成四块；原图中青菜与茄子相对、毛豆与番茄相对
# 枚举毛豆面积 m（0.01 精度），三种"相对"配对都试，只有图中配对给出合法（全正）解
found = {}
for pairing in ['青菜-茄子', '青菜-毛豆', '青菜-番茄']:
    for k in range(1, 500000):
        m = F(k, 100); qc = F(14, 10)*m; fq = qc - 140; qz = fq - 40
        if min(m, qc, fq, qz) <= 0: continue
        prod = {'青菜-茄子': (qc*qz, m*fq), '青菜-毛豆': (qc*m, fq*qz), '青菜-番茄': (qc*fq, m*qz)}[pairing]
        if prod[0] == prod[1]:
            found[pairing] = (m, qz)
assert list(found) == ['青菜-茄子'], found
m, qz = found['青菜-茄子']
res['2026GD-41'] = pick(float(m - qz), {'A': 60, 'B': 70, 'C': 90, 'D': 100})

# ---- 2026GK-72：甲、乙体积比 3:2，各恰有 2 个面是边长 n 的正方形（即 n×n×a 型，a≠n）
# 粘成一个长方体后表面积减少 20%。枚举所有可能的粘接面（两个全等的面才能拼成长方体）。
n = F(1); ratios = set()
for a100 in range(1, 1000):
    a = F(a100, 100); b = a*F(2, 3)
    if a == n or b == n: continue
    dimsA = (n, n, a); dimsB = (n, n, b)
    SA = 2*(n*n + 2*n*a); SB = 2*(n*n + 2*n*b)
    facesA = {tuple(sorted(f)) for f in [(n, n), (n, a)]}; facesB = {tuple(sorted(f)) for f in [(n, n), (n, b)]}
    for f in facesA & facesB:                    # 可以完全贴合的公共面
        loss = 2*f[0]*f[1]
        if loss == F(1, 5)*(SA + SB):
            e = sorted(dimsB); ratios.add(e[0]/e[-1])
assert len(ratios) == 1, ratios
res['2026GK-72'] = [k for k, v in {'A': F(2, 3), 'B': F(3, 4), 'C': F(3, 5), 'D': F(4, 5)}.items() if v in ratios][0]

# ---- 2026ZJA-64：长方体 12 条棱 + 12 条面对角线只出现 3 种长度，最短为 1，求体积
# 设 a≤b≤c，枚举 b²、c² ∈ {k/16}（覆盖 √2、√3 等常见值），统计不同长度个数
vols = set()
for b2 in [F(k, 16) for k in range(16, 16*16 + 1)]:
    for c2 in [F(k, 16) for k in range(16, 16*16 + 1)]:
        if c2 < b2: continue
        L2 = {F(1), b2, c2, 1 + b2, 1 + c2, b2 + c2}
        if len(L2) == 3 and min(L2) == 1:
            vols.add(round(math.sqrt(b2*c2), 12))
assert len(vols) == 1, vols
res['2026ZJA-64'] = pick(vols.pop(), {'A': math.sqrt(2), 'B': 2, 'C': 2*math.sqrt(2), 'D': math.sqrt(6)}, 1e-9)

if __name__ == '__main__':
    for k, v in res.items():
        print(k, v)
