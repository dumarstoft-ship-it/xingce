# -*- coding: utf-8 -*-
"""M04 考法地图：改编 idea 中给出的数据与预期答案的独立验算（供出题人参考，出题时仍需各自写 verify 脚本）。"""
from fractions import Fraction as F
import math, itertools

def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0): lo = m
        else: hi = m
    return (lo + hi) / 2

# ---------------- 往返运动工具（精确） ----------------
def unfold_pos(d, L):
    """展开距离 d -> (位置, 方向)；方向 0 表示恰在端点"""
    p = d % (2 * L)
    if p == 0: return F(0), 0
    if p < L: return p, 1
    if p == L: return L, 0
    return 2 * L - p, -1

def line_events(v1, v2, L, T, d1_0=F(0), d2_0=F(0)):
    """两人在 [0,L] 往返，初始展开距离 d1_0、d2_0；返回 (t, x, kind) 列表（kind=迎面/追上）"""
    # 相同位置：d1 ≡ d2 (mod 2L) 同向；d1 ≡ -d2 (mod 2L) 反向
    ev = []
    k = 0
    res = set()
    for k in range(-50, 400):
        # 同向：(d1_0+v1 t) - (d2_0+v2 t) = 2Lk
        if v1 != v2:
            t = (2 * L * k - d1_0 + d2_0) / (v1 - v2)
            if 0 < t <= T: res.add((t, "same"))
        # 反向：(d1_0+v1 t) + (d2_0+v2 t) = 2Lk
        t = (2 * L * k - d1_0 - d2_0) / (v1 + v2)
        if 0 < t <= T: res.add((t, "opp"))
    out = []
    for t, kind in sorted(res):
        x1, _ = unfold_pos(d1_0 + v1 * t, L)
        x2, _ = unfold_pos(d2_0 + v2 * t, L)
        assert x1 == x2
        # 端点处同时到达：看到达前方向
        eps = F(1, 10**9)
        _, a = unfold_pos(d1_0 + v1 * (t - eps), L)
        _, b = unfold_pos(d2_0 + v2 * (t - eps), L)
        kk = "追上" if a == b else "迎面"
        out.append((t, x1, kk))
    # 去重（端点处 same/opp 同时成立）
    ded = []
    for e in out:
        if not ded or ded[-1][0] != e[0]: ded.append(e)
    return ded

R = {}
# ======================= Day 3 =======================
# G1-V1 已知全程反求快百分之几
v = bisect(lambda v: v + 3 * (v + 20) - 300, 1, 300); jia = 300 / 4
R["D3-G1-V1 甲比乙快%"] = (jia - v) / v * 100
# G1-V2 环湖两路线
x = bisect(lambda x: 3 * (x + 0.4) - 2.5 * x - 3, 0.1, 100); R["D3-G1-V2 小环km"] = 2.5 * x
# G1-V3 停留后提速：原计划160min，1/4路程后停20min
plan_rest = 160 * 3 / 4; actual = plan_rest - 20; R["D3-G1-V3 提速%"] = (plan_rest / actual - 1) * 100
# G1-V4 深中通道：旧路程=3×新，新速度=4/3旧，节省66min，求新用时
told = bisect(lambda T: T - T * (1 / 3) / (4 / 3) - 66, 1, 1000); R["D3-G1-V4 新用时min"] = told * (1 / 3) / (4 / 3)
# G2-V1 往返平均速度反推
R["D3-G2-V1 返程速度"] = bisect(lambda v: 2 * 60 * v / (60 + v) - 48, 1, 59)
# G2-V2 三段（骑12、步4 等距；划艇6）2.5h
outs = set()
for a in [0.5, 1, 2, 3]:  # 骑行段与步行段路程 a
    t_rest = 2.5 - a / 12 - a / 4
    if t_rest > 0: outs.add(round(2 * a + 6 * t_rest, 9))
R["D3-G2-V2 全程km(与分段无关)"] = outs
# G2-V3 等时 vs 等距
R["D3-G2-V3 距离km"] = bisect(lambda S: (S / 2 / 6 + S / 2 / 3) - S / 4.5 - 0.25, 0.1, 100)
# G2-V4 区间测速
R["D3-G2-V4 后12km最高均速"] = 12 / ((20 / 100) - 4 / 60)
# G3-V1 120m 折返相遇距终点30 -> 甲到终点时乙差x
x = bisect(lambda x: x * (120 / (120 - x)) / (120 / (120 - x) + 1) - 30, 1, 119); R["D3-G3-V1 x米"] = x
# G3-V2 降速1/6迟到12；先骑6km再降速迟到8
T0 = bisect(lambda T: T * 6 / 5 - T - 12, 1, 1000)  # 原用时(min)
seg = 8 / (6 / 5 - 1); first = T0 - seg; speed = 6 / (first / 60); R["D3-G3-V2 全程km"] = speed * T0 / 60
# G3-V3 相遇后4h、9h
t = math.sqrt(4 * 9); R["D3-G3-V3 甲速"] = 300 / (t + 4)
# G3-V4 三车链式比例
R["D3-G3-V4 AB"] = bisect(lambda S: (S - 20) ** 2 - S * (S - 36), 37, 1000)
# G3-V5 高铁时刻表：G 8:00 发，D 8:10 发，8:40 相遇，G 9:00 到
g_before, d_before, g_after = 40, 30, 20
ratio = d_before / g_after  # vG/vD
R["D3-G3-V5 D到达(分钟,自8:40)"] = g_before * ratio
# G4-V1 追上点反求出发时刻
R["D3-G4-V1 小李晚出发min"] = (135 / 60 - 135 / 90) * 60
# G4-V2 第二次相距300
R["D3-G4-V2 甲走m"] = 70 * (1500 + 300) / 120
# G4-V3 休息后提速二次追及
v = bisect(lambda v: 2 * (v + 1) - 8 / 3 * v, 0.1, 100)
gap = 3 * v - 2 * (v + 1); R["D3-G4-V3 乙速/再追上分钟"] = (v, gap / ((v + 2) - v) * 60)
# G4-V4 相遇点偏离中点
R["D3-G4-V4 全长"] = bisect(lambda S: (S / 2 + 2) / (S / 2 - 2) - 1.4, 4.01, 1000)
# G5-V1 同向超车窗口
R["D3-G5-V1 秒"] = 400 / ((300 - 180) / 3.6)
# G5-V2 桥1200/50s 隧道900/40s 完全在隧道内
v = (1200 - 900) / (50 - 40); L = v * 50 - 1200; R["D3-G5-V2 (车长,完全在内s)"] = (L, (900 - L) / v)
# G5-V3 迎面10s 同向12s 人1m/s
v = bisect(lambda v: 10 * (v + 1) - 12 * (v - 1), 1.01, 1000); R["D3-G5-V3 车长"] = 10 * (v + 1)
# G6-V1 直径两端反向，第3次相遇甲圈数
Lp = 30; v1, v2 = Lp / 10, Lp / 15; t3 = (Lp / 2 + 2 * Lp) / (v1 + v2); R["D3-G6-V1 甲圈数"] = v1 * t3 / Lp
# G6-V2 甲在乙前方100m，1.2倍，第二次追上
R["D3-G6-V2 乙米"] = (300 + 400) / 0.2
# G6-V3 变速后速度倍数
Lc = 3 * (3 + 1); t2 = (Lc * 2 / 3) / 3; R["D3-G6-V3 倍数"] = (Lc / 3 / t2) / 1
# G6-V4 不同点反向第5次
R["D3-G6-V4 甲米"] = 6 * (100 + 4 * 400) / 10
# G6-V5 同向30min反向6min 环3km
d, s = 3 / 30 * 60, 3 / 6 * 60; R["D3-G6-V5 甲km/h"] = (d + s) / 2
# G7-V1 梯形 v-t
R["D3-G7-V1 最高速km/h"] = 3.6 / ((2 + 1) / 60)
# G7-V2 中间时刻速度
a = (160 / 10 - 100 / 10) / 10; R["D3-G7-V2 20秒末"] = 100 / 10 + a * 15
# G7-V3 匀加速追匀速最远
R["D3-G7-V3 最远m"] = max(10 * t - 0.5 * t * t for t in [i / 100 for i in range(0, 2001)])
# G7-V4 最短运行时间
ta = 20 / 1; sa = 0.5 * 1 * ta ** 2; R["D3-G7-V4 秒"] = 2 * ta + (1200 - 2 * sa) / 20

# ======================= Day 17 =======================
R["D17-G1-V1 乙速m/min"] = bisect(lambda v: (6000 / v - 2000 / v) - 50, 1, 1000)
# G1-V2 取物返回+耗时5min+9km/h
yi_at = 6 * 45 / 60; R["D17-G1-V2 追上处km"] = 9 * (yi_at / (9 - 6))
R["D17-G1-V3 至少整小时"] = math.floor(1000 / 60 - 1000 / 75) + 1
R["D17-G1-V4 剩余均速"] = 100 / (2.5 - 1 - 20 / 40)
v = bisect(lambda v: 70 * v - (40 * v + 600), 0.1, 1000); R["D17-G2-V1 上山路程"] = 140 * v
# G2-V2 去程50min返程30min
for a_ in range(1, 30):
    for b_ in range(1, 30):
        if abs(a_ / 12 + b_ / 6 - 50 / 60) < 1e-9 and abs(a_ / 12 + b_ / 18 - 30 / 60) < 1e-9:
            R["D17-G2-V2 家校km"] = a_ + b_
# G2-V3 速度比反求路程比
x_ = 1.0; y_ = bisect(lambda y: 1.25 * x_ / (0.8 * y) - 0.5, 0.01, 100)
U_over_D = bisect(lambda r: (r / x_ + 1 / y_) - (r / (1.25 * x_) + 1 / (0.8 * y_)), 0.001, 100)
R["D17-G2-V3 上:下路程"] = U_over_D
S = bisect(lambda S: (S - S / 1.5) / (3 + 1) * 3 - 600, 1, 100000); R["D17-G2-V4 山路"] = S
# G3 接送
R["D17-G3-V1 车/步"] = 32 / 8
R["D17-G3-V2 步行min"] = 60 - 10
def two_batch(S, c, w):
    d = bisect(lambda d: d + 2 * w * d / (c + w) - S, 0.001, S)
    x = S - d
    # 独立模拟验证同时到达
    t1 = d / c + x / w
    # 第二批：步行到被接点
    tback = (d - w * d / c) / (c + w)
    pick_t = d / c + tback; pick_x = w * pick_t
    t2 = pick_t + (S - pick_x) / c
    return d, x, t1 * 60, t2 * 60
R["D17-G3-V3 (乘车,步行,批1min,批2min)"] = two_batch(22, 40, 5)
a_ = bisect(lambda a: (a / 12 + (18 - a) / 4) - (a / 6 + (18 - a) / 12), 0.01, 17.99)
R["D17-G3-V4 (甲骑km,用时h)"] = (a_, a_ / 12 + (18 - a_) / 4)
# G4 流水
R["D17-G4-V1 水速"] = 2 / ((20 + 20) / 60)
R["D17-G4-V2 下移km"] = (15 + 5) * 2 - (15 + 3) * 2
up, down = F(1, 5), F(1, 3); boat, water = (up + down) / 2, (down - up) / 2
R["D17-G4-V3 往返h"] = 1 / (boat + 2 * water) + 1 / (boat - 2 * water)
for w in [1, 2, 3, 4]:
    t = 90 / 25; jia = (20 + w) * t; buoy = w * t
    assert jia < 90
    R.setdefault("D17-G4-V4 甲乙距", set()).add(round(jia - buoy, 9))
# G5 发车
R["D17-G5-V1 间隔"] = 2 * 12 * 4 / (12 + 4)
R["D17-G5-V2 被超间隔"] = bisect(lambda t: 2 * 6 * t / (6 + t) - 8, 6.01, 1000)
R["D17-G5-V3 往返min"] = 600 / (150 - 90) + 600 / (150 + 90)
cnt = sum(1 for dep in range(-200, 200, 10) if -45 < dep < 45)  # 乙站发车时刻(以本车发车为0)，途中相遇条件
R["D17-G5-V4 相遇车数"] = cnt
# G6 环形
R["D17-G6-V1 A追B间隔"] = 1 / (1 / 30 - 1 / 45)
Lk = bisect(lambda L: L / 10 - L / 12 - 4, 1, 100000); R["D17-G6-V2 乙第2次追甲(秒)"] = 2 * Lk / 2
R["D17-G6-V3 乙再跑min"] = 4 * 4 / 5
# 环线地铁：同步发车，统计 (0,80) 内相遇
meet = 0
for j in range(16):
    for k in range(-5, 10):
        t = F(40) * (k - F(j, 16))
        if 0 < t < 80: meet += 1
R["D17-G6-V4 相遇列数(同步发车,不计起止)"] = meet
meet2 = 0
for j in range(16):
    for k in range(-5, 10):
        t = F(40) * (k - F(2 * j + 1, 32))
        if 0 < t < 80: meet2 += 1
R["D17-G6-V4' 错开2.5min时"] = meet2
# G7 往返多次
ev = line_events(F(2), F(3), F(100), F(1000), F(0), F(100))  # 两端出发：乙从B出发朝A=展开距离100
R["D17-G7-V1 3a-b 检验"] = [(str(t), str(x), k) for t, x, k in ev[:3]]
# 到达中点次数
def arrivals(v, lo, hi, x0, dir0, target, n):
    L = hi - lo
    d0 = (x0 - lo) if dir0 > 0 else 2 * L - (x0 - lo)
    res = []; t = F(0); step = F(1, 1)
    # 枚举展开距离中 target 出现的位置
    k = 0
    cand = []
    for m in range(0, 200):
        for base in [target - lo, 2 * L - (target - lo)]:
            dd = base + 2 * L * m
            if dd > d0: cand.append(dd)
    cand = sorted(set(cand))
    return (cand[n - 1] - d0) / v
r = arrivals(F(1), 0, 2, 0, 1, 1, 3) / arrivals(F(1), 1, 2, 2, -1, 1, 4)
R["D17-G7-V2 张/王"] = r
ev = line_events(F(5), F(3), F(300), F(2000))
R["D17-G7-V3 同端第3次迎面"] = [(str(t), str(x), k) for t, x, k in ev if k == "迎面"][:3]
ev = line_events(F(7), F(3), F(200), F(500))
R["D17-G7-V4 7:3 200m 事件"] = [(str(t), str(x), k) for t, x, k in ev[:4]]
# V5 两端出发第3次迎面 4h，AB=100，甲快5
v = bisect(lambda v: (2 * v + 5) * 4 - 500, 1, 1000)
ev = line_events(F(v + 5).limit_denominator(1000), F(v).limit_denominator(1000), F(100), F(5), F(0), F(100))
R["D17-G7-V5 (乙速, 事件)"] = (v, [(float(t), float(x), k) for t, x, k in ev[:4]])
# V6 机器人等效穿过：事件驱动模拟
def robots(pos, dirs, L, speed=F(1)):
    pos = [F(p) for p in pos]; dirs = list(dirs); alive = [True] * len(pos); t = F(0); stops = []
    while any(alive):
        best = None
        idx = [i for i in range(len(pos)) if alive[i]]
        idx.sort(key=lambda i: pos[i])
        for i in idx:  # 到端点
            dt = (L - pos[i]) / speed if dirs[i] > 0 else pos[i] / speed
            if best is None or dt < best[0]: best = (dt, "end", i)
        for a, b in zip(idx, idx[1:]):
            if dirs[a] > 0 and dirs[b] < 0:
                dt = (pos[b] - pos[a]) / (2 * speed)
                if best is None or dt < best[0]: best = (dt, "hit", a, b)
        dt = best[0]; t += dt
        for i in idx: pos[i] += dirs[i] * speed * dt
        for i in idx:
            if alive[i] and (pos[i] <= 0 or pos[i] >= L):
                alive[i] = False; stops.append((t, i, 0 if pos[i] <= 0 else L))
        for a, b in zip(idx, idx[1:]):
            if alive[a] and alive[b] and pos[a] == pos[b] and dirs[a] > 0 and dirs[b] < 0:
                dirs[a], dirs[b] = -1, 1
    return stops
st = robots([10, 20, 30, 40, 50], [1, -1, 1, -1, 1], F(60))
R["D17-G7-V6 最后停止秒"] = max(s[0] for s in st)

# ======================= Day 31 =======================
v = F(4, 120)  # AB=2,BC=3: 2/v+3/(1.5v)=120
assert 2 / v + 3 / (F(3, 2) * v) == 120
ab_time = 140 - 3 / (F(3, 2) * v); R["D31-G1-V1 降速%"] = float((1 - (2 / ab_time) / v) * 100)
outs = set()
for t in [1, 2, 3]:
    s = (75 * (5 * t + 4) - 300) / 2; outs.add((round(s / (3 * t), 6), round(s / 4, 6), round(300 / (2 * t), 6)))
R["D31-G1-V2 (第二天,第三天,第一天) 随t"] = outs
x = bisect(lambda x: (15 - x) / 6 + x / 3 - 4, 0, 15); R["D31-G1-V3 河道"] = x
R["D31-G1-V4 最远km"] = 2 * 60 * 40 / 100 * (45 / 60) / 2
R["D31-G2-V1 快车km/h"] = ((500 / 10 + 500 / 50) / 2) * 3.6
R["D31-G2-V2 车长"] = (20 * 60 - 20 * 40) / 2
# 流水往返第二次相遇（分段精确模拟）
def river_two(Lr, vb, w, T=10):
    # 甲从A(上游,0)下行，乙从B(Lr)上行；到岸立即返回
    import fractions
    def pos(start, dir0, t):
        # dir0=+1 下行
        x, d, tt = F(start), dir0, F(0)
        while True:
            sp = vb + w if d > 0 else vb - w
            tgt = Lr if d > 0 else 0
            need = abs(tgt - x) / sp
            if tt + need >= t:
                return x + d * sp * (t - tt)
            tt += need; x = F(tgt); d = -d
    # 扫描相遇（二分）：细分时间网格找符号变化
    meets = []; N = 4000; prev = None
    for i in range(1, N):
        t = F(T) * i / N
        diff = pos(0, 1, t) - pos(Lr, -1, t)
        s = (diff > 0) - (diff < 0)
        if prev is not None and s != prev:
            lo, hi = F(T) * (i - 1) / N, t
            for _ in range(60):
                m = (lo + hi) / 2
                dm = pos(0, 1, m) - pos(Lr, -1, m)
                if ((dm > 0) - (dm < 0)) == prev: lo = m
                else: hi = m
            meets.append((float(hi), float(pos(0, 1, hi))))
        if s != 0: prev = s
    return meets
R["D31-G2-V3 流水相遇(时刻,距A)"] = river_two(F(60), F(25), F(5))[:2]
R["D31-G2-V4 水速"] = 6 / 2
R["D31-G3-V1 级数"] = [30 + 15 * u for u in range(0, 10) if 30 + 15 * u == 36 + 12 * u]
u = bisect(lambda u: (3 + u) * 20 - (3 - u) * 60, 0, 2.99); R["D31-G3-V2 级数"] = (3 + u) * 20
u = bisect(lambda u: (24 + 12 * u) - (120 - 60 * u), 0, 1.99); R["D31-G3-V3 级数"] = 24 + 12 * u
R["D31-G3-V4 秒"] = 1 / (1 / 60 + 1 / 90)
R["D31-G4-V1 倍数"] = 180 / ((200 - 20) - (60 + 20 + 60))
v = bisect(lambda v: 45 * v - 3, 0.001, 1); R["D31-G4-V2 步速km/h"] = v * 60
# 周期休息追及（逐分钟精确）
def jia_rest(t):  # 分钟；5km/h，走50休10
    k, r = divmod(t, 60); return (k * 50 + min(r, 50)) * 5 / 60
tt = [t / 10 for t in range(1200, 3000) if abs(15 * (t / 10 - 120) / 60 - jia_rest(t / 10)) < 1e-9]
R["D31-G4-V3 乙出发后min"] = tt[0] - 120 if tt else None
truck_arrive = 120 / 60; comm_reach = 1 + 120 / 90
R["D31-G4-V4 回仓库(自8:00小时)"] = comm_reach + 120 / 90
x = bisect(lambda x: (5 * x) ** 2 - 30 ** 2 - (4 * x) ** 2, 0.1, 1000); R["D31-G5-V1 BC"] = 4 * x
R["D31-G5-V2 距离"] = (math.hypot(100, 50), 50 * math.sqrt(5))
ts = [i / 1000 for i in range(0, 3000)]
dmin = min((math.hypot(10 - 6 * t, 8 * t), t) for t in ts); R["D31-G5-V3 (最近,时h)"] = dmin
R["D31-G5-V4 增加km"] = math.sqrt(50 ** 2 - 30 ** 2) / 6
# 匀变速
a = bisect(lambda a: (1 + (1 + a)) / 2 * 1 - 3, 0, 100)  # 第1小时平均速度=甲速3（乙初速1）
dist = (1 + (1 + 2 * a)) / 2 * 2; R["D31-G6-V1 甲到达(自9:00 h)"] = dist / 3
S = bisect(lambda S: ((S / 3) / 16 + (S / 6) / 20) - (S / 2) / 20 - 2 / 60, 0.01, 100); R["D31-G6-V2 全程"] = S
v0 = F(1, 2); vavg = F(50, 30); vend = 2 * vavg - v0; acc = (vend - v0) / 30
R["D31-G6-V3 倍数"] = float(((vend - acc * 10) + vend) / 2)
R["D31-G6-V4 米"] = 20 * 0.5 + 20 * 4 / 2
# 两车同时到达最远距离
vj = bisect(lambda v: v * (1 + 3) - 6, 0.01, 10); acc = vj / 2
gaps = [(1.2 * t - (0.5 * acc * t * t if t <= 2 else 0.5 * acc * 4 + vj * (t - 2)), t) for t in [i / 1000 for i in range(0, 5001)]]
R["D31-G6-V5 最远米"] = max(gaps)[0] * 1000
# 图像
R["D31-G7-V1 最小直线距离"] = min(math.hypot(a, 100 - a) for a in [i / 100 for i in range(0, 10001)])
t = bisect(lambda t: t * t - 144, 0, 100); R["D31-G7-V2 相距"] = 7 * t
def sA(t):
    if t <= 3: return 60 * t
    if t <= 4: return 180
    if t <= 6: return 180 - 90 * (t - 4)
    return 0
def sB(t):
    return 180 - 30 * (t - 1) if 1 <= t <= 7 else (180 if t < 1 else 0)
ms = []
prev = None
for i in range(1, 6001):
    t = i / 1000
    d = sA(t) - sB(t); s = (d > 0) - (d < 0)
    if prev is not None and s != prev: ms.append((round(t, 3), round(sA(t), 2)))
    if s != 0: prev = s
R["D31-G7-V3 相遇(时,距A)"] = ms
# 往返多次（深化）
ev = line_events(F(3), F(7), F(100), F(200), F(0), F(100))
R["D31-G8-V1 S=100 事件(两端,3:7)"] = [(float(t), float(x), k) for t, x, k in ev[:5]]
ev = line_events(F(3), F(2), F(50), F(200), F(0), F(50))
R["D31-G8-V1' S=50 事件(两端,3:2)"] = [(float(t), float(x), k) for t, x, k in ev[:5]]
ev = line_events(F(7), F(2), F(300), F(1000))
R["D31-G8-V2 7:2 300m 追上"] = [(float(t), float(x)) for t, x, k in ev if k == "追上"][:4]
t3 = arrivals(F(3, 2), 0, 2, 0, 1, 2, 3)
R["D31-G8-V3 王到乙次数"] = sum(1 for n in range(1, 20) if arrivals(F(1), 1, 2, 2, -1, 2, n) < t3)
def two_trucks_max(L, v1, v2, start2=0, dir2=1, trips=1):
    def p(v, t, start, d):
        tot = 2 * L * trips
        dist = min(v * t, tot)
        x, _ = unfold_pos((start if d > 0 else 2 * L - start) + dist, L)
        return x
    best = 0
    T = 2 * L * trips / min(v1, v2)
    for i in range(0, 20001):
        t = T * i / 20000
        best = max(best, abs(p(v1, t, 0, 1) - p(v2, t, start2, dir2)))
    return best
R["D31-G8-V4 最远"] = two_trucks_max(F(40), F(80), F(60))

# ======================= Day 40 =======================
S = bisect(lambda S: (S / 4) / (8 + 3) - 10, 0.01, 100000)
R["D40-G1-V1 晚到min"] = (S / 3 + S / 6) - (S / 4 + S / 8)
S = bisect(lambda S: 5 * (S - 3 * (S / 3 - S / 5)) / 8 - 3, 0.1, 100); R["D40-G1-V2 山路"] = S
R["D40-G1-V3 上山速"] = [v for v in range(1, 20) if abs(12 / v - 12 / (v + 2) - 1) < 1e-9]
# 特殊模型
D = 1.0
u = bisect(lambda u: (1 - u / 3) - (1 - u) * 20 / 12, 0.01, 0.99)  # 以车速V=1；被超间隔 D/(1-u)=20, D/(1-u/3)=12
R["D40-G2-V1 发车间隔"] = 20 * (1 - u)
# 三批接送：车速 c=5，步行 w=1，求每批乘车占比（解方程组，独立模拟）
def three_batch(c, w, S=1.0):
    # 未知：每批乘车 d；三批同时到达，步行相同 x=S-d。用模拟求 d 使最后一批与第一批同时到达
    def sim(d):
        # 第1批从0上车，车开到 d 放下；回头接第2批（第2批从0步行）；第2批上车后车开 d 放下；回头接第3批...
        t = 0.0; car = 0.0; groups_x = [0.0, 0.0, 0.0]; arrive = []
        # 第1批
        t1 = d / c; car = d
        arr1 = t1 + (S - d) / w
        t = t1
        walkers = [1, 2]
        # 接第2批
        g2 = w * t
        tm = (car - g2) / (c + w); t += tm; car -= c * tm
        start = car; t += d / c; car = start + d
        arr2 = t + (S - car) / w
        g3 = w * t
        tm = (car - g3) / (c + w); t += tm; car -= c * tm
        t += (S - car) / c
        arr3 = t
        return arr1, arr2, arr3
    d = bisect(lambda d: sim(d)[0] - sim(d)[2], 0.01, S - 0.001)
    return d, sim(d)
R["D40-G2-V2 三批(乘车占比,到达)"] = three_batch(5.0, 1.0)
R["D40-G2-V3 乙走级数"] = 2 * (bisect(lambda t: 3 * (t - 10) - t, 10.01, 100) - 10)
w = 2 / ((20 + 20) / 60); R["D40-G2-V4 掉头时距落水处km"] = (18 - w) * (20 / 60)
L = bisect(lambda L: (L + 320) - 24 * L / 8, 1, 10000); R["D40-G2-V5 车长"] = L
# 运动几何：搜索整数勾股设定（仿2022GK-68）
cands = []
for X in range(5, 40):
    for Y in range(5, 40):
        for a in range(1, 20):
            for b in range(1, 20):
                if 4 * b != 3 * a: continue  # 速度比 4:3
                d1 = math.hypot(X - a, Y - b)
                for T2 in [2, 3, 4]:
                    if X - T2 * a >= 0 or Y - T2 * b >= 0:  # 要求 T2 时两人都已过路口
                        continue
                    d2 = math.hypot(T2 * a - X, T2 * b - Y)
                    if abs(d1 - round(d1)) < 1e-9 and abs(d2 - round(d2)) < 1e-9 and X - a > 0 and Y - b > 0 and X != Y:
                        cands.append((X, Y, a, b, round(d1), T2, round(d2), round((X / a - Y / b) * 60, 2)))
R["D40-G3-V2 候选(西距,北距,张速,李速,1h距,T2,T2距,张比李晚到min)"] = cands[:8]
n = 30; R["D40-G3-V1 甲速"] = bisect(lambda v: (n * math.sqrt(3)) / (math.sqrt(3) / 2 * v) - n / v - 2, 0.1, 1000)
R["D40-G3-V3 最近"] = min(math.hypot(3 * t, 100 - 4 * t) for t in [i / 100 for i in range(0, 5001)])
R["D40-G3-V4 分钟"] = 30 / math.sqrt(50 ** 2 - 30 ** 2) * 60
# 匀变速冲刺
dec = 30 * 50 / 2; accd = 30 * 40 / 2; R["D40-G4-V1 耽误秒"] = (50 + 120 + 40) - (dec + accd) / 30
T = bisect(lambda T: 1.5 * (T - 2) - 1.2 * T, 4, 1000); R["D40-G4-V2 (T分钟,全程km)"] = (T, 1.2 * T)
v1 = (125 / 5) * 2 - 30; a = (30 - v1) / 5; R["D40-G4-V3 出发点到第一根"] = v1 ** 2 / (2 * a)
def pos_yi(t):
    if t <= 10: return t * t
    s = t - 10
    if s <= 10: return 100 + 20 * s - s * s
    return 200
ts = [i / 100 for i in range(1, 4001)]
cross = [t for t in ts if abs(10 * t - pos_yi(t)) < 1e-9]
R["D40-G4-V4 相遇时刻"] = cross[:3]
# 环形
b = 20; a = 2 * b; R["D40-G5-V1 (d1,d2,丙第二次追乙t)"] = (2 * a, 5 * b, 3 + 300 / (a + b))
syn = 1 / (1 / 365 - 1 / 687)
import datetime
R["D40-G5-V2 下次火星冲日"] = (round(syn, 1), str(datetime.date(2025, 1, 16) + datetime.timedelta(days=round(syn))))
r = bisect(lambda r: 2 * 3 * (r + 20) / 1.5 - 1.2 * 2 * 3 * r, 0.1, 10000); R["D40-G5-V3 环面积"] = 3 * ((r + 20) ** 2 - r ** 2)
pts = set((F(3, 5) * k) % 1 for k in range(1, 100)); R["D40-G5-V4 不同相遇点"] = len(pts)
# 环形休息追及：搜索参数（甲每圈a分+休r分，乙每圈b分），首次追上在跑动段内部
found = []
for a_ in range(2, 9):
    for r_ in range(1, 4):
        for b_ in range(a_ + 1, 15):
            # 精确：逐个跑动段解方程
            for k in range(1, 60):
                t0 = (a_ + r_) * (k - 1)
                # 甲位置 (k-1) + (t-t0)/a_ ; 乙 t/b_ ; 追上: 甲 - 乙 = 1
                # (k-1) + (t - t0)/a_ - t/b_ = 1
                t = F((1 - (k - 1)) + F(t0, a_)) / (F(1, a_) - F(1, b_))
                ok = t0 < t < t0 + a_
                # 休息段内乙不可能被追上（甲不动）；检查此前段落是否已追上
                if t0 <= t <= t0 + a_:
                    found.append((a_, r_, b_, k, t, ok))
                    break
R["D40-G5-V5 候选(甲圈时,休,乙圈时,圈,时刻,内部?)"] = [f for f in found if f[5] and f[4].denominator == 1][:6]
# 往返高阶
R["D40-G6-V1 两端相向往返1次最远"] = None
def opposite_trip_max(L, v1, v2):
    # 甲 A->B->A，乙 B->A->B，各 1 次，到达后停
    def pa(t):
        d = min(v1 * t, 2 * L); x, _ = unfold_pos(d, L); return x
    def pb(t):
        d = min(v2 * t, 2 * L); x, _ = unfold_pos(L + d, L); return x  # 从B出发朝A
    T = 2 * L / min(v1, v2); best = (0, 0)
    for i in range(1, 30001):
        t = T * i / 30000
        best = max(best, (abs(pa(t) - pb(t)), t))
    return best
R["D40-G6-V1 两端相向往返1次最远"] = opposite_trip_max(F(60), F(90), F(60))
def robots_dispatch(L, left_times, right_times):
    # 事件驱动：入场事件 + 碰撞 + 到端
    evs = sorted([(F(t), 'L', i) for i, t in enumerate(left_times)] + [(F(t), 'R', i) for i, t in enumerate(right_times)])
    pos, dirs, tag, alive = [], [], [], []
    t = F(0); stops = []
    pending = list(evs)
    while pending or any(alive):
        idx = [i for i in range(len(pos)) if alive[i]]
        idx.sort(key=lambda i: pos[i])
        best = None
        for i in idx:
            dt = (L - pos[i]) if dirs[i] > 0 else pos[i]
            if dt > 0 and (best is None or dt < best[0]): best = (dt,)
        for a_, b_ in zip(idx, idx[1:]):
            if dirs[a_] > 0 and dirs[b_] < 0:
                dt = (pos[b_] - pos[a_]) / 2
                if best is None or dt < best[0]: best = (dt,)
        if pending:
            dt = pending[0][0] - t
            if best is None or dt <= best[0]: best = (dt,)
        dt = best[0]; t += dt
        for i in idx: pos[i] += dirs[i] * dt
        for i in idx:
            if alive[i] and (pos[i] <= 0 or pos[i] >= L) and dt > 0:
                alive[i] = False; stops.append((t, tag[i], 'left' if pos[i] <= 0 else 'right'))
        for a_, b_ in zip(idx, idx[1:]):
            if alive[a_] and alive[b_] and pos[a_] == pos[b_] and dirs[a_] > 0 and dirs[b_] < 0:
                dirs[a_], dirs[b_] = -1, 1
        while pending and pending[0][0] == t:
            _, side, i = pending.pop(0)
            pos.append(F(0) if side == 'L' else F(L)); dirs.append(1 if side == 'L' else -1)
            tag.append(side + str(i + 1)); alive.append(True)
    return stops
st = robots_dispatch(F(20), [0, 2, 4, 6], [1, 3, 5])
R["D40-G6-V2 停止(时刻,机器人,端)"] = [(float(a), b, c) for a, b, c in st]
ev = line_events(F(5), F(3), F(100), F(200), F(0), F(100))
R["D40-G6-V3 两端出发事件(5,3,100)"] = [(float(t), float(x), k) for t, x, k in ev[:5]]
# 渡船往返+停靠
def ferry(L, v1, v2, stay, T=40):
    def pos(v, start_at_left, t):
        x = 0.0 if start_at_left else L; tt = 0.0; d = 1 if start_at_left else -1
        while True:
            need = L / v
            if tt + need >= t: return x + d * v * (t - tt)
            tt += need; x = L if d > 0 else 0.0; d = -d
            if tt + stay >= t: return x
            tt += stay
    ms = []; prev = None; N = 400000
    for i in range(1, N):
        t = T * i / N
        dd = pos(v1, True, t) - pos(v2, False, t); s = (dd > 1e-12) - (dd < -1e-12)
        if prev is not None and s != prev and s != 0: ms.append(round(t, 3))
        if s != 0: prev = s
    return ms
R["D40-G6-V4 渡船相遇时刻(min)"] = ferry(1.2, 12 / 60, 8 / 60, 2)[:3]
R["D40-G6-V5 同时回起点min"] = math.lcm(36, 24, 18)
# 图像最值
R["D40-G7-V1 乙至多min"] = 9 / (6 / (90 - 15))
R["D40-G7-V3 甲追上乙(min)"] = bisect(lambda T: 1 * (T - 2) - 0.75 * T, 4, 100)
R["D40-G7-V4 乙至少m/s"] = 12 * 400 / 600 - 5
# 跨模块
R["D40-G8-V1 绿波最大km/h"] = max(v for v in [i / 100 for i in range(1, 1668)] if (600 / v) % 60 < 30 - 1e-9 or abs((600 / v) % 60) < 1e-9) * 3.6
R["D40-G8-V2 米"] = (340 * 2 + 20 * 2) / 2
R["D40-G8-V3 (A元,B元)"] = (30 * 2 + 30 / 60 * 60 * 0.5, 24 * 2 + 24 / 40 * 60 * 0.5)
R["D40-G8-V4 最省油速度"] = min((300 / v * (v * v / 400 + 4), v) for v in range(10, 120))

for k, v in R.items():
    print(k, "=>", v)
