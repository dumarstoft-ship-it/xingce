# -*- coding: utf-8 -*-
from fractions import Fraction as F
import math
# 1) 流水两船往返：精确分段
def river_pos(Lr, vb, w, start_left, t):
    x = F(0) if start_left else F(Lr); d = 1 if start_left else -1; tt = F(0)
    while True:
        sp = vb + w if d > 0 else vb - w   # 下游为正方向
        tgt = Lr if d > 0 else 0
        need = abs(tgt - x) / sp
        if tt + need >= t:
            return x + d * sp * (t - tt)
        tt += need; x = F(tgt); d = -d
def meets(Lr, vb, w, T):
    # 在细网格上找精确交点：分段线性，逐段求解
    res = []
    grid = [F(T) * i / 2000 for i in range(2001)]
    for a, b in zip(grid, grid[1:]):
        fa = river_pos(Lr, vb, w, True, a) - river_pos(Lr, vb, w, False, a)
        fb = river_pos(Lr, vb, w, True, b) - river_pos(Lr, vb, w, False, b)
        if fa == 0: res.append(a)
        elif fa * fb < 0:
            lo, hi = a, b
            for _ in range(80):
                m = (lo + hi) / 2
                fm = river_pos(Lr, vb, w, True, m) - river_pos(Lr, vb, w, False, m)
                if (fm > 0) == (fa > 0): lo = m
                else: hi = m
            res.append(hi)
    out = []
    for t in res:
        if not out or abs(float(t - out[-1])) > 1e-6: out.append(t)
    return [(round(float(t), 4), round(float(river_pos(Lr, vb, w, True, t)), 4)) for t in out]
print("流水两船往返相遇(时h, 距A km):", meets(60, F(25), F(5), 8))

# 2) 同端出发往返两次，最远距离（2022SC1-47 改编候选）
def unfold(d, L):
    p = d % (2 * L)
    return p if p <= L else 2 * L - p
def same_start_max(L, v1, v2, trips):
    T = F(2 * L * trips) / min(v1, v2); best = (0, 0)
    for i in range(1, 40001):
        t = T * i / 40000
        d1 = min(v1 * t, 2 * L * trips); d2 = min(v2 * t, 2 * L * trips)
        dist = abs(unfold(d1, L) - unfold(d2, L))
        if dist > best[0]: best = (dist, t)
    return best
for L, v1, v2, tr in [(30, 100, 80, 2), (36, 90, 60, 2), (40, 100, 60, 2), (30, 90, 60, 2), (60, 100, 75, 2), (24, 60, 40, 2), (45, 90, 60, 1), (30, 60, 45, 2)]:
    b = same_start_max(L, F(v1), F(v2), tr)
    print("同端往返", tr, "次 L=%s v=%s,%s -> 最远 %.4f 于 t=%.4f" % (L, v1, v2, float(b[0]), float(b[1])))

# 3) 勾股两时刻（仿 2022GK-68）：张从丙地正西 X 向东，李从丙地正北 Y 向南；1 小时后距离整数，T2 小时后两人都已过丙地且距离整数
cands = []
for X in range(6, 40):
    for Y in range(4, 40):
        for a in range(2, 16):
            for b in range(1, 16):
                if a == b: continue
                if not (X - a > 0 and Y - b > 0): continue
                d1 = math.hypot(X - a, Y - b)
                if abs(d1 - round(d1)) > 1e-9: continue
                for T2 in [3, 4, 5]:
                    if not (T2 * a > X and T2 * b > Y): continue
                    d2 = math.hypot(T2 * a - X, T2 * b - Y)
                    if abs(d2 - round(d2)) > 1e-9: continue
                    late = (X / a - Y / b) * 60
                    if abs(late) < 1e-9: continue
                    # 速度比为简单比例
                    from fractions import Fraction as Fr
                    r = Fr(b, a)
                    if r.denominator <= 5:
                        cands.append((X, Y, a, b, str(r), round(d1), T2, round(d2), round(late, 1)))
for c in cands[:40]:
    print("勾股候选 西距%d 北距%d 张速%d 李速%d 李/张=%s 1h距%d T2=%d T2距%d 张比李晚(分)=%s" % c)
