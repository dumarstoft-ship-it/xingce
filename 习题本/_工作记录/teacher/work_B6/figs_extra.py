import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from svgkit import *

OUT = os.path.join(os.path.dirname(__file__), "fig")
os.makedirs(OUT, exist_ok=True)
FIG = {}

def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))

def lab(p, s, dx=0, dy=0, size=14, italic=True):
    return text((p[0]+dx, p[1]+dy), s, size=size, italic=italic)

# ---------- T237x1 圆锥形雨量容器 ----------
cx, top, R, H = 175, 48, 75, 200
apex = (cx, top + H)
wy = top + H/2; wr = R/2
body = ""
body += path(f"M {cx-wr} {wy} L {apex[0]} {apex[1]} L {cx+wr} {wy} A {wr} {7} 0 0 1 {cx-wr} {wy} Z", fill="#9e9e9e", stroke=None)
body += ellipse((cx, wy), wr, 7, fill="#bdbdbd", w=1.0)
body += ellipse((cx, top), R, 14)
body += line((cx-R, top), apex) + line((cx+R, top), apex)
# 尺寸
body += line((cx-R, top-4), (cx-R, top-26), w=0.9) + line((cx+R, top-4), (cx+R, top-26), w=0.9)
body += dim((cx-R, top-20), (cx+R, top-20), "", w=0.9) + text((cx, top-32), "300mm", size=12)
body += line((cx-R-4, top), (cx-R-40, top), w=0.9) + line((apex[0]-6, apex[1]), (cx-R-40, apex[1]), w=0.9)
body += dim((cx-R-34, top), (cx-R-34, apex[1]), "", w=0.9) + text((cx-R-39, (top+apex[1])/2), "400mm", size=12, anchor="end")
body += line((cx+wr+4, wy), (cx+R+40, wy), w=0.9, dash=True) + line((apex[0]+6, apex[1]), (cx+R+40, apex[1]), w=0.9)
body += dim((cx+R+34, wy), (cx+R+34, apex[1]), "", w=0.9) + text((cx+R+36, (wy+apex[1])/2), "200mm", size=12, anchor="start")
FIG["T237x1"] = svg(cx+R+90, apex[1]+16, body)

# ---------- T249x1 小区道路（五边形） ----------
s2 = math.sqrt(2)
BC = (60 - 50/s2)*s2
Ap, Bp = (0, 0), (40, 0)
Cp = (40 + BC/s2, -BC/s2)
Dp = (Cp[0] - 50/s2, Cp[1] - 50/s2)
Ep = (0, -60)
sc, ox, oy = 3.0, 34, 24
T = lambda p: (ox + sc*p[0], oy - sc*p[1])
A_, B_, C_, D_, E_ = map(T, (Ap, Bp, Cp, Dp, Ep))
body = poly([A_, B_, C_, D_, E_])
body += right_angle(A_, B_, E_) + right_angle(C_, B_, D_) + right_angle(E_, D_, A_)
body += lab(A_, "A", -10, -8) + lab(B_, "B", 2, -11) + lab(C_, "C", 12, 0) + lab(D_, "D", 2, 13) + lab(E_, "E", -10, 9)
FIG["T249x1"] = svg(C_[0]+30, E_[1]+28, body)

# ---------- T249x2 公园道路 AD ----------
sc, ox, oy = 1.05, 30, 140
T = lambda p: (ox + sc*p[0], oy - sc*p[1])
bc = math.sqrt(200**2 - 100**2)
A_, B_, C_, D_ = T((0, 100)), T((0, 0)), T((bc, 0)), T((bc/2, -bc*math.sqrt(3)/2))
body = line(A_, B_) + line(B_, C_) + line(A_, C_) + line(B_, D_) + line(C_, D_)
body += line(A_, D_, dash=True)
body += right_angle(B_, A_, C_)
body += lab(A_, "A", -10, -6) + lab(B_, "B", -12, 0) + lab(C_, "C", 12, 0) + lab(D_, "D", 0, 14)
body += text((C_[0]-8, 22), "北", size=12, italic=False) + line((C_[0]-8, 50), (C_[0]-8, 30), w=1.0) + arrow_head((C_[0]-8, 30), (C_[0]-8, 50), 6)
FIG["T249x2"] = svg(C_[0]+30, D_[1]+26, body)

# ---------- T249x3 长方形 ABCD 中的 E、F ----------
w, h = 250, 125
A_, B_, C_, D_ = (24, 22), (24+w, 22), (24+w, 22+h), (24, 22+h)
E_ = (B_[0], B_[1] + 2*h/3); F_ = (D_[0] + 2*w/3, D_[1])
body = poly([A_, B_, C_, D_]) + line(A_, E_) + line(A_, F_) + line(E_, F_)
body += lab(A_, "A", -10, -6) + lab(B_, "B", 10, -6) + lab(C_, "C", 10, 8) + lab(D_, "D", -10, 8)
body += lab(E_, "E", 11, 0) + lab(F_, "F", 0, 14)
FIG["T249x3"] = svg(C_[0]+28, C_[1]+26, body)

# ---------- T249x4 三角形公园 ----------
A_, B_, C_ = (140, 20), (24, 220), (300, 220)
E_ = (A_[0] + (B_[0]-A_[0])/3, A_[1] + (B_[1]-A_[1])/3)
F_ = (A_[0] + 2*(B_[0]-A_[0])/3, A_[1] + 2*(B_[1]-A_[1])/3)
D_ = ((A_[0]+C_[0])/2, (A_[1]+C_[1])/2)
O_ = inter(E_, C_, F_, D_)
body = poly([E_, O_, D_], fill="#111", stroke="#111", w=1.0)
body += poly([A_, B_, C_]) + line(E_, C_) + line(F_, D_) + line(F_, C_)
body += lab(A_, "A", 0, -11) + lab(B_, "B", -10, 6) + lab(C_, "C", 10, 6) + lab(D_, "D", 11, -2)
body += lab(E_, "E", -11, -2) + lab(F_, "F", -11, 0) + lab(O_, "O", 2, 13)
FIG["T249x4"] = svg(330, 242, body)

# ---------- T249x5 石像测量 ----------
k = 6.0
A_ = (30, 268); D_ = (30 + 40*k, 268); C_ = (D_[0], 268 - 24*k); B_ = (D_[0], 268 - 40*k)
body = line(A_, D_) + line(D_, B_) + line(A_, B_) + line(A_, C_)
body += right_angle(D_, A_, B_)
def arc_at(v, r, a0, a1):
    p0 = (v[0] + r*math.cos(math.radians(-a0)), v[1] + r*math.sin(math.radians(-a0)))
    p1 = (v[0] + r*math.cos(math.radians(-a1)), v[1] + r*math.sin(math.radians(-a1)))
    return path(f"M {f(p0[0])} {f(p0[1])} A {r} {r} 0 0 0 {f(p1[0])} {f(p1[1])}", w=1.0)
body += arc_at(A_, 92, 0, 45) + arc_at(A_, 56, 0, 31)
body += text((A_[0]+110*math.cos(math.radians(38.5)), A_[1]-110*math.sin(math.radians(38.5))), "45°", size=12)
body += text((A_[0]+72*math.cos(math.radians(14)), A_[1]-72*math.sin(math.radians(14))), "31°", size=12)
body += lab(A_, "A", -10, 4) + lab(D_, "D", 11, 6) + lab(C_, "C", 11, 0) + lab(B_, "B", 11, 0)
FIG["T249x5"] = svg(D_[0]+30, 290, body)

# ---------- T252x1 梯形田地 ----------
C_, B_, D_, A_ = (22, 22), (300, 22), (88, 116), (246, 116)
body = poly([C_, B_, A_, D_]) + line(C_, A_)
body += lab(C_, "C", -8, -8) + lab(B_, "B", 10, -8) + lab(D_, "D", -10, 10) + lab(A_, "A", 8, 12)
FIG["T252x1"] = svg(328, 142, body)

# ---------- T252x2 梯形 CD=2AB=3DF ----------
u = 40
D_, C_ = (20, 170), (20 + 6*u, 170)
A_, B_ = (70, 32), (70 + 3*u, 32)
F_ = (20 + 2*u, 170)
G_ = inter(A_, F_, B_, D_)
body = poly([A_, B_, C_, D_]) + line(A_, F_) + line(B_, D_)
body += lab(A_, "A", -8, -9) + lab(B_, "B", 8, -9) + lab(C_, "C", 10, 8) + lab(D_, "D", -10, 8)
body += lab(F_, "F", 0, 14) + lab(G_, "G", -13, 2)
FIG["T252x2"] = svg(C_[0]+28, 194, body)

# ---------- T252x3 梯形 DC=3AB，中位线 EF ----------
u = 90
D_, C_ = (22, 210), (22 + 3*u, 210)
A_, B_ = (112, 30), (112 + u, 30)
E_ = ((A_[0]+D_[0])/2, (A_[1]+D_[1])/2); F_ = ((B_[0]+C_[0])/2, (B_[1]+C_[1])/2)
G_ = inter(A_, F_, B_, E_); H_ = inter(E_, C_, D_, F_)
body = poly([A_, B_, C_, D_]) + line(E_, F_) + line(A_, F_) + line(B_, E_) + line(E_, C_) + line(D_, F_)
body += lab(A_, "A", -8, -9) + lab(B_, "B", 8, -9) + lab(C_, "C", 10, 8) + lab(D_, "D", -10, 8)
body += lab(E_, "E", -11, 0) + lab(F_, "F", 11, 0) + lab(G_, "G", 0, -12) + lab(H_, "H", 0, 13)
FIG["T252x3"] = svg(C_[0]+28, 234, body)

# ---------- T255x1 小岛森林火灾 ----------
O = (150, 142); r = 100
P = (O[0], O[1] + r)
X1 = (O[0] - r*math.sqrt(3)/2, O[1] + r/2); X2 = (O[0] + r*math.sqrt(3)/2, O[1] + r/2)
body = circle(O, r)
body += path(f"M {f(X1[0])} {f(X1[1])} A {r} {r} 0 0 1 {f(X2[0])} {f(X2[1])}", w=1.6)   # 以起火点为圆心的火线
body += line(P, O, dash=True, w=1.0) + line(P, X1, dash=True, w=1.0)
body += text((O[0]+9, O[1]+52), "r", size=13, italic=True) + text(((P[0]+X1[0])/2+7, (P[1]+X1[1])/2-11), "r", size=13, italic=True)
body += dot(P, 2.6)
body += text((O[0], O[1]-48), "森林", size=13, italic=False)
body += text((O[0]-56, O[1]+2), "火", size=13, italic=False) + text((O[0]+56, O[1]+2), "线", size=13, italic=False)
body += text((P[0], P[1]+16), "起火点", size=12, italic=False)
FIG["T255x1"] = svg(300, P[1]+30, body)

# ---------- T255x2 两个圆形花坛与矩形围栏 ----------
s = 30; s3 = math.sqrt(3)
Wm, Hm = 4 + 2*s3, 6
ox, oy = 20, 20
T = lambda x, y: (ox + s*x, oy + s*(Hm - y))
body = poly([T(0, 0), T(Wm, 0), T(Wm, Hm), T(0, Hm)])
body += circle(T(3, 3), 3*s) + circle(T(Wm-1, 5), 1*s)
FIG["T255x2"] = svg(2*ox + s*Wm, 2*oy + s*Hm, body)

# ---------- T255x3 正三角形广场与三个圆 ----------
k = 5.0
a = 50*k
Bv, Cv = (25, 240), (25 + a, 240); Av = (25 + a/2, 240 - a*math.sqrt(3)/2)
inr = a/(2*math.sqrt(3))
O = (25 + a/2, 240 - inr)
r = inr/(2/math.sqrt(3) + 1)
d = 2*r/math.sqrt(3)
cs = [(O[0] + d*math.sin(t), O[1] + d*math.cos(t)) for t in (0, 2*math.pi/3, -2*math.pi/3)]
body = poly([Av, Bv, Cv])
for c in cs:
    body += circle(c, r)
FIG["T255x3"] = svg(Cv[0]+25, 260, body)

# ---------- T256x1 厂区涉密区域 ----------
sc = 0.8; e = 80.0; yF = 100 + math.sqrt(150**2 - e**2)
ox, oy = 26, 22
T = lambda x, y: (ox + sc*(x + e), oy + sc*(yF - y))
A_, B_, C_, D_ = T(0, 100), T(0, 0), T(240, 0), T(240, 100)
E_, F_ = T(-e, 0), T(-e, yF)
G_ = T(0, 100 - 100*240/(240 + e))
body = poly([A_, D_, G_, F_], fill="#a8a8a8", stroke=None)
body += poly([A_, D_, C_, B_]) + line(B_, E_) + line(E_, F_) + line(F_, A_) + line(D_, E_) + line(F_, G_)
body += lab(A_, "A", 9, -9) + lab(B_, "B", 0, 13) + lab(C_, "C", 0, 13) + lab(D_, "D", 0, -11)
body += lab(E_, "E", 0, 13) + lab(F_, "F", -10, -6) + lab(G_, "G", 11, 11)
FIG["T256x1"] = svg(C_[0]+24, B_[1]+28, body)

# ---------- T256x2 两个相邻正方形 ----------
u = 18; a = 10*u; s_ = 6*u
ox, oy = 24 + s_, 24
D_ = (ox, oy + a); A_ = (ox, oy); B_ = (ox + a, oy); C_ = (ox + a, oy + a)
E_ = (ox - s_, oy + a); F_ = (ox - s_, oy + a - s_); M_ = (ox, oy + a - s_)
defs = hatch_def("h_sq", gap=6, angle=45, color="#555")
body = poly([A_, F_, C_], fill="url(#h_sq)", stroke=None)
body += poly([A_, B_, C_, D_]) + poly([F_, M_, D_, E_]) + line(A_, F_) + line(F_, C_) + line(A_, C_)
body += lab(A_, "A", 0, -11) + lab(B_, "B", 9, -9) + lab(C_, "C", 9, 9) + lab(D_, "D", 0, 14)
body += lab(E_, "E", -9, 9) + lab(F_, "F", -11, 0)
FIG["T256x2"] = svg(C_[0]+26, C_[1]+28, body, defs)

# ---------- T256x3 矩形农场 ----------
sc = 0.32; L = 800.0
ox, oy = 26, 24
T = lambda x, y: (ox + sc*x, oy + sc*(400 - y))
A_, B_, C_, D_ = T(0, 400), T(L, 400), T(L, 0), T(0, 0)
F_, E_ = T(600, 400), T(600, 0)
O_ = T(600, 400*600/L)
body = poly([D_, O_, C_], fill="#8f8f8f", stroke=None)
body += poly([A_, B_, C_, D_]) + line(F_, E_) + line(B_, D_) + line(O_, C_)
body += lab(A_, "A", -9, -8) + lab(B_, "B", 9, -8) + lab(C_, "C", 9, 9) + lab(D_, "D", -9, 9)
body += lab(F_, "F", 0, -11) + lab(E_, "E", 0, 13) + lab(O_, "O", -11, -9)
FIG["T256x3"] = svg(C_[0]+26, C_[1]+28, body)

# ---------- T256x4 人工湖两条环道 ----------
sc = 0.85
O = (160, 150)
Rr, rr = 150*sc, 100*sc
body = circle(O, rr, fill="#ececec", stroke="#333", w=1.6, dash=False).replace('stroke-width="1.6"', 'stroke-width="1.6" stroke-dasharray="1.5 3"')
body += circle(O, Rr, dash=False).replace('stroke-width="1.4"', 'stroke-width="1.8" stroke-dasharray="12 7"')
Bp, Ap = (O[0] + rr, O[1]), (O[0] + Rr, O[1])
body += line(Bp, Ap, w=1.6) + line((Ap[0], Ap[1]-6), (Ap[0], Ap[1]+6), w=1.4)
body += dot(O, 2.4) + text((O[0], O[1]-16), "湖面", size=13, italic=False)
body += text((O[0]+50, O[1]-46), "福道", size=13, italic=False) + text((O[0]+122, O[1]-82), "乐道", size=13, italic=False)
body += lab(Bp, "B", -11, 0) + lab(Ap, "A", 12, 0)
FIG["T256x4"] = svg(330, 300, body)

for k_, v_ in FIG.items():
    with open(os.path.join(OUT, f"{k_}.svg"), "w") as fh:
        fh.write(v_)
print("wrote", sorted(FIG))
