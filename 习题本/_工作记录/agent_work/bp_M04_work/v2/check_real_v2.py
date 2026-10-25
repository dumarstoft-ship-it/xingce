# -*- coding: utf-8 -*-
"""M04 行程问题 真题核查 v2（本轮重新核对）。
(1) 5 道无官方答案真题：从题面数据出发模拟/枚举求解；
(2) 49 道有官方答案真题：逐题从题面数据独立复算（不代入官方答案），与官方答案比对；
    选项为图像的 2 道（2021SD-39、2020SC0725-47）复算距离函数的分段形状。
截图中缺失的分数/根式已对照 q_crop 确认：2021ZJA-62(3/4,1/3)、2024SD-60(1/3)、2025GK-74(√3n,2√3)、
2024SD-56(1/2,3/8)、2023SC-50(1/2)、2021ZJA-72 选项(√2,√3,4√3/3,2(√3−1))、2026GK-71 选项(5/7,7/5,7/10,10/7)。"""
import sys, json, math, datetime
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2')
from m04lib import *

def opt(options, value):
    return pick(options, value)

def solve_unique(cands):
    s = sorted(set(cands))
    assert len(s) == 1, s
    return s[0]

R, O, NOTE = {}, {}, {}

# =============== 自解 5 道 ===============
# 2026ZJA-48：8 点同时出发，甲每小时比乙多 1 km；11 点甲休息 1 h，乙继续，12 点乙赶上甲。问此时乙走了多少 km。
sol = []
for v100 in range(1, 3000):
    v = F(v100, 100)
    jia = Traj().move_for(3, v + 1).wait(1)
    yi = Traj().move_for(4, v)
    ms = [m for m in meetings(jia, yi) if m['t'] > 0]
    if ms and ms[0]['t'] == 4:
        sol.append(yi.pos(4))
R['2026ZJA-48'] = opt({'A': 9, 'B': 12, 'C': 15, 'D': 18}, solve_unique(sol))
NOTE['2026ZJA-48'] = '11点时甲领先3×1=3千米，乙在甲休息的1小时内补上→乙速3千米/小时，4小时走12千米'

# 2026GK-71：甲=0、丙=1、乙=2。张在[0,2]往返（从甲出发），王在[1,2]往返（从乙出发）。
# 王第5次到达乙与张第4次到达乙同时 → 速度比=同一时间内路程比。不预设比值：枚举张速/王速 = p/q，模拟检验。
def arrivals(tr, x):
    return [b for a, b, x0, x1 in tr.segs if b > a and x1 == x and x0 != x1]
hits = []
for p in range(1, 40):
    for q in range(1, 40):
        if math.gcd(p, q) != 1:
            continue
        zhang = Traj(0, 0)
        for k in range(12):
            zhang.move_to(2, F(p)).move_to(0, F(p))
        wang = Traj(0, 2)
        for k in range(12):
            wang.move_to(1, F(q)).move_to(2, F(q))
        if arrivals(wang, 2)[4] == arrivals(zhang, 2)[3]:
            hits.append(F(p, q))
R['2026GK-71'] = opt({'A': F(5, 7), 'B': F(7, 5), 'C': F(7, 10), 'D': F(10, 7)}, solve_unique(hits))
NOTE['2026GK-71'] = '设甲丙=丙乙=1：王第5次到乙跑了5×2=10，张第4次到乙跑了2+3×4=14，同时到达→速度比14:10=7/5'

# 2026GK-79：环形，甲乙顺时针、丙逆时针，速度比 4:5:6；甲丙、乙丙首次相遇间隔 5 秒；问乙首次追上甲。
def ring_first(v1, d1, v2, d2, L):
    """同点同时出发，逐秒外的精确求解：最小 t>0 使两者位置相同"""
    rel = abs(d1 * F(v1) - d2 * F(v2))
    return F(L) / rel
cands = []
for k in [F(1), F(2), F(3, 2)]:                 # 速度单位任取，检验结论与单位无关
    for L in range(1, 20000):
        if ring_first(4 * k, 1, 6 * k, -1, L) - ring_first(5 * k, 1, 6 * k, -1, L) == 5:
            cands.append(ring_first(5 * k, 1, 4 * k, 1, L))
t_catch = solve_unique(cands)                   # 秒
mins = t_catch / 60
R['2026GK-79'] = 'A' if mins < 8 else 'B' if mins < 9 else 'C' if mins < 10 else 'D'
assert t_catch == 550
NOTE['2026GK-79'] = '设速度4k、5k、6k，周长L：L/10k−L/11k=L/110k=5→L/k=550；乙追甲用L/(5k−4k)=550秒≈9分10秒'

# 2026ZJA-57：A 上游、B 下游，甲从 A 顺水、乙从 B 逆水，静水速相同，同时在 C 放竹排；某时刻甲、乙距竹排 2、8（均未相遇）。
vals = set()
for vb in [F(5), F(8), F(12), F(15), F(20)]:
    for w in [F(1), F(2), F(3)]:
        for x in [F(6), F(10), F(15), F(21)]:
            for y in [F(12), F(16), F(25), F(40)]:
                # 下游为正：甲(t)=(vb+w)t，竹排=x+wt，乙=x+y-(vb-w)t
                t1 = (x - 2) / vb          # 甲距竹排 2 的时刻（相对水速 vb）
                t2 = (y - 8) / vb          # 乙距竹排 8 的时刻
                if t1 == t2 and t1 > 0:
                    vals.add(y - x)
_lab = {F(6): 'y-x=6', F(-6): 'x-y=6', F(3): 'y-x=3', F(-3): 'x-y=3'}[solve_unique(vals)]
_hits = [k for k, s in {'A': 'x-y=3', 'B': 'x-y=6', 'C': 'y-x=3', 'D': 'y-x=6'}.items() if s == _lab]
assert len(_hits) == 1
R['2026ZJA-57'] = _hits[0]
NOTE['2026ZJA-57'] = '以水为参照竹排不动，甲、乙对竹排的接近速度都是静水速v：x−vt=2、y−vt=8→y−x=6'

# 2026GD-45：200 米直道往返，甲 140、乙 100 米/分，同时从起点出发。"追上"=同向且甲从后面赶上（含端点同时到达）。
jia = bounce(200, 140, 80)
yi = bounce(200, 100, 80)
catches = []
for m in meetings(jia, yi):
    t = m['t']
    if t <= 0:
        continue
    va, vb = jia.vel(t, -1), yi.vel(t, -1)
    if va * vb > 0:                  # 到达该点前两人同向
        e = F(1, 1000)
        # 之前甲在乙身后（沿运动方向）
        behind = (jia.pos(t - e) - yi.pos(t - e)) * (1 if va > 0 else -1) < 0
        if behind:
            catches.append((t, m['x']))
assert catches[:3] == [(10, 200), (20, 0), (30, 200)], catches[:3]
R['2026GD-45'] = opt({'A': 0, 'B': 50, 'C': 100, 'D': 200}, catches[1][1])
NOTE['2026GD-45'] = '往返直道展开成400米"环形"：甲每多跑400米追上一次，用时400÷40=10分钟；第2次在20分钟，甲跑2800米=7个来回，回到起点'

# =============== 49 道官方答案复算 ===============
L = F(60); O['2022HB-70'] = opt({'A': 30, 'B': 60, 'C': 15, 'D': 45}, (L / 2) / (L / 10 - L / 12))
O['2023SD-43'] = opt({'A': 100, 'B': 108, 'C': 116, 'D': 120}, 2 * F(20) / F(20, 60))
gap = F(3120) / 45 - F(3120) / 55
O['2023SZ-53'] = opt({'A': 11, 'B': 12, 'C': 13, 'D': 14}, math.ceil(gap))
NOTE['2023SZ-53'] = '精确值12.6小时，按"至少早起飞的整小时数"取13'
v = solve_unique([F(k, 10) for k in range(1, 3000) if F(6, 5) * F(k, 10) * 4 == F(k, 10) + 3 * (F(k, 10) + 30)])
O['2024GK-66'] = opt({'A': 540, 'B': 510, 'C': 600, 'D': 570}, F(6, 5) * v * 4)
rel = F(420) / F(36, 10) * F(36, 10)        # 米/秒 → 千米/时：420/3.6 m/s ×3.6
O['2024JSA-52'] = opt({'A': 210, 'B': 240, 'C': 450, 'D': 630}, rel - 180)
fa = Traj().move_to(100, 100).move_to(0, 100); son = Traj().move_to(100, 60)
m = [e for e in meetings(fa, son) if e['t'] > 1][0]
O['2025GD-38'] = opt({'A': 35, 'B': 30, 'C': 25, 'D': 15}, 100 - m['x'])
vz = F(150) / F(5, 2)
zh = Traj().move_for(F(5, 2), vz)
cand = []
for v10 in range(1, 3000):
    vl = F(v10, 10)
    li = Traj().wait(1).move_for(3, vl)
    ms = [e for e in meetings(zh, li) if e['t'] > 1]
    if ms and ms[0]['x'] == 135:
        cand.append(vl)
O['2025SC-55'] = opt({'A': 75, 'B': 90, 'C': 108, 'D': 120}, solve_unique(cand))
cand = [F(k, 10) for k in range(1, 1000) if F(k, 10) / 2 / 6 + F(1, 4) + F(k, 10) / 2 / 3 == F(5, 2)]
O['2025SD-52'] = opt({'A': 9, 'B': 10, 'C': 12, 'D': F(27, 2)}, solve_unique(cand))
O['2020HB-67'] = opt({'A': 1100, 'B': 1000, 'C': 960, 'D': 880}, 80 * F(1200 - 100, 40 + 60))
outs = set()
for a in [F(1, 2), F(1), F(2), F(3)]:          # 平路长度任取，坡长由总时间 1 小时定
    b = (1 - 2 * a / 9) / (F(1, 6) + F(1, 18))
    if b > 0: outs.add(a + b)
O['2020HB-73'] = opt({'A': 3.5, 'B': 4.5, 'C': 5.5, 'D': 6.5}, solve_unique(outs))
S = (F(500) * 3 + 2400) / F(3, 4); fast, slow = 2400, 1500
O['2020JSA-58'] = opt({'A': 1350, 'B': 1600, 'C': 1800, 'D': 1950}, S - S * F(slow, fast))
# 2020SD-36：400 米环形、相距 200 米同向；甲第三次追上乙时乙跑 2000 米。枚举速度比。
cand = []
for r100 in range(101, 400):
    r = F(r100, 100)
    t3 = (200 + 400 * 2) / (r - 1)            # 乙速度取 1
    if t3 * 1 == 2000:
        cand.append(r)
O['2020SD-36'] = opt({'A': 1.2, 'B': 1.5, 'C': 1.6, 'D': 2.0}, solve_unique(cand))
cand = []
for v10 in range(10, 200):
    v = F(v10, 10)
    wang = Traj().move_for(F(1, 4), v).move_for(F(1, 4), -v).move_for(10, F(6, 5) * v)
    li = Traj().move_for(F(15) / v, v)
    if wang.pos(F(15) / v) == 15:
        cand.append(v)
O['2020SZS-27'] = opt({'A': 4, 'B': 4.5, 'C': 5, 'D': 6}, solve_unique(cand))
outs = set()
for t in [F(1), F(2), F(7, 2)]:
    s = (80 * (7 * t + 5) - 400) / 2; outs.add(s / (4 * t))
O['2020ZJB-14'] = opt({'A': 70, 'B': 75, 'C': 80, 'D': 85}, solve_unique(outs))
x = solve_unique([F(k) for k in range(1, 1000) if (k + 10) * 120 - 100 * k == 2800])
O['2021JSA-54'] = opt({'A': 4.2, 'B': 4.5, 'C': 4.8, 'D': 5.4}, (x + 10) * 60 / 1000)
cand = []
for v10 in range(10, 300):
    v = F(v10, 10)
    for S10 in range(1, 300):
        S = F(S10, 10)
        T = S / v
        if T - S / (F(6, 5) * v) == F(1, 6) and T - (2 / v + (S - 2) / (F(13, 10) * v)) == F(1, 6):
            cand.append(S)
O['2021SC2-47'] = opt({'A': 5.4, 'B': 7.2, 'C': 8.5, 'D': 9.6}, solve_unique(cand))
# 2021SD-39：正方形边长 40、速度 1，乙在甲到 AB 中点（T=20）时出发。距离函数分段形状。
def sq_pos(s, side=40):
    s = s % (4 * side)
    pts = [(0, 0), (0, side), (side, side), (side, 0)]      # A(0,0)→B(0,40)→C→D 顺时针
    k = int(s // side); r = s - k * side
    (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % 4]
    return (x0 + (x1 - x0) * r / side, y0 + (y1 - y0) * r / side)
def dist39(T):
    a = sq_pos(T); b = sq_pos(max(0, T - 20))
    return math.hypot(a[0] - b[0], a[1] - b[1])
assert all(abs(dist39(t) - t) < 1e-9 for t in [5, 10, 20])                 # 0~20 线性上升
assert all(abs(dist39(t) - 20) < 1e-9 for t in [25, 30, 39, 65, 75])     # 同边时恒为 20
assert abs(dist39(50) - 10 * math.sqrt(2)) < 1e-9                          # 拐角处下凹到 10√2
mid = dist39(50); chord = (dist39(45) + dist39(55)) / 2
assert dist39(45) < (dist39(40) + dist39(50)) / 2                          # 凸（"凹函数"）弧
O['2021SD-39'] = 'C'
NOTE['2021SD-39'] = '复算：0~20线性升到20，同边时恒20，过拐角时降到10√2≈14.1再回升，且弧形下凸→对应C'
AB, BC = F(3), F(4)
v = (AB + BC / 2) / 150
O['2021ZJA-62'] = opt({'A': 165, 'B': 170, 'C': 190, 'D': 195}, BC / (2 * v) + AB / (v * F(2, 3)))
west = math.sqrt(160 ** 2 - 80 ** 2)
O['2021ZJA-72'] = opt({'A': math.sqrt(2), 'B': math.sqrt(3), 'C': 4 * math.sqrt(3) / 3, 'D': 2 * (math.sqrt(3) - 1)}, west / 60)
S = solve_unique([F(k, 10) for k in range(1, 1000) if (F(k, 10) / 4) / 18 - (F(k, 10) / 4) / 21 == F(3, 60)])
O['2022GK-65'] = 'D' if S > 25 else 'C' if S > 24 else 'B' if S > 23 else 'A'
ans = []
for a in range(1, 20):
    for b in range(1, 20):
        if F(b) != F(3, 5) * a: continue
        d1 = math.hypot(17 - a, 8 - b); d4 = math.hypot(17 - 4 * a, 8 - 4 * b)
        if abs(d1 - 13) < 1e-9 and abs(d4 - 5) < 1e-9 and 4 * a >= 17 and 4 * b >= 8:
            diff = (F(17, a) - F(8, b)) * 60
            ans.append('D' if diff > 10 else 'C' if diff > 0 else 'B' if diff < -10 else 'A')
O['2022GK-68'] = solve_unique(ans)
jia = Traj().move_to(900, 5).move_to(0, 9); yi = Traj().move_to(900, 3).move_to(0, 5)
m = [e for e in meetings(jia, yi) if e['kind'] == 'head-on'][0]
O['2022SC2-50'] = opt({'A': 270, 'B': 390, 'C': 510, 'D': 630}, m['x'])
outs = set()
for t3 in [F(1, 10), F(1, 5), F(3, 10), F(2, 5)]:
    t1 = 3 * t3; t2 = 2 - t1 - t3
    if t2 > 0: outs.add(2 * t1 + 3 * t2 + 6 * t3)
O['2023GD-38'] = opt({'A': -1, 'B': 6, 'C': 8, 'D': 12}, solve_unique(outs))
outs = set()
for u in [F(2), F(4), F(10)]:
    v0 = u / 2
    a = solve_unique([F(k, 100) * u for k in range(1, 500) if v0 * 2 + F(k, 100) * u * 2 == u * 2])
    SB = v0 * 3 + a * 9 / 2
    outs.add(SB / u)
hrs = solve_unique(outs)
O['2023GK-72'] = opt({'A': F(7, 2), 'B': F(15, 4), 'C': 4, 'D': F(17, 4)}, hrs)
outs = set()
for vy in [F(1), F(2), F(5)]:
    T = F(4000) / vy
    ride = 3600
    repair = T - ride / (3 * vy)
    outs.add(repair * vy)
O['2023JSA-58'] = opt({'A': 3000, 'B': 2800, 'C': 2400, 'D': 2000}, solve_unique(outs))
# 2023SD-36：以 17:00 为 0 时刻（分钟）。放学 18:00=60。母亲单程 T 分钟，车速 c，小张步速 w。
outs = set()
for T in [F(20), F(30), F(40)]:
    c = F(1)                                    # 车速取 1（路程单位：车行 1 分钟）
    for w in [F(k, 50) for k in range(1, 50)]:
        # 小张 30 分时从学校（距家 T）出发向家走；母亲 60−T 时刻从家出发
        start_m = 60 - T
        # 相遇：c(t − start_m) + w(t − 30) = T
        t = (T + c * start_m + w * 30) / (c + w)
        if t < 30 or t > 60: continue
        home = t + (t - start_m)
        if (60 + T) - home == 10:
            outs.add(t - 30)
O['2023SD-36'] = opt({'A': 20, 'B': 25, 'C': 15, 'D': 10}, solve_unique(outs))
O['2023SZ-60'] = opt({'A': 30, 'B': 40, 'C': 50, 'D': 60}, 1 / (F(1, 20) - F(1, 40)))
w = F(1); up, down = 5 * w - w, 5 * w + w
t_meet = F(15) / up                       # 单位：1.31 千米
total = 15 + down * t_meet
O['2023ZJA-59'] = opt({'A': 38, 'B': 39, 'C': 76, 'D': 78}, 2 * (math.floor(total) + 1))
CB = F(320) / 4; CD = CB / 3; BD = math.sqrt(CB ** 2 + CD ** 2)
O['2023ZJA-67'] = 'A' if BD < 80 else 'B' if BD < 90 else 'C' if BD < 100 else 'D'
cand = []
for v in range(1, 5000):
    v = F(v)
    total = v * 1 + 2 * v * 1                   # 山脚—凉亭上山 v×1；凉亭—山顶 = 下山 2v×1 小时
    if v + 500 == total / 2 and F(v) / (2 * v) == F(1, 2):
        cand.append(total)
O['2024GD-44'] = opt({'A': 2000, 'B': 3000, 'C': 3600, 'D': 4000}, solve_unique(cand))
cand = []
for r in range(1, 2000):
    R_ = r + 50
    if F(2 * 3 * r, 5) == 4 * F(2 * 3 * R_, 30):
        cand.append(3 * F(r) ** 2 / 10000)
O['2024HB-75'] = opt({'A': 2, 'B': 3, 'C': 4, 'D': 6}, solve_unique(cand))
BC2 = F(900) / (F(16, 9) - 1)
O['2024SD-60'] = opt({'A': 26, 'B': 28, 'C': 30, 'D': 34}, round(math.sqrt(BC2)))
cand = []
for v in range(1, 500):
    lang, feng = 5 * F(v), 6 * F(v)             # 同一段路小朗用 6 分、小峰用 5 分 → 速度比 5:6
    if (feng - lang) * 6 == 180:
        cand.append(lang * 60 / 1000)
O['2024SZ-56'] = opt({'A': 6, 'B': 7.2, 'C': 9, 'D': 10.8}, solve_unique(cand))
cand = []
for D in range(61, 2000):
    D = F(D)
    jia_t = 60 + 20 + (D - 60)
    yi_t = 60 + 20 + 60 + D / 5
    if jia_t - yi_t == 12:
        cand.append(jia_t)
O['2024ZJA-61'] = opt({'A': 165, 'B': 175, 'C': 185, 'D': 195}, solve_unique(cand))
cand = []
yi_v, jia_v = F(1), F(2)
S = (yi_v + jia_v) * 3
cand = [S / 2 / jia_v]                          # 第二次相遇前甲也跑了半圈
O['2025GK-68'] = opt({'A': 2 + F(10, 60), 'B': F(9, 4), 'C': 2 + F(20, 60), 'D': F(5, 2)}, solve_unique(cand))
n = math.sqrt(120 ** 2 / 4)
vj = solve_unique([F(k, 10) for k in range(1, 1000) if abs(n / (k / 10) - (math.sqrt(3) * n) / (2 * math.sqrt(3) * k / 10) - 3) < 1e-9])
O['2025GK-74'] = opt({'A': 10, 'B': 15, 'C': 10 * math.sqrt(3), 'D': 15 * math.sqrt(3)}, vj)
outs = set()
for a in [F(1), F(2), F(7, 2)]:
    b = solve_unique([F(k, 10) * a for k in range(1, 200) if 1 / a + 2 / (F(k, 10) * a) == 1 / (F(6, 5) * a) + 2 / (F(4, 5) * F(k, 10) * a)])
    outs.add(F(6, 5) * a / (F(4, 5) * b))
O['2025JSA-60'] = opt({'A': F(1, 3), 'B': F(2, 5), 'C': F(5, 12), 'D': F(1, 2)}, solve_unique(outs))
cand = [F(v) for v in range(1, 300) if F(v) / 2 * F(10, 60) + F(27, 2) == F(v) * F(20, 60)]
O['2025ZJA-61'] = opt({'A': 54, 'B': 63, 'C': 72, 'D': 81}, solve_unique(cand))
# 2020SC0725-47：选项为图像。复算距离函数：相遇前 100−2t−t²/2（下凹递减），相遇后 2t+t²/2−100（上凸递增），乙到端后 2t（直线）
tm = -2 + math.sqrt(4 + 200)                 # 相遇
ty = math.sqrt(200)                          # 乙到终点
assert 12 < tm < ty < 50
O['2020SC0725-47'] = 'D'
NOTE['2020SC0725-47'] = '复算：相遇前距离100−2t−t²/2（开口向下、越降越快），约12.3秒相遇；相遇后2t+t²/2−100陡升，约14.1秒乙到终点停下，此后距离=2t直线上升到100（t=50）→对应D'
cand = [F(v) for v in range(1, 200) if 30 * (F(1, 2) + F(10, v)) + 10 == 2 * v]
O['2020SZ1-48'] = opt({'A': 20, 'B': 18, 'C': 16, 'D': 15}, solve_unique(cand))
cand = [F(k, 2) for k in range(1, 36) if (18 - F(k, 2)) / 8 + F(k, 2) / 4 == 3]
O['2020SZS-16'] = opt({'A': 4, 'B': 6, 'C': 12, 'D': 18}, solve_unique(cand))
# 2021ZJA-71：环形 360，顺时针。设乙在 0，甲在乙后 d1，丙在乙后 d2（d2>d1）。
cand = []
for a in range(1, 400):          # 甲乙速度差
    for c in range(1, 400):      # 丙乙速度差
        d1, d2 = 3 * a, F(9, 2) * c
        if (c - a) > 0 and F(d2 - d1) / (c - a) == 8 and F(d2 + 360) / c == F(27, 2) and d2 < 360:
            cand.append(d1)
O['2021ZJA-71'] = opt({'A': 48, 'B': 84, 'C': 108, 'D': 144}, solve_unique(cand))
def jia58():
    tr = Traj(0, 0).wait(15)
    for k in range(3):
        tr.move_to(3 * (k + 1), F(1, 10))
        if k < 2: tr.wait(15)
    return tr
ok = []
for mins in range(46, 400):
    u = F(9, mins); yi = Traj(0, 0).move_to(9, u); jia = jia58()
    inner = set(mm['t'] for mm in meetings(jia, yi) if 0 < mm['x'] < 9 and mm['t'] > 0)
    if len(inner) == 2:
        ok.append(mins)
O['2022JSA-58'] = opt({'A': 75, 'B': 120, 'C': 135, 'D': 150}, min(ok))
def shuttle(Lab, v, trips):
    tr = Traj(0, 0)
    for k in range(trips):
        tr.move_to(Lab, v).move_to(0, v)
    return tr
A_, B_ = shuttle(30, 100, 2), shuttle(30, 80, 2)
pts = sorted(A_.breakpoints() | B_.breakpoints())
best = max(abs(A_.pos(t) - B_.pos(t)) for t in pts)
O['2022SC1-47'] = opt({'A': 18, 'B': 20, 'C': 24, 'D': 30}, best)
cand = []
for N in range(13, 300):
    for r10 in range(1, 100):                  # 扶梯速度/乙速 = r
        r = F(r10, 10)
        # 甲速 2、乙速 1、扶梯 r：甲走 36 级用时 18 → N = 36 + 18 r；乙后半程走 12 级用时 12 → N/2 = 12 + 12 r
        if N == 36 + 18 * r and F(N, 2) == 12 + 12 * r:
            cand.append(N)
O['2023SC-50'] = opt({'A': 48, 'B': 60, 'C': 66, 'D': 72}, solve_unique(cand))
# 2023SZ-56：按真实规则（相遇即掉头、到端点停止）做事件模拟，不用"等效穿越"。
def soldiers():
    spawns = [(F(k), 0, +1) for k in range(7)] + [(F(1, 2) + k, 9, -1) for k in range(8)]
    active = []      # [pos, dir]
    stopped_times = []
    t = F(0)
    pending = sorted(spawns)
    while pending or active:
        # 候选事件：下一次出生、端点到达、相邻相向相遇
        cand_t = []
        if pending: cand_t.append(pending[0][0] - t)
        for p, d in active:
            cand_t.append((9 - p) if d > 0 else p)
        act = sorted(active)
        for (p1, d1), (p2, d2) in zip(act, act[1:]):
            if d1 > 0 and d2 < 0:
                cand_t.append((p2 - p1) / 2)
        dt = min(x for x in cand_t if x >= 0)
        t += dt
        active = [[p + d * dt, d] for p, d in active]
        # 端点停止
        still = []
        for p, d in active:
            if (p >= 9 and d > 0) or (p <= 0 and d < 0):
                stopped_times.append(t)
            else:
                still.append([p, d])
        active = still
        # 相遇掉头（位置重合、相向）
        pos_groups = {}
        for i, (p, d) in enumerate(active):
            pos_groups.setdefault(p, []).append(i)
        for p, idx in pos_groups.items():
            if len(idx) == 2 and active[idx[0]][1] != active[idx[1]][1]:
                for i in idx: active[i][1] *= -1
            assert len(idx) <= 2
        while pending and pending[0][0] == t:
            _, p, d = pending.pop(0); active.append([F(p), d])
    return max(stopped_times), len(stopped_times)
last, cnt = soldiers()
assert cnt == 15
O['2023SZ-56'] = opt({'A': F(33, 2), 'B': 17, 'C': F(35, 2), 'D': 18}, last)
plan = F(100)                                     # 计划速度任取
first = 30 * plan; mid_v = first / 50; rest = 120 * plan - 2 * first
avg = rest / 40; vend = 2 * avg - mid_v; acc = (vend - mid_v) / 40
last10 = (vend - acc * 10 + vend) / 2; ratio = last10 / plan
O['2024SC-50'] = 'A' if ratio < F(18, 10) else 'B' if ratio < 2 else 'C' if ratio <= F(22, 10) else 'D'
cand = []
for S in range(24, 3000, 24):
    S = F(S)
    wang_up, li_up = F(4), F(3)                   # 由"王剩 1/2 时李走了 3/8"得 4:3，赋值 4u、3u（u 待定）
    for u10 in range(1, 200):
        u = F(u10, 10)
        tw = S / (wang_up * u)
        li_rest = S - li_up * u * tw
        if li_rest / (li_up * u + F(3, 2) * wang_up * u) == 10:
            dw = S / (wang_up * u) + S / (F(3, 2) * wang_up * u)
            dl = S / (li_up * u) + S / (F(3, 2) * li_up * u)
            cand.append(dl - dw)
O['2024SD-56'] = opt({'A': 30, 'B': 40, 'C': 50, 'D': 60}, solve_unique(cand))
syn_years = 1 / (1 - F(1, 12))
d = datetime.date(2024, 12, 8) + datetime.timedelta(days=round(float(syn_years) * 365.25))
O['2026CQ-58'] = 'A' if (d.year, d.month) <= (2025, 9) else 'B' if (d.year == 2026 and d.month <= 3) else 'C' if (d.year == 2026 and d.month <= 6) else 'D'
NOTE['2026CQ-58'] = '地球每年比木星多转1−1/12圈，会合周期=12/11年≈398天，2024-12-08+398天≈%s' % d

data = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tasks_in/M04.json'))
official = {q['id']: q['answer_official'] for q in data['real']}
need_self = sorted(q['id'] for q in data['real'] if q['needs_self_solve'])
bad = [k for k, v in O.items() if v != official.get(k)]
missing = sorted(set(k for k, v in official.items() if v) - set(O))
assert sorted(R) == need_self, (sorted(R), need_self)
print('自解：', R)
print('官方答案复算：%d 道；不一致：%s；未复算：%s' % (len(O), bad, missing))
json.dump({'self': R, 'official_check': O, 'note': NOTE, 'mismatch': bad, 'unchecked': missing},
          open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2/real_check_result.json', 'w'),
          ensure_ascii=False, indent=1, default=str)
