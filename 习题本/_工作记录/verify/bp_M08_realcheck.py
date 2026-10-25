# -*- coding: utf-8 -*-
# M08 几何问题：真题独立复算（从题面数据出发，不代入预期答案）。
# 覆盖全部有官方答案的真题 + 2 道建议剔除题；6 道自解题见 bp_M08_selfsolve.py；6 道待识别答案的题只算参考值。
import math, itertools, json
from fractions import Fraction as F

pi, sqrt = math.pi, math.sqrt
OFFICIAL = {q['id']: q['answer_official'] for q in json.load(open(
    '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tasks_in/M08.json'))['real']}

def pick(val, opts, tol=1e-6):
    hits = [k for k, v in opts.items() if (v(val) if callable(v) else abs(v - val) <= tol)]
    assert len(hits) == 1, (val, opts, hits)
    return hits[0]

def shoelace(p):
    return abs(sum(p[i][0]*p[(i+1) % len(p)][1] - p[(i+1) % len(p)][0]*p[i][1] for i in range(len(p)))) / 2

def inter(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))

R = {}
def rng(lo, hi):            # option "在 lo~hi 之间"
    return lambda v: lo <= v < hi

# ---------------- 难度 1 ----------------
R['2020HB-69'] = pick((pi*10**2*6/3)/(pi*5**2), {'A': 4, 'B': 6, 'C': 8, 'D': 12})
s = 20/2; R['2020JSA-55'] = pick(3*s + 9, {'A': 42, 'B': 24, 'C': 28, 'D': 39})          # (L+3)(W+3)-LW
R['2020ZJB-12'] = pick(6*(1/0.2)**2, {'A': 30, 'B': 60, 'C': 150, 'D': 180})
r_small = 15/2; r_big = r_small*math.sqrt(16/9)
R['2020ZJB-18'] = pick((2*pi*r_big + 2*pi*r_small)/(pi*0.5), {'A': 50, 'B': 60, 'C': 70, 'D': 90})
n = [n for n in range(3, 50) if 6*(n-2)**2 == (n-2)**3][0]
R['2022SD-36'] = pick(n, {'A': 4, 'B': 6, 'C': 16, 'D': 8})
x = [x for x in range(3, 30) if x*x*(x-2) == 144][0]
R['2023GD-34'] = pick(x, {'A': 4, 'B': 6, 'C': 8, 'D': 10})
best = min(4*2*(a + 36/a) for a in [i/100 for i in range(100, 3601)])                    # 底面积36，侧面积=4×周长
R['2023HB-70'] = pick(round(best, 6), {'A': 24, 'B': 36, 'C': 96, 'D': 132})
lo, hi = (1000/200)**2, (3000/100)**2
R['2023JSA-53'] = pick((lo, hi), {'A': lambda v: v == (100, 225), 'B': lambda v: v == (100, 900),
                                 'C': lambda v: v == (25, 225), 'D': lambda v: v == (25, 900)})
minutes = 40*pi/(2*pi*4); area = pi*3**2*minutes/60
R['2023ZJA-66'] = pick(area/pi, {'A': 0.5, 'B': 0.75, 'C': 1, 'D': 1.5})
A = (0, 0); B = (6*math.cos(math.radians(120)), 6*math.sin(math.radians(120))); C = (-6, 0)   # 北偏西30°、正西
R['2024GD-38'] = pick(math.dist(B, C), {'A': 3, 'B': 4, 'C': 5, 'D': 6})
areas = [w*(10-w) for w in range(1, 10)]                                                     # 每块周长20，整米
R['2024HB-64'] = pick(max(areas) - min(areas), {'A': 10, 'B': 12, 'C': 16, 'D': 25})

# ---------------- 难度 2 ----------------
# 2020HB-68：A左上、C右上、B左下、D右下；A+D周长=B+C周长=大矩形周长
pD = 24 + 28 - 20
R['2020HB-68'] = pick(max(w*(pD/2 - w) for w in [i/100 for i in range(1, int(pD/2*100))]), {'A': 42, 'B': 49, 'C': 64, 'D': 81}, 1e-3)
# 2020HB-74
jia = (0, 0); yi = (0, -2); bing = (yi[0] - 2*math.sin(math.radians(60)), yi[1] + 2*math.cos(math.radians(60)))
d = (-math.sin(math.radians(75)), math.cos(math.radians(75)))
t = [k/10000 for k in range(1, 50000) if abs(math.dist((k/10000*d[0], k/10000*d[1]), jia) - math.dist((k/10000*d[0], k/10000*d[1]), bing)) < 2e-4]
R['2020HB-74'] = pick(sum(t)/len(t), {'A': 1, 'B': sqrt(2), 'C': sqrt(3), 'D': 2}, 1e-3)
# 2020SC0725-55：长方体(上下左右后) + 半圆柱(两个半圆端面+曲面)
S = 2*0.5*1 + 2*0.5*2 + 1*2 + pi*0.5**2 + pi*0.5*2
R['2020SC0725-55'] = pick(200/S, {'A': rng(0, 20.0000001), 'B': rng(20.0000001, 25.0000001), 'C': rng(25.0000001, 30.0000001), 'D': rng(30.0000001, 1e9)})
R['2020SC1206-44'] = pick((40/2 + 80) - ((40 + 80)/2 + 60/2), {'A': 10, 'B': 15, 'C': 20, 'D': 25})
half = 2.4; top = sqrt(4**2 - half**2) - 1.1
R['2020SD-41'] = pick(math.floor(top/0.2 + 1e-9), {'A': 9, 'B': 10, 'C': 11, 'D': 12})
R['2021JSA-65'] = pick(1/math.cos(math.radians(45)) - 1, {'A': (sqrt(2)-1)/2, 'B': (2-sqrt(2))/2, 'C': sqrt(2)-1, 'D': 2-sqrt(2)})
# 2022GD-39：影长与人到灯的距离 d：1.6/H = 3.2/(3.2+d) = 1.6/(1.6+d-1)
dd = [k/1000 for k in range(1, 20000) if abs(3.2*(0.6 + k/1000) - 1.6*(3.2 + k/1000)) < 1e-9][0]
R['2022GD-39'] = pick(1.6*(3.2 + dd)/3.2, {'A': 2.6, 'B': 2.8, 'C': 3.2, 'D': 3.4})
# 2022GK-73：圆柱 r=√2/2,h=1 切成棱长1的正方体，切下四块的总表面积
r = sqrt(2)/2
val = 2*pi*r*1 + 2*(pi*r*r - 1) + 4*1*1
gk73 = pick(val, {'A': sqrt(2)*(pi+2), 'B': 2*sqrt(2)*(pi-2), 'C': (sqrt(2)+1)*pi + 2, 'D': 2*sqrt(2)*pi - 2})
R['2022GK-73'] = gk73
# 2022JSA-59：∠B=90°，∠A=30°，△ADE∽△ABC(∠ADE=90°)，面积比1:3
AB = 1.0; AC = AB/math.cos(math.radians(30)); AE = AC/sqrt(3)
R['2022JSA-59'] = pick(AE/(AB-AE), {'A': 2, 'B': 1.5, 'C': sqrt(3), 'D': 2/sqrt(3)})
R['2022ZJA-67'] = pick(2 + math.hypot(12, 4 + 1), {'A': 17, 'B': 15, 'C': 19, 'D': 20})
R['2022ZJA-68'] = pick((math.sin(math.radians(60))/math.sin(math.radians(30)))**2, {'A': 3*sqrt(2), 'B': sqrt(3), 'C': 2, 'D': 3})
# 2023GK-67：正方形边3，三角形面积=3（总面积1/3）
xx = 2*3/3
tri = 3 + xx + math.hypot(3, xx); trap = 3 + 3 + (3 - xx) + math.hypot(3, xx)
R['2023GK-67'] = pick(tri/trap, {'A': 1/2, 'B': 5/7, 'C': (1+sqrt(5))/(2+sqrt(5)), 'D': (5+sqrt(13))/(7+sqrt(13))})
# 2023HB-69：楔形屋顶 底4×3，高1，上棱2（居中）：屋面高度 z=min(四个面)，对底面做数值积分
def wedge(a, b, c, h, N=800):
    off = (a - c)/2; tot = 0
    for i in range(N):
        x = (i + 0.5)/N*a
        for j in range(N):
            y = (j + 0.5)/N*b
            tot += min(h*y/(b/2), h*(b - y)/(b/2), h*x/off, h*(a - x)/off)
    return tot*(a/N)*(b/N)
R['2023HB-69'] = pick(wedge(4, 3, 2, 1), {'A': 5, 'B': 11, 'C': 12, 'D': 24}, 1e-2)
# 2023JSA-57：圆柱 r=2h，半球体积=9/16圆柱
k = ((9/16)*(pi*1*1*0.5))/((2/3)*pi)       # R^3, 取 r=1
R['2023JSA-57'] = pick(k**(1/3), {'A': 1/4, 'B': 1/3, 'C': 2/3, 'D': 3/4})
# 2023JSA-59：AB=10,BC=8,AC=6；沿AD折叠 AC 落到 AB
cd = [k/1000 for k in range(1, 8000) if abs((k/1000)**2 + 4**2 - (8 - k/1000)**2) < 1e-9][0]
R['2023JSA-59'] = pick(0.5*(8 - cd)*6, {'A': 15, 'B': 16, 'C': 18, 'D': 21})
Ex = 8**2/10                                 # E 到 AD 的距离 = AE²/AB
R['2023SC-47'] = pick(0.5*10*Ex, {'A': 24, 'B': 32, 'C': 44, 'D': 48})
R['2023SC-53'] = pick(50*40 - 50*2 - 1*(40 - 2), {'A': 1862, 'B': 1880, 'C': 1950, 'D': 1960})
W = 4 + sqrt(12)                             # 大圆心(3,3)，小圆心(W-1,5)，距离4
R['2023ZJA-62'] = pick(6*W, {'A': 12*(2+sqrt(3)), 'B': 12*(1+2*sqrt(3)), 'C': 12*sqrt(13), 'D': 6*(3+sqrt(13))})
A = (0, 100); B = (0, 0); C = (sqrt(200**2 - 100**2), 0)
D = (C[0]/2, -C[0]*sqrt(3)/2)                # 正三角形 BCD 在 BC 南侧
R['2024GK-70'] = pick(math.dist(A, D), {'A': 150*sqrt(3), 'B': 50*(sqrt(3)+1), 'C': 100*sqrt(7), 'D': 200*sqrt(2)})
AE = 2.23 - 1; BC = 2 - AE
R['2024HB-71'] = pick(round(BC/4*60), {'A': 8, 'B': 10, 'C': 12, 'D': 14})
def frustum_lat(R_, r_, h): return pi*(R_ + r_)*math.hypot(h, R_ - r_)
R['2024JSA-58'] = pick(frustum_lat(35, 25, 80)/frustum_lat(30, 22.5, 60), {'A': 16/7, 'B': 32/21, 'C': 48/35, 'D': 64/49})
side = 2*sqrt(3)                             # △ACE 边长
R['2024JSA-65'] = pick(pi*(side*sqrt(3)/6)**2/pi, {'A': 1, 'B': 2, 'C': 5/4, 'D': 1.5})
for t in [5, 10, 20, 30]:                     # 2024ZJA-65：AG=DE=CF=t，DF=80，BC=160；结果与 t 无关
    a = 80 - t
    v = 0.5*(t + a)*(a - t) + 0.5*t*160
    assert abs(v - 3200) < 1e-9
R['2024ZJA-65'] = pick(v, {'A': 3200, 'B': 3600, 'C': 4000, 'D': 4800})
pts = {(x, y) for x in range(-3, 4) for y in range(-3, 4) if abs(x) + abs(y) <= 3}
assert len(pts) == 25
sides = set()
for (x1, y1), (x2, y2) in itertools.permutations(pts, 2):
    dx, dy = x2-x1, y2-y1
    if (x2-dy, y2+dx) in pts and (x1-dy, y1+dx) in pts: sides.add(dx*dx + dy*dy)
R['2024ZJA-67'] = pick(len(sides), {'A': 4, 'B': 5, 'C': 6, 'D': 7})
A = (0, 100); B = (0, 0); E = (-60, 0); Fp = (-60, 250); Dp = (240, 100)   # E 的位置任取（结果与 BE 无关）
G = inter(E, Dp, A, B)
R['2025GK-78'] = pick(shoelace([A, Dp, G, Fp])/1e4, {'A': 1.2, 'B': 1.3, 'C': 1.4, 'D': 1.5})
cone_min = 1*(12/6)**3                       # 圆锥注满用时
cyl_per_cm = cone_min*3/12                   # 同底圆柱每厘米 = 圆锥体积×3/12
R['2025GK-80'] = pick(12 + (30 - (cone_min - 1))/cyl_per_cm, {'A': 22, 'B': 22.5, 'C': 23, 'D': 23.5})
R['2025HB-67'] = pick((pi - math.radians(60))*1, {'A': pi/4, 'B': pi/2, 'C': 2*pi/3, 'D': 3*pi/4})
R['2025HB-74'] = pick((110+115+125+130)/((20 + 40)/2*20), {'A': 0.6, 'B': 0.8, 'C': 1, 'D': 1.25})
R['2025HB-77'] = pick((pi*50**2 + pi*5*(100 + 80 + 68))/pi, {'A': 3740, 'B': 5256, 'C': 6240, 'D': 6496})
R['2025HB-79'] = pick((F(2, 3)**3)/(1 - F(2, 3)**3), {'A': F(8, 27), 'B': F(19, 27), 'C': F(19, 8), 'D': F(8, 19)}, 0)
xw = [x for x in range(1, 500) if F(23.7 - 1.7).limit_denominator()/x == F(111.7 - 1.7).limit_denominator()/(x + 200)]
R['2025JSA-59'] = pick(xw[0], {'A': 30, 'B': 40, 'C': 50, 'D': 60})
boc = 15*12/9
R['2025ZJA-66'] = pick(2*(boc + 12)/8, {'A': 6, 'B': 7, 'C': 8, 'D': 9})

# ---------------- 难度 3 ----------------
full = 2**3 - 1; halfv = 1.5**3 - 1
y = 4.5*halfv/(full - halfv)                 # 剩余水重：倒出4.5 对应 full-half
R['2020SC0725-54'] = pick(4.5 - y, {'A': rng(0, 1.5), 'B': rng(1.5, 2), 'C': rng(2, 2.5), 'D': rng(2.5, 1e9)})
S2 = S3 = 2/2; S1 = 3 - S2                   # 斜放面积=两侧正放面积和
R['2020SC1206-49'] = pick(S1 + S2 + S3, {'A': 4, 'B': 5, 'C': 11, 'D': 13})
xs = [x for x in range(1, 1000) if 200**2 + (2*x)**2 == 2*(100 + x)**2]
R['2022JSA-67'] = pick(100 + xs[0], {'A': 100*sqrt(2), 'B': 150, 'C': 100*sqrt(3), 'D': 200})
# 2022SC2-44：坐标(x 左右, y 前后, z 高)，按解析图读出的 8 个贯穿孔
holes = [('y', 3, 3), ('y', 2, 2),                       # D、E：正面，沿前后贯穿 (x,z)
         ('z', 2, 4), ('z', 3, 3), ('z', 3, 2),          # A、B、C：顶面，沿上下贯穿 (x,y)
         ('x', 3, 3), ('x', 3, 2), ('x', 2, 2)]          # F、G、H：右面，沿左右贯穿 (y,z)
removed = set()
for ax, u, v in holes:
    for t in range(1, 5):
        removed.add({'y': (u, t, v), 'z': (u, v, t), 'x': (t, u, v)}[ax])
R['2022SC2-44'] = pick(64 - len(removed), {'A': 32, 'B': 40, 'C': 42, 'D': 48})
Wd, Ht = 17.5, 20.0                          # 长方形面积350，任取长宽
p_ = 100/Ht; q_ = 140/Wd
R['2022ZJA-65'] = pick(350 - 50 - 70 - (Wd - p_)*(Ht - q_)/2, {'A': 150, 'B': 155, 'C': 175, 'D': 180})
rr = 0.75; off = 2 - 2*rr                     # 珠心可横向错开 0.5
s = sqrt((2*rr)**2 - off**2)
R['2022ZJA-69'] = pick(1 + math.floor((20 - 2*rr)/s + 1e-9), {'A': 10, 'B': 13, 'C': 14, 'D': 20})
A = (0.3, 1.0); B = (0.0, 0.0); C = (1.0, 0.0)
E = (A[0] + (B[0]-A[0])/3, A[1] + (B[1]-A[1])/3); Fq = (A[0] + 2*(B[0]-A[0])/3, A[1] + 2*(B[1]-A[1])/3)
D = ((A[0]+C[0])/2, (A[1]+C[1])/2); O = inter(E, C, Fq, D)
R['2023GK-64'] = pick(shoelace([A, B, C])/shoelace([E, O, D]), {'A': 9, 'B': 12, 'C': 16, 'D': 18})
mass = 0.9**3; exposed = (1 - mass/1.5)**(1/3)
R['2023GK-75'] = pick(exposed, {'A': rng(0.8, 9), 'B': rng(0.7, 0.8), 'C': rng(0.6, 0.7), 'D': rng(0, 0.6)})
a = 2.0; h = a/2                              # 2024GK-71：角上等腰直角三角形直角边a，梯形高a/2
s_in = (a*a/h + a)/2                          # 梯形面积(2s-a)/2*h = a²/2
R['2024GK-71'] = pick((4*a*a/2)/(s_in*s_in), {'A': 2/3, 'B': 4/3, 'C': 8/9, 'D': 16/9})
side = sqrt(25)
reuleaux = (pi - sqrt(3))/2*side**2
R['2024HB-69'] = pick(reuleaux, {'A': 25*pi/6 - 25*sqrt(3)/6, 'B': 25*pi/4 - 25*sqrt(3)/4, 'C': 25*pi/3 - 25*sqrt(3)/3, 'D': 25*pi/2 - 25*sqrt(3)/2})
w = (pi*(150*200/400)**2*200/3)/(pi*150**2)
R['2024HB-70'] = pick(w, {'A': rng(50, 100), 'B': rng(25, 50), 'C': rng(10, 25), 'D': rng(0.1, 10)})
be_max = 5; be_min = 13 - sqrt(13**2 - 5**2)
R['2024SC-53'] = pick(be_max - be_min, {'A': 3, 'B': 4, 'C': 5, 'D': 6})
# 2024SC-55：A(0,80) B(80,80) C(80,0) D(0,0)；E 在 AB 中点正北30；F 在 C 东偏南45°、40√2
E = (40, 110); Fq = (80 + 40, -40)
via_B = math.dist(E, (80, 80)) + math.dist((80, 80), Fq)
via_D = math.dist(E, (0, 80)) + 80 + math.dist((0, 0), Fq)
R['2024SC-55'] = pick(via_D - via_B, {'A': 30, 'B': 50, 'C': 40*sqrt(2), 'D': 80})
a = 6/sqrt(2); Bp = (a, a); E = (0, a/2)       # B(0,0) A(0,a) C(a,0)；B 关于 AC 的对称点 (a,a)
t = (a - E[1]) / ((Bp[1]-E[1]) + (Bp[0]-E[0]))  # EB' 与 x+y=a 的交点
Fq = (E[0] + t*(Bp[0]-E[0]), E[1] + t*(Bp[1]-E[1]))
R['2025HB-78'] = pick(math.dist(Fq, (0, a)), {'A': sqrt(2), 'B': 1.5, 'C': 2, 'D': 3})
R2 = 20*sqrt(2)
lune = 0.5*pi*20**2 - (0.25*pi*R2**2 - 0.5*R2**2)
R['2025HB-80'] = pick(lune, {'A': 400, 'B': 200*pi, 'C': 800, 'D': 400*pi})
upright = 2*((30**2 + 20**2 + 60**2)/1e4)      # 竖放、只算半球曲面（官方约定）
R['2025JSA-65'] = pick(upright*pi, {'A': 1.47*pi, 'B': 1.02*pi, 'C': 0.98*pi, 'D': 0.68*pi})
# 2025SC-48：外扩2.5cm 模型：钢片75×45，钢板705×120；竖放(75高)两两x向不重叠，横放(45高)同一x处至多两层
best = 0
for n75 in range(0, 705//45 + 1):
    n45 = (1410 - 45*n75)//75
    best = max(best, n75 + n45)
assert best == 24 and (705//45) + (705//75) == 24          # 上界24，且两带排法可达
R['2025SC-48'] = pick(best, {'A': 23, 'B': 24, 'C': 25, 'D': 26})
k = F(1); A_ = 21*k; B_ = 14*k; C_ = 9*k        # B:C=14:9，B+C=(1+2/21)A
assert B_ + C_ == A_*(1 + F(2, 21))
R['2025SC-49'] = pick(B_*C_/A_/A_, {'A': F(1, 3), 'B': F(2, 5), 'C': F(2, 7), 'D': F(3, 11)}, 0)
ABl = 2; r_c = 1                                # D 到圆的最短距离 = AB/2 = 1；OD=2r
assert abs(2*r_c - r_c - ABl/2) < 1e-12
R['2025ZJA-69'] = pick(0.5*ABl*ABl*sqrt(3)/(pi*r_c**2), {'A': rng(0, 1), 'B': rng(1, 1.5), 'C': rng(1.5, 2), 'D': rng(2, 99)})
A = (0.0, 0.0); B = (1.0, 0.0); C = (0.3, 0.8)
D = (B[0] + (B[0]-A[0]), B[1] + (B[1]-A[1]))            # AB 延长一倍
E = (C[0] + 2*(C[0]-B[0]), C[1] + 2*(C[1]-B[1]))        # BC 延长两倍
Fq = (A[0] + 3*(A[0]-C[0]), A[1] + 3*(A[1]-C[1]))       # CA 延长三倍
ratio = shoelace([D, E, Fq])/shoelace([A, B, C])
need = (ratio - 1)*2/5                                     # 每单位面积 2 人·天
R['2026CQ-65'] = pick(math.ceil(need - 1e-9) - 2, {'A': 3, 'B': 5, 'C': 6, 'D': 12})
hO = 60*math.tan(math.radians(45)) + 1.8
dist = (hO - 1.8)/math.tan(math.radians(60))       # 站在叶片OA端点正下方：水平距离 = 叶长×cos30°
L = dist/math.cos(math.radians(30))
R['2026CQ-66'] = pick(hO + L, {'A': 81.8, 'B': 89.8, 'C': 95.8, 'D': 101.8})

# ---------------- 建议剔除的两题（只做核查） ----------------
excl = {}
excl['2022JSA-55'] = {'A': math.e - 1/math.e, 'B': 2.0, 'C': (2/3)*4**1.5, 'D': 8/3}      # 积分值
a_, b_ = 40, 20
t2 = 1/(1/a_**2 + 1/b_**2)
excl['2023JSA-55'] = {'内接矩形最大(官方口径)': 2*a_*b_, '内接正方形最大(方阵口径)': 4*t2}

# ---------------- 待识别答案（只给参考值，不作为答案） ----------------
ref = {}
s = 200/sqrt(3)                                      # 2021GK-70：高100的正三角形边长
area = 3*sqrt(3)/4*s*s + 2*(0.5*s*s*sqrt(3))
ref['2021GK-70'] = pick(area*1.2/1000, {'A': 72/sqrt(3), 'B': 84/sqrt(3), 'C': 108/sqrt(6), 'D': 126/sqrt(6)})
h0 = [k/100 for k in range(1, 2000) if abs(((3 + 0.2*k/100)/3)**3 - (1 + 61/64)) < 1e-9][0]
ref['2021GK-74'] = pick(h0, {'A': 3.5, 'B': 3.75, 'C': 4.25, 'D': 4.5})
xs = [k/1000 for k in range(1, 20000) if abs(math.hypot(k/1000, 2.1) + 2.1 - 4/3*k/1000) < 1e-6]
ref['2021SD-36'] = pick(xs[0], {'A': rng(0, 5), 'B': rng(5, 6), 'C': rng(6, 7), 'D': rng(7, 99)})
Rcov = 110*sqrt(3)/3                                   # 假设被裁掉的覆盖半径为 110√3/3（与选项吻合的唯一常见写法）
ref['2021SD-41(若半径为110√3/3)'] = pick(sqrt(Rcov**2 - (100/sqrt(3))**2), {'A': 15*sqrt(5), 'B': 10*sqrt(7), 'C': 5*sqrt(21), 'D': 15*sqrt(21)})
lens = 2*2*2*math.acos((2*sqrt(2))/(2*2)) - (2*sqrt(2)/2)*sqrt(4*4 - 8)
gray = 4*lens; union = 5*pi*4 - gray; black = 64 - union
diff = gray - black
ref['2022SC1-53'] = pick(diff, {'A': rng(-5, 0), 'B': rng(-99, -5), 'C': rng(0, 5), 'D': rng(5, 99)})
# 2023SZ-51：水 π·36·5 = π·36·2r − (4/3)πr³ ⇔ r³ − 54r + 135 = 0，球须放得进瓶(r≤6)
cands = [r_ for r_ in (3, 4, 5, 6) if abs(36*5 - (36*2*r_ - 4/3*r_**3)) < 1e-9]
ref['2023SZ-51'] = pick(cands[0], {'A': 3, 'B': 4, 'C': 5, 'D': 6}) if len(cands) == 1 else cands
other_root = (-3 + sqrt(9 + 180))/2

if __name__ == '__main__':
    bad = []
    for k, v in R.items():
        off = OFFICIAL.get(k)
        flag = '' if v == off else '  <-- 与库内官方答案不同'
        if v != off: bad.append(k)
        print(f'{k:16s} 复算={v}  官方={off}{flag}')
    print('复算题数', len(R), '；不一致：', bad)
    print('2022JSA-55 各选项积分值', {k: round(v, 4) for k, v in excl['2022JSA-55'].items()})
    print('2023JSA-55', excl['2023JSA-55'])
    print('待识别答案参考值', ref, '；2023SZ-51 另一正根≈', round(other_root, 3))
