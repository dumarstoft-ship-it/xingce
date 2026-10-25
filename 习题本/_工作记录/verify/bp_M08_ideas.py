# -*- coding: utf-8 -*-
# M08 考法地图：104 条改编 idea + 备用 idea 的数据与预期答案核对（每条独立从题面数据求解，并断言：
#   ① 预期答案在四个选项中恰好出现一次；② idea 里写明来源的干扰项确实由对应错误路径算出）。
# 出题时如改动数字，请仿照对应函数重算。运行：python3 -I bp_M08_ideas.py
import math, itertools, random
from fractions import Fraction as F
from itertools import combinations, permutations

pi, sqrt = math.pi, math.sqrt
CHECKS = {}

def check(cid):
    def deco(fn):
        CHECKS[cid] = fn
        return fn
    return deco

def one(ans, opts, tol=1e-6):
    """ans 在 opts 中恰好出现一次；返回其下标"""
    hits = [i for i, o in enumerate(opts) if abs(float(o) - float(ans)) <= tol]
    assert len(hits) == 1, (ans, opts, hits)
    return hits[0]

def near(a, b, tol=1e-6):
    assert abs(float(a) - float(b)) <= tol, (a, b)

# =========================== 第 7 天 ===========================
@check('7-1-1')
def _():
    s = (44 - 2*2)/2                       # 2(L+W)+2·2 = 44
    ans = 2*s
    one(ans, [36, 40, 44, 48])
    near(2*(44/2), 44)                     # 漏角块：2(L+W)=44
    near(2*(s + 4), 48)                    # 扩建后的周长
    near(2*((44 - 8)/2), 36)               # 角块按 8 算
    return ans

@check('7-1-2')
def _():
    dr = 7*1.25
    ans = 2*3.14*dr                        # 两个弯道合成一个整圆
    one(round(ans), [27.5, 55, 62.8, 110], 0.5)
    near(3.14*dr, 27.475, 1e-9)            # 只算一个弯道
    near(2*3.14*8*1.25, 62.8, 1e-9)        # 半径差误用 8 道
    near(2*3.14*17.5, 109.9, 1e-9)         # 把 17.5 当半径差
    return ans

@check('7-1-3')
def _():
    L, W, r = 8, 5, 0.3
    ans = 2*(L + W) + 2*pi*r               # 直线段 + 四个四分之一圆弧
    opts = [26, 26 + 0.6*pi, 2*(L + 2*r + W + 2*r), 26 + 1.2*pi]
    one(ans, opts)
    near(opts[2], 28.4)                    # 角上按直角拐弯
    return ans

@check('7-2-1')
def _():
    water = pi*6**2*9
    h = water/(pi*9**2/3)
    one(h, [3, 4, 12, 27])
    near(water/(pi*81), 4)                 # 忘了 1/3
    near(9*3, 27)                          # 只乘 3 没换底面积
    near(water/(pi*18**2/3), 3)            # 直径当半径
    return h

@check('7-2-2')
def _():
    R = 56
    xs = [x for x in range(3, 100) if 6*x*x - (2*x*x + 4*x*(x - 2)) == R]
    assert xs == [7]
    one(7, [5.6, 7, 14, 28])
    near(R/4, 14); near(R/10, 5.6)          # 漏乘厚度；误按五条带
    assert 7*7 != R                         # "只少了一个面"的错误想法不会碰巧得到答案
    return 7

@check('7-2-3')
def _():
    cone = pi*6**2*8/3; ball = 4/3*pi*2**3
    n = math.floor(cone*0.9/ball + 1e-9)
    one(n, [8, 9, 24, 27])
    assert math.floor(cone/ball + 1e-9) == 9
    assert math.floor(3*cone*0.9/ball + 1e-9) == 24 and round(3*cone/ball) == 27
    return n

@check('7-2-4')
def _():
    base, depth, a = 40*30, 10, 20
    water = base*depth
    h_full = (water + a**3)/base           # 假设完全浸没
    assert h_full < a                      # 假设不成立
    h = water/(base - a*a)
    assert h <= a
    rise = h - depth
    one(rise, [10/3, 5, 20/3, 15])
    near(h_full - depth, 20/3)             # 按完全浸没算
    near(a*a*depth/base, 10/3)             # 只按原水深算浸入
    near(h, 15)                            # 答成水深
    return rise

@check('7-3-1')
def _():
    R, H = 5, 4
    w = sqrt(R*R - H*H)                    # 靠右行驶：车身外侧角离中线 w
    one(w, [3, 4, 5, 6])
    near(2*w, 6)                           # 居中通行
    return w

@check('7-3-2')
def _():
    a = 13; AE, BE = 5, 12
    assert AE**2 + BE**2 == a*a
    ex = AE**2/a; ey = AE*BE/a             # A(0,0) B(13,0) C(13,13) D(0,13)
    sBCE = 0.5*a*(a - ex)
    one(sBCE, [30, 54.5, 60, 72])
    near(0.5*AE*BE, 30)                    # △ABE
    near(0.5*a*(a - ey), 54.5)             # △CDE
    near(sBCE, BE**2/2)
    return sBCE

@check('7-3-3')
def _():
    xs = [F(k, 100) for k in range(1, 1000) if F(k, 100)**2 + F(3, 2)**2 == (F(k, 100) + F(1, 2))**2]
    assert xs == [2]
    one(2, [1.5, 2, 2.25, 2.5])
    wrong = [F(k, 100) for k in range(1, 1000) if F(k, 100)**2 + F(9, 4) == F(k, 100)**2 + F(k, 100)]   # 漏 0.5²
    assert wrong == [F(9, 4)]
    return 2

@check('7-3-4')
def _():
    sols = {(b, c) for b in range(1, 200) for c in range(b + 1, 300) if 12*12 + b*b == c*c}
    sols |= {(b, c) for b in range(1, 12) for c in range(13, 300) if b*b + 144 == c*c}
    n = len(sols)
    one(n, [3, 4, 5, 7])
    pairs = [(d, 144//d) for d in range(1, 13) if 144 % d == 0 and d < 144//d]
    assert len(pairs) == 7                 # 不排除奇偶时的因数对数
    return n

@check('7-4-1')
def _():
    A = (0, 0)
    B = (8*math.sin(math.radians(20)), 8*math.cos(math.radians(20)))
    C = (8*math.sin(math.radians(40)), -8*math.cos(math.radians(40)))
    d = math.dist(B, C)
    one(d, [8, 8*sqrt(2), 8*sqrt(3), 16])
    return d

@check('7-4-2')
def _():
    assert 36**2 + 27**2 == 45**2
    s = sqrt(60**2 - 36**2) - 27
    one(s, [15, 21, 33, 48])
    near(sqrt(60**2 - 36**2), 48)          # 忘了减已走的 27
    return s

@check('7-4-3')
def _():
    yi = (0, 0)
    jia = (6*math.sin(math.radians(30)), 6*math.cos(math.radians(30)))
    bing = (8*math.sin(math.radians(60)), -8*math.cos(math.radians(60)))
    # 到三点等距的点：外心（解方程组）
    (x1, y1), (x2, y2), (x3, y3) = yi, jia, bing
    D = 2*(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    ux = ((x1*x1 + y1*y1)*(y2 - y3) + (x2*x2 + y2*y2)*(y3 - y1) + (x3*x3 + y3*y3)*(y1 - y2))/D
    uy = ((x1*x1 + y1*y1)*(x3 - x2) + (x2*x2 + y2*y2)*(x1 - x3) + (x3*x3 + y3*y3)*(x2 - x1))/D
    r = math.dist((ux, uy), yi)
    one(r, [4.8, 5, 6, 7])
    near(6*8/10, 4.8)                      # 斜边上的高
    return r

@check('7-4-4')
def _():
    v1 = (18*math.sin(math.radians(35)), 18*math.cos(math.radians(35)))
    v2 = (24*math.sin(math.radians(55)), -24*math.cos(math.radians(55)))
    rel = math.dist(v1, v2)
    t = 75/rel
    one(t, [1.8, 2.5, 3.1, 4.2])
    near(75/42, 1.8, 0.02); near(75/24, 3.1, 0.03); near(75/18, 4.2, 0.04)
    return t

@check('7-5-1')
def _():
    H, h = 4.8, 1.6
    shadow = lambda d: h*d/(H - h)
    ans = shadow(9) - shadow(3)
    one(ans, [2, 3, 4.5, 6])
    near(6*h/H, 2); near(shadow(9), 4.5)
    return ans

@check('7-5-2')
def _():
    n = round(2/0.25)
    up = sum(range(1, n + 1)); down = sum(range(1, n))
    assert up + down == n*n == 64
    one(up, [28, 32, 36, 64])
    return up

@check('7-5-3')
def _():
    k = (1500/300)**2
    ans = k*(1/5)
    one(ans, [1, 5, 25, 125])
    near((1500/300)*(1/5), 1); near((1500/300)**3*(1/5), 25)
    return ans

@check('7-6-1')
def _():
    best = max(x*(60 - 2*x) for x in [i/100 for i in range(1, 3000)])
    one(best, [225, 400, 450, 900], 1e-6)
    return best

@check('7-6-2')
def _():
    best = 0
    for p in range(4, 26):
        if p % 2: continue                  # 整米边长 ⇒ 周长为偶数
        if 2*p > 50: continue
        a = max(w*(p//2 - w) for w in range(1, p//2))
        best = max(best, 2*a)
    one(best, [70, 72, 78, 156])
    near(2*5*7, 70); near(2*6*6.5, 78); near(12*13, 156)
    return best

@check('7-6-3')
def _():
    def best(cx, cy):                       # cx·x + cy·y = 24000，xy 最大
        return max(x*(24000 - cx*x)/cy for x in [i/10 for i in range(1, int(24000/cx*10))])
    ans = best(400, 300)
    one(ans, [600, 1200, 1800, 2400], 1e-3)
    near(best(400, 600), 600, 1e-3)         # 靠河一边也装了围栏
    near(best(400, 200), 1800, 1e-3)        # 平行边误按 200 元
    near(best(200, 300), 2400, 1e-3)        # 只算了一条垂直边
    return ans

@check('7-7-1')
def _():
    a, c = 9, 16
    side = sqrt(a*c)
    ans = a + c + 2*side
    one(ans, [25, 37, 49, 50])
    near(a + c + side, 37); near(a + c + (a + c), 50)
    return ans

@check('7-7-2')
def _():
    sol = []
    for k in range(1, 100000):
        bing = F(k, 100); ding = bing + 20; yi = bing + 40; jia = F(5, 4)*yi
        if jia*bing == yi*ding: sol.append((jia, yi, bing, ding))
    assert len(sol) == 1
    jia, yi, bing, ding = sol[0]
    tot = jia + yi + bing + ding
    one(tot, [280, 350, 450, 495])
    # 干扰：误用"对角两块面积之和相等"
    w = [F(k, 100) for k in range(1, 100000) if F(5, 4)*(F(k, 100) + 40) + F(k, 100) == (F(k, 100) + 40) + F(k, 100) + 20]
    b2 = w[0]; near(F(5, 4)*(b2 + 40) + (b2 + 40) + b2 + b2 + 20, 280)
    near(jia + yi + bing, 350)              # 漏算丁
    # 干扰：把"乙比丙多 40"看成"乙比丁多 40"
    for k in range(1, 100000):
        bing2 = F(k, 100); ding2 = bing2 + 20; yi2 = ding2 + 40; jia2 = F(5, 4)*yi2
        if jia2*bing2 == yi2*ding2: near(jia2 + yi2 + bing2 + ding2, 495); break
    # 其他两种"相对"配对都无正解
    for k in range(1, 100000):
        bing3 = F(k, 100); ding3 = bing3 + 20; yi3 = bing3 + 40; jia3 = F(5, 4)*yi3
        assert jia3*yi3 != bing3*ding3 and jia3*ding3 != yi3*bing3
    return tot

@check('7-7-3')
def _():
    a, b = 2, 3; S = 100
    parts = {'上': a*a, '左': a*b, '下': b*b, '右': a*b}
    ans = S*parts['左']/sum(parts.values())
    one(ans, [16, 20, 24, 36])
    near(S*parts['上']/25, 16); near(S*parts['下']/25, 36); near(S*2/5/2, 20)
    return ans

@check('7-7-4')
def _():
    li, ly, hp = 12, 18, 24                 # 荔枝与黄皮相对 → 龙眼与杨桃相对
    yt = li*hp/ly
    val = lambda y: li*0.8 + ly*0.6 + hp*0.5 + y*0.9
    ans = val(yt)
    one(ans, [40.5, 46.8, 49, 64.8])
    near(val(li*ly/hp), 40.5)               # 误把相邻两块配对
    near(val(ly*hp/li), 64.8)               # 另一种误配
    near((li + ly + hp + yt)*(0.8 + 0.6 + 0.5 + 0.9)/4, 49)   # 产值简单平均
    return ans

# =========================== 第 21 天 ===========================
@check('21-1-1')
def _():
    theta = 200*pi/600
    ans = 180 - math.degrees(theta)
    one(ans, [60, 90, 120, 150])
    return ans

@check('21-1-2')
def _():
    R = 2; tri = 2*sqrt(3); r = tri*sqrt(3)/6
    ans = (R/r)**2
    one(ans, [16/9, 2, 3, 4])
    near((sqrt(3)/r)**2, 3)                 # 误用正六边形内切圆
    near((R/(3/2))**2, 16/9)                # 内切圆半径误取高的一半
    return ans

@check('21-1-3')
def _():
    ans = None
    for n in range(3, 40):
        miss = (n - 2)*180 - 2570
        if 0 < miss < 180: assert ans is None; ans = miss
    one(ans, [110, 120, 130, 140])
    return ans

@check('21-1-4')
def _():
    n = sum(1 for a, b, c in combinations(range(2, 8), 3) if a + b > c)
    one(n, [10, 12, 13, 20])
    assert len(list(combinations(range(2, 8), 3))) == 20
    return n

@check('21-2-1')
def _():
    AC, BC = 9, 12; AB = math.hypot(AC, BC)
    cd = [x/1000 for x in range(1, 12000) if abs((x/1000)**2 + (AB - AC)**2 - (BC - x/1000)**2) < 1e-9]
    assert len(cd) == 1
    ans = cd[0]
    one(ans, [3.6, 4.5, 6, 7.5])
    near(BC*AB/(AB + AC), 7.5)              # 比例写反
    near(AC*BC/AB/2, 3.6)
    return ans

@check('21-2-2')
def _():
    R = 40
    r = [x/100 for x in range(1, 4000) if abs((R + x/100)**2 - (R**2 + (R - x/100)**2)) < 1e-6]
    assert r == [10.0]
    one(10, [8, 10, 16.6, 20])
    near(R*sqrt(2) - R, 16.57, 0.01)        # 竖直边漏减 r
    return 10

@check('21-2-3')
def _():
    # S1+S2=1, S2+S3=2, S3+S4=3（斜放正方形面积=两侧正放面积之和）；S2 可在 (0,1) 内任取
    vals = set()
    for t in [0.1, 0.3, 0.5, 0.9]:
        S = [1 - t, t, 2 - t, 1 + t]
        assert min(S) > 0
        vals.add(round(sum(S), 12))
    assert vals == {4.0}
    one(4, [3, 4, 5, 6])
    return 4

@check('21-2-4')
def _():
    a = 6; leg = 2*(a*a/4)/a               # 三角形面积 = 正方形 1/4
    hyp = math.hypot(a, leg)
    tri = a + leg + hyp; trap = a + a + (a - leg) + hyp
    ans = trap - tri
    one(ans, [3, 6, 3*sqrt(5), 6 + 3*sqrt(5)])
    return ans

@check('21-3-1')
def _():
    L, W, road, slant = 60, 40, 2, 1.5
    ans = (L - slant)*(W - road)
    one(ans, [2220, 2223, 2280, 2340])
    near(L*W - L*road - slant*W, 2220)      # 重叠处扣两次
    near(L*W - L*road, 2280); near(L*W - slant*W, 2340)
    return ans

@check('21-3-2')
def _():
    a, b = 6, 8; c = math.hypot(a, b)
    semi = lambda d: pi*(d/2)**2/2
    lunes = semi(a) + semi(b) - (semi(c) - a*b/2)
    one(lunes, [24, 48, 12.5*pi, 12.5*pi - 24])
    near(semi(c) - a*b/2, 12.5*pi - 24)     # 求成两个弓形
    return lunes

@check('21-3-3')
def _():
    s = 4; r = s/2
    random.seed(7); N = 400000; cnt2 = 0; cnt_cov = 0
    cs = [(s/2, 0), (s/2, s), (0, s/2), (s, s/2)]
    for _ in range(N):
        x, y = random.random()*s, random.random()*s
        k = sum(1 for cx, cy in cs if (x - cx)**2 + (y - cy)**2 <= r*r)
        cnt2 += (k >= 2); cnt_cov += (k >= 1)
    assert cnt_cov == N                     # 四个半圆盖满正方形
    mc = cnt2/N*s*s
    ans = 4*(pi*r*r/2) - s*s
    near(mc, ans, 0.05)
    one(ans, [2*pi, 4*pi - 8, 8*pi - 16, 16 - 4*pi])
    return ans

@check('21-3-4')
def _():
    vals = set()
    for b in [5, 12, 20, 29]:               # 小正方形边长任取
        B, C, D = (0, 0), (30, 0), (30, 30)
        Fq = (30 + b, b)                    # CEFG：E(30+b,0) F(30+b,b) G(30,b)
        area = abs((C[0]-B[0])*0 + (D[0]-B[0])*(Fq[1]-B[1]) - (Fq[0]-B[0])*(D[1]-B[1]))/2
        vals.add(area)
    assert vals == {450.0}
    one(450, [450, 600, 900, 0])
    return 450

@check('21-4-1')
def _():
    def shaded(AF, BE=60):
        A, B, D = (0, 100), (0, 0), (240, 100)
        E = (-BE, 0); Fh = 100 + math.sqrt(AF**2 - BE**2)
        Fp = (-BE, Fh)
        den = (E[0]-D[0])*(A[1]-B[1]) - (E[1]-D[1])*(A[0]-B[0])
        t = ((E[0]-A[0])*(A[1]-B[1]) - (E[1]-A[1])*(A[0]-B[0]))/den
        G = (E[0] + t*(D[0]-E[0]), E[1] + t*(D[1]-E[1]))
        P = [A, D, G, Fp]
        return abs(sum(P[i][0]*P[(i+1) % 4][1] - P[(i+1) % 4][0]*P[i][1] for i in range(4)))/2
    d = shaded(200) - shaded(150)
    near(shaded(150), 12000, 1e-6)
    one(d/1e4, [0, 0.25, 0.5, 0.75])
    return d

@check('21-4-2')
def _():
    A, B, C = (0.2, 1.3), (0.0, 0.0), (1.0, 0.0)
    D = ((A[0]+B[0])/2, (A[1]+B[1])/2); E = ((A[0]+C[0])/2, (A[1]+C[1])/2)
    def inter(p1, p2, p3, p4):
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
        den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/den
        return (x1 + t*(x2-x1), y1 + t*(y2-y1))
    O = inter(B, E, C, D)
    area = lambda P: abs(sum(P[i][0]*P[(i+1) % len(P)][1] - P[(i+1) % len(P)][0]*P[i][1] for i in range(len(P))))/2
    ans = 36*area([D, O, E])/area([A, B, C])
    one(ans, [2.25, 3, 4.5, 6])
    near(36*area([B, O, D])/area([A, B, C]), 6)   # 误当成重心六块之一 △BOD
    return ans

@check('21-4-3')
def _():
    S, a, b = 420, 60, 84
    vals = set()
    for W in [12, 14, 20, 28, 35]:
        H = S/W; p = 2*a/H; q = 2*b/W
        assert 0 < p < W and 0 < q < H
        vals.add(round((W - p)*(H - q)/2, 9))
    assert len(vals) == 1
    ans = vals.pop()
    one(ans, [84, 90, 96, 186])
    near(S - a - b - ans, 186)
    return ans

@check('21-4-4')
def _():
    sol = []
    for D in range(1, 500):
        C = D + 30; A = D + 60
        if A % 2: continue
        B = A//2
        if A*D == B*C: sol.append((A, B, C, D))
    assert len(sol) == 1
    A, B, C, D = sol[0]; tot = A + B + C + D
    assert math.isqrt(tot)**2 == tot        # 正方形边长 15（条件相容）
    x = (A + B)/math.isqrt(tot); y = (A + C)/math.isqrt(tot)
    near(x*y, A)
    one(tot, [200, 210, 225, 240])
    return tot

@check('21-4-5')
def _():
    ans = 30*F(2, 3)*2
    one(ans, [20, 30, 40, 60])
    near(30*F(2, 3), 20)                    # 漏了 AE=2AC
    return ans

@check('21-5-1')
def _():
    A, B, C = 20, 26, 30
    whole = B + C
    one(whole, [36, 56, 66, 76])
    near(whole - A, 36); near(A + B + C, 76)
    return whole

@check('21-5-2')
def _():
    k = sqrt(F(4, 9))                       # AB:CD
    inc = (1 - (k + 1)/2)/((k + 1)/2)
    one(inc, [0.2, 0.25, 0.385, 0.5], 1e-3)
    near((9 - 6.5)/6.5, 0.385, 1e-3)        # 把 4:9 直接当底边比
    return inc

@check('21-5-3')
def _():
    best = max(r*(40 - 2*r)/2 for r in [i/100 for i in range(1, 2000)])
    one(best, [100, 127, 200, 400], 1e-6)
    near(40**2/(4*pi), 127, 0.5)            # 误围成整圆
    return best

@check('21-5-4')
def _():
    R = 10
    best = max(2*x*sqrt(R*R - x*x) for x in [i/1000 for i in range(1, 10000)])
    one(best, [50, 80, 100, 200], 1e-3)
    s2 = [s*s for s in [k/1000 for k in range(1, 20000)] if abs((s/2)**2 + s*s - R*R) < 1e-2]
    near(s2[0], 80, 0.1)                    # 误以为正方形最大
    return best

@check('21-6-1')
def _():
    ans = math.hypot(6, 3 + 5)
    one(ans, [2*sqrt(10), 8, 10, 14])
    near(math.hypot(6, 5 - 3), 2*sqrt(10))  # 没作对称
    return ans

@check('21-6-2')
def _():
    ans = math.hypot(12, 2 + 4 + 3) + 1 + 2
    one(ans, [15, 18, 20, 21])
    near(ans - 3, 15)                       # 忘加桥长
    return ans

@check('21-6-3')
def _():
    r, d = 30, 60
    tan = sqrt(d*d - r*r); ang = math.acos(r/d)
    arc = r*(pi - 2*ang)
    ans = 2*tan + arc
    one(ans, [60*sqrt(3) + 10*pi, 60*sqrt(3) + 20*pi, 120 + 10*pi, 60 + 30*pi])
    # 暴力：A(-60,0)→圆上点 T1（线段不进入圆内 ⇔ A·T1 ≥ r²）→沿上半圆弧→T2→B(60,0)，枚举 T1、T2 取最短
    A, B = (-d, 0.0), (d, 0.0)
    best = 1e9
    for i in range(0, 1801):
        t1 = pi*i/1800
        T1 = (r*math.cos(t1), r*math.sin(t1))
        if A[0]*T1[0] + A[1]*T1[1] < r*r - 1e-9: continue
        for j in range(0, i + 1):
            t2 = pi*j/1800
            T2 = (r*math.cos(t2), r*math.sin(t2))
            if B[0]*T2[0] + B[1]*T2[1] < r*r - 1e-9: continue
            best = min(best, math.dist(A, T1) + r*(t1 - t2) + math.dist(T2, B))
    near(best, ans, 0.05)
    return ans

@check('21-6-4')
def _():
    OP = 10
    P1 = (OP*math.cos(math.radians(-30)), OP*math.sin(math.radians(-30)))   # 两边夹角 30°，P 在角平分线上时对称点夹角 60°
    P2 = (OP*math.cos(math.radians(30)), OP*math.sin(math.radians(30)))
    ans = math.dist(P1, P2)
    # P 不在平分线上时结果相同（∠P1OP2 = 2×30°）
    for phi in [5, 12, 20, 27]:
        Q1 = (OP*math.cos(math.radians(-phi)), OP*math.sin(math.radians(-phi)))
        Q2 = (OP*math.cos(math.radians(60 - phi)), OP*math.sin(math.radians(60 - phi)))
        near(math.dist(Q1, Q2), ans)
    one(ans, [5, 10, 10*sqrt(2), 10*sqrt(3)])
    return ans

# =========================== 第 35 天 ===========================
@check('35-1-1')
def _():
    top, bot, h, L = 4, 10, 3, 200
    slope = (bot - top)/2/h
    new_bot = top + 2*slope*(h + 1)
    ans = ((top + new_bot)/2*(h + 1) - (top + bot)/2*h)*L
    one(ans, [800, 1400, 2200, 6400])
    near(top*1*L, 800)                      # 只加顶上一层
    near(((top + bot)/2*(h + 1) - (top + bot)/2*h)*L, 1400)   # 误以为底宽不变
    near((top + new_bot)/2*(h + 1)*L, 6400) # 求成加高后总土方
    return ans

@check('35-1-2')
def _():
    base = 50*40; water = base*20
    def depth(bx, by, bh):
        h = water/(base - bx*by)
        return h if h <= bh else (water + bx*by*bh)/base
    up = depth(20, 20, 30); flat = depth(20, 30, 20)
    ans = flat - up
    one(ans, [0, 1, 3.6, 6], 0.05)
    near(water/(base - 600) - up, 3.6, 0.05)  # 横放没检验是否没顶
    near((water + 12000)/base - (water + 12000)/base, 0)   # 两种都按完全浸没
    return ans

@check('35-1-3')
def _():
    cyl_h, cone_h, up_depth = 12, 6, 10
    water = up_depth                        # 以 πr² 为单位
    cone_vol = cone_h/3
    ans = cone_h + (water - cone_vol)
    one(ans, [10, 13, 14, 16])
    near(cone_h + (water - cone_h), 10)     # 圆锥当圆柱
    near(cone_h + (water - cone_h/2), 13)   # 圆锥按一半
    near(cone_h + water, 16)                # 圆锥不算容积
    return ans

@check('35-1-4')
def _():
    a = 6; m = a/2
    tet = m**3/6
    ans = a**3 - 8*tet
    one(ans, [144, 180, 198, 211.5])
    near(a**3 - 8*m**3/3, 144); near(a**3 - 4*tet, 198); near(a**3 - tet, 211.5)
    return ans

@check('35-2-1')
def _():
    layers = [5, 4, 3, 2, 1]
    cubes = {(x, y, z) for z, n in enumerate(layers) for x in range(n) for y in range(n)}
    # 居中叠放：按半格偏移，用 2 倍坐标实现
    cubes = set()
    for z, n in enumerate(layers):
        off = (5 - n)                       # 2 倍坐标下的偏移
        for x in range(n):
            for y in range(n):
                cubes.add((2*x + off, 2*y + off, z))
    # 表面积：上下投影 + 侧面周长（暴力：按 2 倍网格做单位面元统计）
    fine = set()
    for (x, y, z) in cubes:
        for dx in (0, 1):
            for dy in (0, 1):
                fine.add((x + dx, y + dy, z))
    area = 0
    for (x, y, z) in fine:
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            if (x + d[0], y + d[1], z + d[2]) not in fine:
                area += 0.25 if d[2] != 0 else 0.5   # 2 倍网格：水平面元 1/4，竖直面元 1/2×1
    one(area, [85, 110, 140, 150])
    near(area - 25, 85); near(25 + 55 + 60, 140); near(50 + 100, 150)
    return area

@check('35-2-2')
def _():
    a, b, c = 4, 3, 2
    one_area = 2*(a*b + b*c + a*c)
    tot = 3*one_area
    res = sorted(tot - 4*f for f in [a*b, a*c, b*c])
    ans = res[0]
    one(ans, [108, 124, 132, 156])
    assert res == [108, 124, 132]
    return ans

@check('35-2-3')
def _():
    L, s = 10, 2; lo = (L - s)//2; hi = lo + s
    solid = set()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                inx = lo <= y < hi and lo <= z < hi
                iny = lo <= x < hi and lo <= z < hi
                inz = lo <= x < hi and lo <= y < hi
                if not (inx or iny or inz): solid.add((x, y, z))
    area = sum(1 for (x, y, z) in solid for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
               if (x + d[0], y + d[1], z + d[2]) not in solid)
    one(area, [576, 768, 792, 816])
    near(600 - 24, 576); near(600 + 3*4*2*8, 792); near(576 + 3*4*2*10, 816)
    return area

@check('35-2-4')
def _():
    a, b, c = 3, 2, 1
    new = 2*(a*b + b*c + a*c)               # 三个方向各一刀：每刀新增两个截面
    ans = new*50
    one(ans, [550, 1100, 1650, 2200])
    near(new/2*50, 550)
    assert new == 2*(a*b + b*c + a*c)       # = 原表面积
    return ans

@check('35-3-1')
def _():
    n = [n for n in range(3, 100) if 12*(n - 2) == 60][0]
    ans = 6*(n - 2)**2
    one(ans, [96, 125, 150, 216])
    near((n - 2)**3, 125)
    return ans

@check('35-3-2')
def _():
    a, b, c = 4, 5, 6
    cnt = {0: 0, 1: 0, 2: 0, 3: 0}
    for x in range(a):
        for y in range(b):
            for z in range(c):
                k = (x in (0, a - 1)) + (y in (0, b - 1)) + (z in (0, c - 1))
                cnt[k] += 1
    one(cnt[1], [24, 36, 52, 94])
    near(cnt[0], 24); near(cnt[2], 36)
    near(2*((a - 1)*(b - 1) + (a - 1)*(c - 1) + (b - 1)*(c - 1)), 94)
    return cnt[1]

@check('35-3-3')
def _():
    pts = {(x, y) for x in range(4) for y in range(4)}
    sq = set()
    for p, q in permutations(pts, 2):
        dx, dy = q[0] - p[0], q[1] - p[1]
        r, s = (q[0] - dy, q[1] + dx), (p[0] - dy, p[1] + dx)
        if r in pts and s in pts: sq.add(frozenset([p, q, r, s]))
    ans = len(sq)
    one(ans, [14, 17, 20, 22])
    assert sum(1 for S in sq if len({p[0] for p in S}) == 2) == 14   # 正放
    return ans

@check('35-3-4')
def _():
    n = [n for n in range(1, 30) if 1 + n*(n + 1)//2 == 37]
    assert n == [8]
    one(8, [7, 8, 9, 12])
    assert [m for m in range(1, 30) if 1 + m*(m - 1)//2 == 37] == [9]   # 漏了"+n"
    return 8

@check('35-4-1')
def _():
    v = [F(k, 3)**3 for k in (1, 2, 3)]
    layers = [v[0], v[1] - v[0], v[2] - v[1]]
    ans = layers[2]/layers[0]
    one(ans, [7, 9, 19, 27])
    return ans

@check('35-4-2')
def _():
    full = 4*(30/10)**3
    ans = full - 4
    one(ans, [8, 36, 104, 108])
    near(4*(30/10)**2, 36); near(full, 108)
    return ans

@check('35-4-3')
def _():
    exposed = (1 - 0.8)**(1/3)              # 尖朝上：露出的是顶部小圆锥
    assert 0.5 <= exposed < 0.6
    tip_down = 1 - 0.8**(1/3)               # 尖朝下时露出约 0.07
    assert tip_down < 0.1
    return exposed

@check('35-4-4')
def _():
    full = F(60**3 - 30**3); rest = F(45**3 - 30**3)
    poured = 1 - rest/full
    one(poured, [F(1, 2), F(19, 56), F(37, 56), F(7, 8)])
    assert rest/full == F(19, 56)
    near(1 - F(1, 2)**3, F(7, 8))           # 当成完整圆锥
    return poured

@check('35-4-5')
def _():
    R, H = 100, 300                          # 口半径 100mm，深 300mm
    V = pi*R*R*H/3
    w = V/(pi*R*R)
    one(w, [25, 50, 100, 300])
    return w

@check('35-5-1')
def _():
    a, b, c = 4, 2, 1
    cand = [math.hypot(a, b + c), math.hypot(a + b, c), math.hypot(a + c, b)]
    ans = min(cand)
    one(ans, [5, sqrt(21), sqrt(29), sqrt(37)])
    near(sqrt(a*a + b*b + c*c), sqrt(21))   # 体对角线（穿过内部）
    return ans

@check('35-5-2')
def _():
    ans = math.hypot(2*3, 8)
    one(ans, [8, 10, sqrt(73), 16])
    near(math.hypot(3, 8), sqrt(73))
    return ans

@check('35-5-3')
def _():
    l, r = 6, 2
    ang = 2*pi*r/l                          # 展开扇形圆心角
    ans = 2*l*math.sin(ang/2)
    one(ans, [6, 6*sqrt(3), 4*pi, 12])
    return ans

@check('35-5-4')
def _():
    v1 = pi*4**2*3/3; v2 = pi*3**2*4/3
    h = 3*4/5; v3 = pi*h*h*5/3
    ans = max(v1, v2, v3)/min(v1, v2, v3)
    one(ans, [4/3, 5/3, 16/9, 2])
    near(v1/v2, 4/3)
    return ans

@check('35-5-5')
def _():
    V = lambda C, h: (C/(2*pi))**2*pi*h
    ans = V(2, 1)/V(1, 2)
    one(ans, [1, 2, 4, pi])
    return ans

@check('35-6-1')
def _():
    a, b, c = 60, 40, 120
    ans = sqrt(a*a + b*b + c*c)/2
    one(ans, [60, 70, 10*sqrt(157), 140])
    near(sqrt((a/2)**2 + (b/2)**2 + c*c), 10*sqrt(157))   # 误用半球罩公式
    return ans

@check('35-6-2')
def _():
    ans = 1/math.cos(math.radians(30)) - 1
    one(ans, [2*sqrt(3)/3 - 1, 1, sqrt(2) - 1, sqrt(3) - 1])
    near(1/math.cos(math.radians(60)) - 1, 1)   # 把 ∠SOC 误当 60°
    return ans

@check('35-6-3')
def _():
    V = lambda th: 2*(4*math.cos(math.radians(th)))**2*4*math.sin(math.radians(th))/3
    ans = V(45)/V(60)
    one(ans, [sqrt(2), 2*sqrt(6)/3, 2, sqrt(3)])
    near((math.cos(math.radians(45))/math.cos(math.radians(60)))**2, 2)   # 只算了底面积
    return ans

@check('35-6-4')
def _():
    r = [t/100000 for t in range(1, 100000) if abs(sqrt(3)*(1 - t/100000) - (1 + t/100000)) < 2e-5]
    ans = 2 - sqrt(3)
    near(r[0], ans, 1e-4)
    one(ans, [2 - sqrt(3), sqrt(3) - 1, sqrt(2) - 1, 0.25])
    return ans

# =========================== 第 42 天 ===========================
@check('42-1-1')
def _():
    top, bot, h = 20, 40, 20                 # 下底 = 2×上底，斜腰 45°
    k = sqrt((top + bot)/2*h/4/((top + bot)/2*h))   # 4 块全等且与原图相似 → 相似比 1/2
    small = k*(top + bot + h + h*sqrt(2))
    ans = small
    one(ans, [20 + 5*sqrt(2), 40 + 10*sqrt(2), 60, 80 + 20*sqrt(2)])
    near((top + bot + h + h*sqrt(2))/4, 20 + 5*sqrt(2))
    return ans

@check('42-1-2')
def _():
    vals = set()
    for r in [5, 12, 20, 33]:
        R = math.hypot(r, 20)               # 弦长 40 与内圆相切
        vals.add(round((R*R - r*r)/pi*pi, 9))
    assert vals == {400.0}
    one(400*pi, [200*pi, 400*pi, 800*pi, 1600*pi])
    return 400*pi

@check('42-1-3')
def _():
    area = 1800*sqrt(3)/1.5
    a = sqrt(area/3/(sqrt(3)/4))
    ans = sqrt(3)/2*a
    one(ans, [20, 20*sqrt(3), 40, 40*sqrt(3)])
    near(a, 40)
    return ans

@check('42-2-1')
def _():
    slope = (101.6 - 1.6)/(40 + 160)
    ans = 1.6 + 40*slope
    one(ans, [20, 21.6, 25.6, 41.6])
    near(40*slope, 20)                      # 忘加眼高
    return ans

@check('42-2-2')
def _():
    r1, r2, d = 6, 8, 10
    x = (d*d + r1*r1 - r2*r2)/(2*d)
    ans = 2*sqrt(r1*r1 - x*x)
    one(ans, [4.8, 9.6, 10, 12])
    return ans

@check('42-2-3')
def _():
    a, b, c = 9, 12, 15
    r = (a + b - c)/2
    near(r, a*b/(a + b + c))
    ratio = pi*r*r/(a*b/2)
    assert 0.5 <= ratio < 0.6
    return ratio

@check('42-2-4')
def _():
    xs = [x for x in range(1, 100) if math.hypot(x, 6) + 6 - x == 12*40/60]
    assert xs == [8]
    one(8, [6, 8, 10, 12])
    return 8

@check('42-3-1')
def _():
    h = 40/(1/math.tan(math.radians(30)) - 1/math.tan(math.radians(45)))
    ans = h + 1.5
    one(ans, [20*(sqrt(3) + 1), 20*(sqrt(3) + 1) + 1.5, 20*sqrt(3) + 1.5, 40*sqrt(3) + 1.5])
    return ans

@check('42-3-2')
def _():
    hs = [h for h in [k/100 for k in range(1, 20000)] if abs(math.hypot(h, sqrt(3)*h) - 100) < 1e-6]
    assert hs == [50.0]
    one(50, [25, 50, 50*sqrt(2), 100*sqrt(3)/3])
    return 50

@check('42-3-3')
def _():
    dA = (math.sin(math.radians(60)), math.cos(math.radians(60)))
    dB = (math.sin(math.radians(30)), math.cos(math.radians(30)))
    # P = t·dA = (20,0) + s·dB
    s = 20*dA[1]/(dA[0]*dB[1] - dA[1]*dB[0])
    P = (20 + s*dB[0], s*dB[1])
    minutes = (P[0] - 20)/15*60
    one(minutes, [30, 40, 60, 80])
    near(P[1], 10*sqrt(3))
    return minutes

@check('42-4-1')
def _():
    def ratio(kd, ke, kf):                  # BD=kd·AB, CE=ke·BC, AF=kf·CA
        A, B, C = (0.0, 0.0), (1.0, 0.0), (0.37, 0.81)
        D = (B[0] + kd*(B[0]-A[0]), B[1] + kd*(B[1]-A[1]))
        E = (C[0] + ke*(C[0]-B[0]), C[1] + ke*(C[1]-B[1]))
        Fq = (A[0] + kf*(A[0]-C[0]), A[1] + kf*(A[1]-C[1]))
        ar = lambda P: abs(sum(P[i][0]*P[(i+1) % 3][1] - P[(i+1) % 3][0]*P[i][1] for i in range(3)))/2
        return ar([D, E, Fq])/ar([A, B, C])
    ans = 2*ratio(2, 2, 2)
    one(ans, [26, 38, 42, 56])
    near(2*(1 + 3*2*2), 26)                 # 外侧三角形误按 2×2
    near(2*(1 + 3*3*3), 56)                 # 误按 3×3
    return ans

@check('42-4-2')
def _():
    sol = [(a, 10 - a) for a in [k/1000 for k in range(5001, 10000)] if abs(a*(10 - a) - 6*(2*a - 10)**2) < 1e-6]
    assert len(sol) == 1
    a, b = sol[0]
    ans = (a - b)**2
    one(ans, [1, 4, 9, 16])
    return ans

@check('42-4-3')
def _():
    s = 4
    ans = s*s*(1 + pi/3 - sqrt(3))
    random.seed(3); N = 600000; hit = 0
    for _ in range(N):
        x, y = random.random()*s, random.random()*s
        if all(math.hypot(x - cx, y - cy) <= s for cx, cy in [(0, 0), (s, 0), (0, s), (s, s)]): hit += 1
    near(hit/N*s*s, ans, 0.05)
    opts = [16 + 16*pi/3 - 16*sqrt(3), 8*pi - 8*sqrt(3), 16*pi/3 - 4*sqrt(3), 32 - 8*pi]
    one(ans, opts)
    near((pi - sqrt(3))/2*s*s, 8*pi - 8*sqrt(3))   # 误当成莱洛三角形
    return ans

@check('42-4-4')
def _():
    a, b, c = 4, 6, 9                       # AOB, BOC, COD
    d = a*c/b
    p = d/(a + b + c + d)
    one(p, [0.16, 0.20, 0.24, 0.42], 0.005)
    d2 = b*c/a; near(d2/(a + b + c + d2), 0.42, 0.005)   # 误配对
    return p

@check('42-5-1')
def _():
    f = lambda x: x + 192/x                  # 靠墙边 x≤10
    g = lambda x: (x - 10) + x + 192/x      # 若 x>10，超出墙长部分要补新围栏
    best = min([f(x/100) for x in range(100, 1001)] + [g(x/100) for x in range(1001, 3000)])
    one(best, [27.7, 28, 29.2, 32], 0.05)
    near(2*sqrt(192), 27.7, 0.05)            # 忽略墙长限制
    near(f(12), 28); near(f(8), 32)
    return best

@check('42-5-2')
def _():
    A, B, C, D = (0, 8), (0, 0), (8, 0), (8, 8)
    E = (2, 0)
    best = min(math.dist((t, 8 - t), B) + math.dist((t, 8 - t), E) for t in [k/10000 for k in range(0, 80001)])
    opts = [8, 2*sqrt(17), 10, 4*sqrt(2) + 2*sqrt(5)]
    one(best, opts, 1e-4)
    near(math.dist((4, 4), B) + math.dist((4, 4), E), 4*sqrt(2) + 2*sqrt(5))   # 取对角线中点
    near(math.dist(A, E), 2*sqrt(17))       # 误以为最小值是 AE
    return best

@check('42-5-3')
def _():
    hA, hB, gap, dock = 3, 5, 8, 2
    best = min(math.hypot(p, hA) + math.hypot(gap - p - dock, hB) for p in [k/1000 for k in range(-5000, 13001)])
    one(best, [2*sqrt(10), 10, 8*sqrt(2), 12], 1e-4)
    near(math.hypot(gap - dock, hB - hA), 2*sqrt(10))   # 平移后忘了对称
    near(math.hypot(gap, hA + hB), 8*sqrt(2))           # 没平移
    return best

@check('42-5-4')
def _():
    best = max(x*x*(48 - x*x)/(4*x) for x in [k/1000 for k in range(1, 6928)])
    one(best, [24, 27, 32, 36], 1e-4)
    return best

@check('42-6-1')
def _():
    sq = [(a2, b2, c2) for a2 in range(1, 15) for b2 in range(1, 15) for c2 in range(1, 15)
          if a2 + b2 == 5 and a2 + c2 == 10 and b2 + c2 == 13]
    assert sq == [(1, 4, 9)]
    ans = sqrt(1*4*9)
    one(ans, [6, sqrt(14), 12, 5*sqrt(26)])
    near(sqrt(5*10*13), 5*sqrt(26))          # 误把三条面对角线相乘
    return ans

@check('42-6-2')
def _():
    r = min(3, 4/2)
    keep = (4/3*pi*r**3)/(pi*3*3*4)
    ans = 1 - keep
    one(ans, [2/3, 19/27, 8/27, 1/2])
    near(4/3*pi*27, pi*9*4)                 # 陷阱：半径误取 3 时，球的体积竟等于整根圆柱（削去 0），说明受高度限制
    return ans

@check('42-6-3')
def _():
    water = 1 - (1/2)**3                    # 尖朝上（底在下）水深一半：水 = 7/8
    d = water**(1/3)                        # 倒过来尖朝下：水成小圆锥
    assert d > 0.9
    assert 0.8 <= water < 0.9               # 忘开立方 → 0.875 落在 0.8~0.9
    return d

@check('42-6-4')
def _():
    V = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    def right(t):
        a, b, c = t
        for p, q, r in [(a, b, c), (b, a, c), (c, a, b)]:
            if sum((q[i] - p[i])*(r[i] - p[i]) for i in range(3)) == 0: return True
        return False
    ans = sum(right(t) for t in combinations(V, 3))
    one(ans, [24, 32, 48, 56])
    return ans

@check('42-7-1')
def _():
    W, L, a, b, g = 70, 355, 40, 25, 5
    bound = ((W + g)*(L + g))//((a + g)*(b + g))
    two_band = (L + g)//(b + g) + (L + g)//(a + g)
    assert (a + g) + (b + g) == W + g       # 一排竖放 + 一排横放恰好占满宽度
    assert bound == two_band == 20
    one(20, [16, 18, 20, 24])
    assert (W*L)//(a*b) == 24               # 忽略间隔直接用面积比
    return 20

@check('42-7-2')
def _():
    N, c = 5, 2
    rem = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                plus = lambda u, v: u == c or v == c
                if not (plus(y, z) or plus(x, z) or plus(x, y)): rem += 1
    one(rem, [48, 56, 64, 80])
    near(125 - 9*5, 80)                     # 只挖了一组对面
    return rem

@check('42-7-3')
def _():
    # 从顶点 A 引 4 条线到底边（含 AB、AC 共 6 条过 A 的线），另有 2 条平行于 BC 的线（含 BC 共 3 条横线）
    lines_A = 6; horiz = 3
    # 暴力：用坐标生成直线，枚举三线组成的三角形（两两相交且不共点）
    A = (0.0, 6.0); base_pts = [(-3 + 1.2*i, 0.0) for i in range(6)]
    Ls = [('A', A, p) for p in base_pts] + [('H', (-10, y), (10, y)) for y in (0.0, 2.0, 4.0)]
    def inter(l1, l2):
        (_, p1, p2), (_, p3, p4) = l1, l2
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
        den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if abs(den) < 1e-12: return None
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/den
        return (round(x1 + t*(x2-x1), 9), round(y1 + t*(y2-y1), 9))
    def inside(P):                           # 交点须在大三角形内（含边界）
        x, y = P
        return -1e-9 <= y <= 6 + 1e-9 and abs(x) <= 3*(6 - y)/6 + 1e-9
    cnt = 0
    for l1, l2, l3 in combinations(Ls, 3):
        P = [inter(l1, l2), inter(l2, l3), inter(l1, l3)]
        if None in P or len(set(P)) < 3: continue
        if all(inside(p) for p in P): cnt += 1
    assert cnt == math.comb(lines_A, 2)*horiz
    one(cnt, [15, 30, 45, 60])
    return cnt

@check('42-8-1')
def _():
    k = F(1, 2)                             # AD:BC
    up, side, down = k*k, k, 1              # 上:左:下 = 1:2:4（右同左）
    jia = up + down; yi = 2*side
    tj = jia/F(3, 2); ty = yi/1
    early = abs(ty - tj)/max(ty, tj)
    one(early, [F(1, 6), F(1, 5), F(1, 4), F(1, 3)])
    return early

@check('42-8-2')
def _():
    P = [(math.cos(2*pi*k/8), math.sin(2*pi*k/8)) for k in range(8)]
    def contains(t):
        (x1, y1), (x2, y2), (x3, y3) = t
        cr = lambda ax, ay, bx, by: ax*by - ay*bx
        d1 = cr(x2-x1, y2-y1, -x1, -y1); d2 = cr(x3-x2, y3-y2, -x2, -y2); d3 = cr(x1-x3, y1-y3, -x3, -y3)
        return (d1 > 1e-9 and d2 > 1e-9 and d3 > 1e-9) or (d1 < -1e-9 and d2 < -1e-9 and d3 < -1e-9)
    ans = sum(contains(t) for t in combinations(P, 3))
    one(ans, [8, 16, 24, 32])
    rightT = sum(1 for t in combinations(range(8), 3) if any((t[i] - t[j]) % 8 == 4 for i in range(3) for j in range(3)))
    assert rightT == 24 and 56 - rightT == 32
    return ans

@check('42-8-3')
def _():
    V = [(0, 0), (6, 1), (5, 5), (1, 4)]
    area = abs(sum(V[i][0]*V[(i+1) % 4][1] - V[(i+1) % 4][0]*V[i][1] for i in range(4)))/2
    # 整格计数（完全落在四边形内的 1×1 小格数）
    def inside(x, y):
        s = None
        for i in range(4):
            (x1, y1), (x2, y2) = V[i], V[(i+1) % 4]
            c = (x2 - x1)*(y - y1) - (y2 - y1)*(x - x1)
            if abs(c) < 1e-12: continue
            if s is None: s = c > 0
            elif s != (c > 0): return False
        return True
    full = sum(1 for i in range(6) for j in range(5) if all(inside(i + dx, j + dy) for dx in (0, 1) for dy in (0, 1)))
    ha = area*100*100/10000                  # 每格 100 米 → 1 格² = 1 公顷
    Bpts = sum(math.gcd(abs(V[(i+1) % 4][0] - V[i][0]), abs(V[(i+1) % 4][1] - V[i][1])) for i in range(4))
    I = area - Bpts/2 + 1                     # 皮克定理反推内部格点数
    opts = [12, 19, 20, 21]
    one(ha, opts)
    near(full, 12)                            # 只数完整小格
    near(I, 19)                               # 把内部格点数当面积
    near(30 - (3 + 2 + 2 + 2), 21)            # 割补时把左上角的四边形当成一个直角三角形
    return ha

# =========================== 备用 idea（真题被剔除或答案存疑时补位） ===========================
@check('B-2021SD-41')
def _():
    side, Rcov = 60, 40
    circ = side/sqrt(3)
    h = sqrt(Rcov**2 - circ**2)
    one(h, [10, 20, 20*sqrt(2), 20*sqrt(3)])
    return h

@check('B-2021GK-74')
def _():
    hs = [h for h in [k/100 for k in range(1, 3000)] if abs(((2 + 0.25*h)/2)**3 - F(27, 8)) < 1e-9]
    assert hs == [4.0]
    one(4, [3, 4, 5, 6])
    return 4

@check('B-2021GK-70')
def _():
    s = 120/sqrt(3)                          # 高 60 的正三角形边长
    area = 3*sqrt(3)/4*s*s + 2*(0.5*s*s*sqrt(3))
    t = area*1.5/1000
    one(t/sqrt(3), [10.8, 12.6, 14.4, 16.8])
    return t

@check('B-2021SD-36')
def _():
    xs = [x for x in range(1, 100) if math.hypot(x, 5) + 5 == 1.5*x]
    assert xs == [12]
    one(12, [10, 12, 13, 15])
    return 12

@check('B-2022SC1-53')
def _():
    r, d = 6, 6
    lens = 2*r*r*math.acos(d/(2*r)) - (d/2)*sqrt(4*r*r - d*d)
    one(lens, [12*pi - 9*sqrt(3), 24*pi - 18*sqrt(3), 24*pi - 36*sqrt(3), 36*pi - 18*sqrt(3)])
    return lens

@check('B-2023SZ-51')
def _():
    r, R = 3, 6
    h0 = (R*R*2*r - 4/3*r**3)/(R*R)
    one(h0, [4, 4.5, 5, 5.5])
    return h0

if __name__ == '__main__':
    out = {}
    for cid, fn in CHECKS.items():
        out[cid] = fn()
    for cid, v in out.items():
        print(f'{cid:14s} {v}')
    print('全部通过：', len(out), '条（含备用）')
