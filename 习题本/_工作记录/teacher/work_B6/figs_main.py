import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from svgkit import *

OUT = os.path.join(os.path.dirname(__file__), "fig")
os.makedirs(OUT, exist_ok=True)
FIG = {}

# ---------------- T229 三视图 ----------------
def view_triangle(x0, y0, u, title):
    # x0,y0: 底线左端；u: 每厘米像素
    b = ""
    L, M1, M2, R = x0, x0 + 2*u, x0 + 4*u, x0 + 6*u
    apex = (x0 + 3*u, y0 - 2*u)
    b += line((L, y0), (M1, y0)) + line((M1, y0), (M2, y0), dash=True) + line((M2, y0), (R, y0))
    b += line((M1, y0), apex) + line(apex, (M2, y0))
    # 底部尺寸
    yd = y0 + 14
    for xx in (L, M1, M2, R):
        b += line((xx, y0 + 3), (xx, yd + 5), w=0.9)
    for a_, c_ in ((L, M1), (M1, M2), (M2, R)):
        b += dim((a_, yd), (c_, yd), "", w=0.9)
        b += text(((a_ + c_) / 2, yd + 13), "2cm", size=12)
    # 高度尺寸
    xh = M2 + 0.6*u
    b += line(apex, (xh + 6, apex[1]), w=0.9)
    b += dim((xh, apex[1]), (xh, y0), "", w=0.9)
    b += text((xh + 20, (apex[1] + y0) / 2), "2cm", size=12)
    b += text((x0 + 3*u, y0 + 52), title, size=14)
    return b

u = 22
y0 = 112
body = view_triangle(14, y0, u, "主视图") + view_triangle(14 + 6*u + 40, y0, u, "左视图")
cx, cy = 14 + 12*u + 80 + 3*u, 76
body += circle((cx, cy), 3*u) + circle((cx, cy), 1*u) + dot((cx, cy), 2)
body += text((cx, y0 + 52), "俯视图", size=14)
FIG["T229"] = svg(cx + 3*u + 16, y0 + 68, body)

# ---------------- T230 沙漏 ----------------
c_top, c_bot, mid = (110, 32), (110, 208), (110, 120)
rx, ry = 62, 13
body = ""
# 下面圆锥内的细沙（倒置前）
sand = path(f"M {c_bot[0]-rx} {c_bot[1]} L {mid[0]} {mid[1]} L {c_bot[0]+rx} {c_bot[1]} "
            f"A {rx} {ry} 0 0 1 {c_bot[0]-rx} {c_bot[1]} Z", fill="#e3d6b0", stroke=None)
body += sand
body += ellipse(c_top, rx, ry)
body += line((c_top[0]-rx, c_top[1]), mid) + line((c_top[0]+rx, c_top[1]), mid)
body += line(mid, (c_bot[0]-rx, c_bot[1])) + line(mid, (c_bot[0]+rx, c_bot[1]))
body += half_ellipse(c_bot, rx, ry, upper=True, dash=True) + half_ellipse(c_bot, rx, ry, upper=False)
body += text((205, 165), "细沙", size=13) + line((188, 166), (150, 178), w=0.8)
FIG["T230"] = svg(240, 232, body)

# ---------------- T233 遮阳伞 ----------------
def proj(p, origin, k=0.5, th=math.radians(28)):
    x, y, z = p
    return (origin[0] + x + k*y*math.cos(th), origin[1] - z - k*y*math.sin(th))

def umbrella(origin, angle_deg, L, primes, cap, cap_y, d_off):
    pr = "′" if primes else ""
    h = L*math.cos(math.radians(angle_deg)); d = L*math.sin(math.radians(angle_deg))
    s = d*math.sqrt(2)
    A = (-s/2, -s/2, 0); B = (s/2, -s/2, 0); C = (s/2, s/2, 0); D = (-s/2, s/2, 0)
    Q = (0, 0, 0); P = (0, 0, h); H = (0, 0, h - 1.36*L)
    pA, pB, pC, pD, pQ, pP, pH = (proj(t, origin) for t in (A, B, C, D, Q, P, H))
    b = ""
    b += line(pA, pB) + line(pB, pC)
    b += line(pC, pD, dash=True) + line(pD, pA, dash=True)
    b += line(pP, pA) + line(pP, pB) + line(pP, pC) + line(pP, pD, dash=True)
    b += line(pP, pQ, dash=True) + line(pA, pC, dash=True)
    # 伞柄：Q 以下可见部分
    b += line(pQ, pH, w=1.8)
    b += dot(pP, 2) + dot(pQ, 1.8)
    b += text((pP[0], pP[1]-12), "P", italic=True)
    b += text((pA[0]-10, pA[1]+10), "A"+pr, italic=True)
    b += text((pB[0]+6, pB[1]+13), "B"+pr, italic=True)
    b += text((pC[0]+13, pC[1]), "C"+pr, italic=True)
    b += text((pD[0]+d_off[0], pD[1]+d_off[1]), "D"+pr, italic=True)
    b += line((pQ[0]-2, pQ[1]+3), (pQ[0]-15, pQ[1]+21), w=0.8)
    b += text((pQ[0]-21, pQ[1]+29), "Q"+pr, italic=True)
    b += text((origin[0], cap_y), cap, size=14)
    return b

L = 118
body = umbrella((86, 128), 30, L, False, "图1", 262, (-12, -6)) + umbrella((336, 128), 60, L, True, "图2", 262, (7, 11))
FIG["T233"] = svg(470, 280, body)

# ---------------- T234 墙角谷堆 ----------------
O = (150, 150)
e1 = (1.0, 0.0)            # 右侧墙脚方向
e2 = (-0.62, 0.50)         # 前左墙脚方向（透视缩短）
r = 112; Hh = 78
arc = [(O[0] + r*(math.cos(t)*e1[0] + math.sin(t)*e2[0]), O[1] + r*(math.cos(t)*e1[1] + math.sin(t)*e2[1]))
       for t in [i*math.pi/2/60 for i in range(61)]]
apex = (O[0], O[1] - Hh)
def hull(points):
    pts = sorted(set(points))
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
body = ""
body += poly(hull(arc + [apex]), fill="#c9c9c9", stroke=None)
# 墙角三条棱：谷堆外的部分实线，被谷堆挡住的部分虚线
body += line((O[0], 18), apex) + line(apex, O, dash=True)
R1 = arc[0]; R2 = arc[-1]
far1 = (O[0] + 170*e1[0], O[1] + 170*e1[1]); far2 = (O[0] + 190*e2[0]/math.hypot(*e2)*0.95, O[1] + 190*e2[1]/math.hypot(*e2)*0.95)
body += line(O, R1, dash=True) + line(R1, far1)
body += line(O, R2, dash=True) + line(R2, far2)
body += poly(arc, close=False)
body += line(apex, R1) + line(apex, R2)
# 两面墙的示意（淡色）
FIG["T234"] = svg(330, 245, body)

# ---------------- T236 帐篷屋顶 ----------------
def P3(x, y, z, s=62, k=0.6, th=math.radians(25), o=(28, 150)):
    return (o[0] + s*x + s*k*y*math.cos(th), o[1] - s*z - s*k*y*math.sin(th))
P1, P2, Pb3, P4 = P3(0,0,0), P3(4,0,0), P3(4,3,0), P3(0,3,0)
R1, R2 = P3(1,1.5,1), P3(3,1.5,1)
M, Mt = P3(2,1.5,0), P3(2,1.5,1)
body = ""
body += line(P1, P2) + line(P2, Pb3) + line(R1, R2) + line(P1, R1) + line(P2, R2) + line(Pb3, R2)
body += line(Pb3, P4, dash=True) + line(P4, P1, dash=True) + line(P4, R1, dash=True)
body += line(Mt, M, dash=True) + dot(M, 2.6)
body += text(((P1[0]+P2[0])/2, P1[1]+16), "4")
body += text(((P2[0]+Pb3[0])/2+12, (P2[1]+Pb3[1])/2+6), "3")
body += text(((R1[0]+R2[0])/2, R1[1]-13), "2")
body += text((Mt[0]+11, (Mt[1]+M[1])/2-6), "1")
FIG["T236"] = svg(Pb3[0]+30, 176, body)

# ---------------- T241 圆锥 ----------------
cx, cy, rx_, ry_ = 120, 150, 74, 17
hgt = rx_*math.sqrt(3)
apex = (cx, cy - hgt)
body = ""
body += line(apex, (cx-rx_, cy)) + line(apex, (cx+rx_, cy))
body += half_ellipse((cx, cy), rx_, ry_, upper=True, dash=True) + half_ellipse((cx, cy), rx_, ry_, upper=False)
body += line(apex, (cx, cy), dash=True, w=1.0) + dot((cx, cy), 1.8)
body += dot((cx-rx_, cy), 2.4) + dot((cx+rx_, cy), 2.4)
body += text((cx-rx_-12, cy+4), "A", italic=True) + text((cx+rx_+12, cy+4), "B", italic=True)
FIG["T241"] = svg(245, 182, body)

# ---------------- T253 钢珠测孔径 ----------------
u = 26
C0 = (150, 112); Rb = 3*u
ys = C0[1] + 2*u                    # 工件顶端面
hx = math.sqrt(5)*u                 # 孔半径（按比例作图，不标数值）
body = ""
defs = hatch_def("h253", gap=7, angle=45, color="#777")
body += poly([(30, ys), (C0[0]-hx, ys), (C0[0]-hx, ys+62), (30, ys+62)], fill="url(#h253)", stroke=None)
body += poly([(C0[0]+hx, ys), (270, ys), (270, ys+62), (C0[0]+hx, ys+62)], fill="url(#h253)", stroke=None)
body += line((30, ys), (C0[0]-hx, ys)) + line((C0[0]+hx, ys), (270, ys))
body += line((C0[0]-hx, ys), (C0[0]-hx, ys+62)) + line((C0[0]+hx, ys), (C0[0]+hx, ys+62))
body += circle(C0, Rb, fill="#fff")
body += circle(C0, Rb)
top = (C0[0], C0[1]-Rb)
body += line(top, (300, top[1]), dash=True, w=0.9) + line((270, ys), (300, ys), dash=True, w=0.9)
body += dim((292, top[1]), (292, ys), "", w=1.0)
body += text((306, (top[1]+ys)/2), "X", italic=True)
body += text((C0[0], ys+80), "工件剖面示意", size=12, color="#555")
FIG["T253"] = svg(325, ys+96, body, defs)

# ---------------- T254 正方形绿地 ----------------
s0, a = 22, 200
TL, TR, BR, BL = (s0, s0), (s0+a, s0), (s0+a, s0+a), (s0, s0+a)
k = a/math.sqrt(2)
P1_ = (BL[0]+k, BL[1]-k)      # 对角线与以左下角为圆心的弧的交点
P2_ = (TR[0]-k, TR[1]+k)      # 对角线与以右上角为圆心的弧的交点
defs = hatch_def("h254", gap=7, angle=45, color="#555")
body = ""
body += path(f"M {f(TL[0])} {f(TL[1])} L {f(TR[0])} {f(TR[1])} L {f(P1_[0])} {f(P1_[1])} "
             f"A {a} {a} 0 0 0 {f(TL[0])} {f(TL[1])} Z", fill="url(#h254)", stroke=None)
body += path(f"M {f(BR[0])} {f(BR[1])} L {f(BL[0])} {f(BL[1])} L {f(P2_[0])} {f(P2_[1])} "
             f"A {a} {a} 0 0 0 {f(BR[0])} {f(BR[1])} Z", fill="url(#h254)", stroke=None)
body += poly([TL, TR, BR, BL])
body += path(f"M {f(TL[0])} {f(TL[1])} A {a} {a} 0 0 1 {f(BR[0])} {f(BR[1])}")
body += path(f"M {f(TL[0])} {f(TL[1])} A {a} {a} 0 0 0 {f(BR[0])} {f(BR[1])}")
body += line(BL, TR)
FIG["T254"] = svg(2*s0+a, 2*s0+a, body, defs)

# ---------------- T255 航天器与北纬45° ----------------
O = (160, 196); R = 92
S = (O[0], O[1] - math.sqrt(2)*R)
B = (O[0] - R*math.sin(math.radians(45)), O[1] - R*math.cos(math.radians(45)))
C = (O[0] + R*math.sin(math.radians(45)), O[1] - R*math.cos(math.radians(45)))
N = (O[0], O[1] - R)
body = ""
body += circle(O, R)
body += ellipse(((B[0]+C[0])/2, B[1]), (C[0]-B[0])/2, 13, dash=True, w=1.1)
body += line(S, B) + line(S, C)
body += line(S, O, dash=True, w=1.0)
body += dot(S, 2.6) + dot(N, 2.6) + dot(O, 2.2) + dot(B, 2.2) + dot(C, 2.2)
body += text((S[0], S[1]-13), "S", italic=True)
body += line((N[0]+3, N[1]-3), (N[0]+36, N[1]-22), w=0.8) + text((N[0]+60, N[1]-28), "北极点", size=12)
body += text((B[0]-12, B[1]-4), "B", italic=True) + text((C[0]+12, C[1]-4), "C", italic=True)
body += text((O[0]+12, O[1]+6), "O", italic=True)
body += text((O[0]+62, B[1]+27), "北纬45°线", size=12, color="#444")
FIG["T255"] = svg(320, O[1]+R+14, body)

# ---------------- T256 草皮空地 ----------------
sc = 1.45; ox, oy = 52, 268
def Q(x, y): return (ox + sc*x, oy - sc*y)
t_, a_ = 20, 60                           # 作图取 AG=DE=CF=20、AD=DC=60（满足 DF=80）
E, D, C, F_ = Q(-t_, 0), Q(0, 0), Q(a_, 0), Q(a_+t_, 0)
A, G, B = Q(0, a_), Q(0, a_-t_), Q(a_, 160)
body = ""
body += poly([E, G, C], fill="#bdbdbd", stroke=None) + poly([B, C, F_], fill="#bdbdbd", stroke=None)
body += line(E, F_) + line(D, A) + line(A, C) + line(E, G) + line(G, C) + line(C, B) + line(B, F_)
for p_, lab, off in ((E, "E", (0, 14)), (D, "D", (0, 14)), (C, "C", (0, 14)), (F_, "F", (0, 14)),
                     (A, "A", (-11, -4)), (G, "G", (-11, 0)), (B, "B", (-10, -6))):
    body += text((p_[0]+off[0], p_[1]+off[1]), lab, italic=True)
FIG["T256"] = svg(F_[0]+30, oy+28, body)

# ---------------- T258 通信基站 ----------------
u = 128
A, B = (30, 178), (30 + 2*u, 178)
D = (B[0], B[1] - u)
AD = math.hypot(D[0]-A[0], D[1]-A[1])
uDA = ((A[0]-D[0])/AD, (A[1]-D[1])/AD)
E = (D[0] + u*uDA[0], D[1] + u*uDA[1])
AE = math.hypot(E[0]-A[0], E[1]-A[1])
C = (A[0] + AE, A[1])
body = ""
body += line(A, B) + line(B, D) + line(A, D)
body += path(f"M {f(E[0])} {f(E[1])} A {f(AE)} {f(AE)} 0 0 1 {f(C[0])} {f(C[1])}", w=1.2)   # 以 A 为圆心
body += path(f"M {f(E[0])} {f(E[1])} A {u} {u} 0 0 0 {f(B[0])} {f(B[1])}", w=1.2)            # 以 D 为圆心
body += right_angle(B, A, D)
for p_ in (A, B, C, D, E): body += dot(p_, 2.2)
body += text((A[0]-11, A[1]), "A", italic=True) + text((B[0]+11, B[1]+4), "B", italic=True)
body += text((C[0], C[1]+13), "C", italic=True) + text((D[0]+4, D[1]-12), "D", italic=True)
body += text((E[0]-6, E[1]-13), "E", italic=True)
body += dim((A[0], B[1]+28), (B[0], B[1]+28), "", w=0.9)
body += text(((A[0]+B[0])/2, B[1]+40), "2km", size=12)
body += dim((B[0]+26, D[1]), (B[0]+26, B[1]), "", w=0.9)
body += text((B[0]+46, (D[1]+B[1])/2), "1km", size=12)
FIG["T258"] = svg(B[0]+68, B[1]+54, body)

# ---------------- T265 四块飞镖板 ----------------
body = ""
GRAY = "#a9a9a9"
cxs = [60, 170, 280, 390]; cyc = 72
# A 圆 + 内接正三角形（阴影三角形）
r = 42; c = (cxs[0], cyc)
tri = [(c[0] + r*math.cos(math.radians(-90 + 120*i)), c[1] + r*math.sin(math.radians(-90 + 120*i))) for i in range(3)]
body += circle(c, r) + poly(tri, fill=GRAY)
# B 正三角形 + 内切圆（阴影圆）
ri = 25; c = (cxs[1], cyc + 8)
Rt = 2*ri
tri = [(c[0] + Rt*math.cos(math.radians(-90 + 120*i)), c[1] + Rt*math.sin(math.radians(-90 + 120*i))) for i in range(3)]
body += poly(tri) + circle(c, ri, fill=GRAY)
# C 圆 + 内接正方形（阴影正方形）
r = 42; c = (cxs[2], cyc)
h_ = r/math.sqrt(2)
body += circle(c, r) + poly([(c[0]-h_, c[1]-h_), (c[0]+h_, c[1]-h_), (c[0]+h_, c[1]+h_), (c[0]-h_, c[1]+h_)], fill=GRAY)
# D 正方形 + 内切圆（阴影圆）
r = 38; c = (cxs[3], cyc)
body += poly([(c[0]-r, c[1]-r), (c[0]+r, c[1]-r), (c[0]+r, c[1]+r), (c[0]-r, c[1]+r)]) + circle(c, r, fill=GRAY)
for x_, lab in zip(cxs, "ABCD"):
    body += text((x_, 140), lab, size=15, weight="bold")
FIG["T265"] = svg(450, 156, body)

for k_, v_ in FIG.items():
    with open(os.path.join(OUT, f"{k_}.svg"), "w") as fh:
        fh.write(v_)
print("wrote", sorted(FIG))
