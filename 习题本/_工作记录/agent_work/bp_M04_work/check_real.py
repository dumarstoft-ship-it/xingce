# -*- coding: utf-8 -*-
"""M04 真题核查：(1) 5 道无官方答案真题自解（过程模拟）；(2) 43 道有官方答案真题独立复算。
截图中缺失的分数/根式已对照 q_crop 确认：2021ZJA-62(3/4,1/3)、2024SD-60(1/3)、2025GK-74(√3n,2√3)、
2024SD-56(1/2,3/8)、2023SC-50(1/2)、2021ZJA-72 选项(√2,√3,4√3/3,2(√3−1))、2026GK-71 选项(5/7,7/5,7/10,10/7)。"""
import sys, json, math, datetime
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work')
from m04lib import *

R = {}
# ---------------- 自解 5 道 ----------------
# 2026ZJA-48：8 点同时出发，甲比乙每小时多 1 km，11 点甲休息 1 小时，乙 12 点赶上甲。枚举乙速度，模拟两人位置。
sol = []
for v10 in range(1, 300):
    v = F(v10, 10)
    jia = Traj().move_for(3, v + 1).wait(1)     # 8-11 走，11-12 休息
    yi = Traj().move_for(4, v)
    ms = [m for m in meetings(jia, yi) if m['t'] > 0]
    if ms and ms[0]['t'] == 4:                  # 第一次"赶上"恰在 12 点（出发后 4 h）
        sol.append((v, yi.pos(4)))
assert len(sol) == 1
R['2026ZJA-48'] = pick({'A': 9, 'B': 12, 'C': 15, 'D': 18}, sol[0][1])

# 2026GK-71：甲=0，丙=1，乙=2；张在[0,2]往返，王在[1,2]往返（从乙出发）。
def nth_arrival(tr, x, n, exclude_start=True):
    cnt = 0
    for a, b, x0, x1 in tr.segs:
        if x1 == x and b > a and (x0 != x1):
            cnt += 1
            if cnt == n:
                return b
    raise ValueError
zhang = Traj(0, 0)
for k in range(10):
    zhang.move_to(2, 1).move_to(0, 1)
wang = Traj(0, 2)
for k in range(10):
    wang.move_to(1, 1).move_to(2, 1)
t_wang5 = nth_arrival(wang, 2, 5)            # 王速度=1 时第 5 次到乙的时刻
t_zhang4 = nth_arrival(zhang, 2, 4)          # 张速度=1 时第 4 次到乙的时刻
ratio = t_zhang4 / t_wang5                    # 同一时刻到达 => 张速/王速 = 路程比
R['2026GK-71'] = pick({'A': F(5, 7), 'B': F(7, 5), 'C': F(7, 10), 'D': F(10, 7)}, ratio)

# 2026GK-79：环形，甲乙顺时针、丙逆时针，速度 4k:5k:6k，甲丙/乙丙首次相遇间隔 5 秒。取 k=1，扫描周长 L 求出时间差=5 的 L，再求乙首次追上甲。
def first_meet_ring(v1, d1, v2, d2, L):
    # 同点出发，求最小 t>0 使位置重合
    rel = abs(d1 * v1 - d2 * v2)
    return F(L) / rel
cands = []
for L in range(1, 5000):
    if first_meet_ring(4, 1, 6, -1, L) - first_meet_ring(5, 1, 6, -1, L) == 5:
        cands.append(L)
assert cands == [550], cands
t_catch = first_meet_ring(5, 1, 4, 1, 550)  # 秒
mins = t_catch / 60
R['2026GK-79'] = 'A' if mins < 8 else 'B' if mins < 9 else 'C' if mins < 10 else 'D'

# 2026ZJA-57：下游为正方向。A=0（上游），C=x，B=x+y。甲从 A 向下游，乙从 B 向上游，竹排从 C 随水漂。
vals = set()
for vb in [8, 12, 15, 20]:
    for w in [1, 2, 3]:
        for x in [10, 15, 21]:
            # 由"甲距竹排 2、乙距竹排 8，均未相遇"求时刻 t：甲(t)=(vb+w)t，竹排=x+wt -> x - vb t = 2
            t = F(x - 2, vb)
            jia = (vb + w) * t; raft = x + w * t
            # 乙：raft + 8 = (x+y) - (vb-w) t  -> y = 8 + vb t
            y = 8 + vb * t
            yi = x + y - (vb - w) * t
            assert raft - jia == 2 and yi - raft == 8
            vals.add(y - x)
assert len(vals) == 1
R['2026ZJA-57'] = pick({'A': -3, 'B': -6, 'C': 3, 'D': 6}, vals.pop())   # A:x-y=3 即 y-x=-3

# 2026GD-45：200 m 直道往返，甲 140、乙 100 m/min，同时从起点出发；"追上"=同向且甲从后面赶上。
jia = bounce(200, 140, 60); yi = bounce(200, 100, 60)
ev = [m for m in meetings(jia, yi) if m['t'] > 0]
catches = []
for m in ev:
    t = m['t']; e = F(1, 10**6)
    # 端点处同时到达：看到达前两人方向
    va, vb = jia.vel(t, -1), yi.vel(t, -1)
    if va * vb > 0:
        catches.append((t, m['x']))
R['2026GD-45_events'] = [(str(t), str(x)) for t, x in catches[:4]]
R['2026GD-45'] = pick({'A': 0, 'B': 50, 'C': 100, 'D': 200}, catches[1][1])

# ---------------- 43 道官方答案复算 ----------------
O = {}
L = F(60); O['2022HB-70'] = pick({'A': 30, 'B': 60, 'C': 15, 'D': 45}, (L / 2) / (L / 10 - L / 12))
O['2023SD-43'] = pick({'A': 100, 'B': 108, 'C': 116, 'D': 120}, F(20) * 2 / F(1, 3))
v = F(90, 8) * 10  # 1.2v*4 = v + 3(v+30) -> 0.8v = 90
assert F(12, 10) * v * 4 == v + 3 * (v + 30)
O['2024GK-66'] = pick({'A': 540, 'B': 510, 'C': 600, 'D': 570}, F(12, 10) * v * 4)
O['2024JSA-52'] = pick({'A': 210, 'B': 240, 'C': 450, 'D': 630}, F(420) / F(36, 10) * F(36, 10) - 180)
k = F(100, 60); O['2025GD-38'] = pick({'A': 35, 'B': 30, 'C': 25, 'D': 15}, 40 * k / (k + 1))
vz = F(150) / F(5, 2); tz = F(135) / vz; O['2025SC-55'] = pick({'A': 75, 'B': 90, 'C': 108, 'D': 120}, F(135) / (tz - 1))
S = (F(5, 2) - F(1, 4)) / (F(1, 12) + F(1, 6)); O['2025SD-52'] = pick({'A': 9, 'B': 10, 'C': 12, 'D': F(27, 2)}, S)
O['2020HB-67'] = pick({'A': 1100, 'B': 1000, 'C': 960, 'D': 880}, 80 * F(1100, 100))
outs = set()
for a in [F(1, 2), F(1), F(2)]:
    b = (1 - 2 * a / 9) / (F(1, 6) + F(1, 18)); outs.add(a + b)
assert len(outs) == 1; O['2020HB-73'] = pick({'A': 3.5, 'B': 4.5, 'C': 5.5, 'D': 6.5}, outs.pop())
S = (F(1500) + 2400) / F(3, 4); O['2020JSA-58'] = pick({'A': 1350, 'B': 1600, 'C': 1800, 'D': 1950}, S - S * F(1500, 2400))
O['2020SD-36'] = pick({'A': 1.2, 'B': 1.5, 'C': 1.6, 'D': 2.0}, F(2000 + 200 + 800, 2000))
# 2020SZS-27：小王往返 30 min 后以 1.2v 追，在乙地(15km)追上
for v10 in range(10, 100):
    v = F(v10, 10)
    if F(15) / v == F(1, 2) + F(15) / (F(6, 5) * v):
        O['2020SZS-27'] = pick({'A': 4, 'B': 4.5, 'C': 5, 'D': 6}, v)
outs = set()
for t in [F(1), F(2), F(7, 2)]:
    s = (80 * (7 * t + 5) - 400) / 2; outs.add(s / (4 * t))
assert len(outs) == 1; O['2020ZJB-14'] = pick({'A': 70, 'B': 75, 'C': 80, 'D': 85}, outs.pop())
x = F(2800 - 1200, 20); O['2021JSA-54'] = pick({'A': 4.2, 'B': 4.5, 'C': 4.8, 'D': 5.4}, (x + 10) * 60 / 1000)
T0 = F(10) / (1 - F(5, 6))  # 提速 20% 省 10 分钟 -> 原时 60 分钟
# 原速 2 km 后提速 30% 省 10 分钟：剩余原用时 r 满足 r - r/1.3 = 10
r = F(10) / (1 - F(10, 13)); first = T0 - r; v = F(2) / (first / 60)
O['2021SC2-47'] = pick({'A': 5.4, 'B': 7.2, 'C': 8.5, 'D': 9.6}, v * T0 / 60)
AB, BC = F(3), F(4); v = (AB + BC / 2) / 150; back = BC / (2 * v) + AB / (v * F(2, 3))
O['2021ZJA-62'] = pick({'A': 165, 'B': 170, 'C': 190, 'D': 195}, back)
O['2021ZJA-72'] = pick({'A': math.sqrt(2), 'B': math.sqrt(3), 'C': 4 * math.sqrt(3) / 3, 'D': 2 * (math.sqrt(3) - 1)}, math.sqrt(160**2 - 80**2) / 60)
S = F(3, 60) / (F(1, 4) / 18 + F(1, 4) / 21 - F(1, 2) / 21)
O['2022GK-65'] = 'D' if S > 25 else 'C' if S > 24 else 'B' if S > 23 else 'A'
ans = []
for a in range(1, 20):
    for b in range(1, 20):
        if F(b) != F(3, 5) * a: continue
        d1 = math.hypot(17 - a, 8 - b); d4 = math.hypot(17 - 4 * a, 8 - 4 * b)
        if abs(d1 - 13) < 1e-9 and abs(d4 - 5) < 1e-9 and 4 * a >= 17 and 4 * b >= 8:
            diff = (F(17, a) - F(8, b)) * 60
            ans.append('D' if diff > 10 else 'C' if diff > 0 else 'B' if diff < -10 else 'A')
assert len(ans) == 1; O['2022GK-68'] = ans[0]
# 2022SC2-50：模拟 900 m 往返，甲逆 5u、顺 9u，乙逆 3u（乙未到 B 前迎面）
jia = Traj().move_to(900, 5).move_to(0, 9); yi = Traj().move_to(900, 3).move_to(0, 5)
m = [e for e in meetings(jia, yi) if e['kind'] == 'head-on'][0]
O['2022SC2-50'] = pick({'A': 270, 'B': 390, 'C': 510, 'D': 630}, m['x'])
outs = set()
for frog in [F(3, 10), F(6, 10), F(9, 10)]:
    t_walk = frog * 2 / 6; t_swim = 2 - frog - t_walk; outs.add(2 * frog * 2 + 3 * t_swim)
assert len(outs) == 1; O['2023GD-38'] = pick({'B': 6, 'C': 8, 'D': 12}, outs.pop())
# 2023GK-72：甲初速 1、乙 2，匀加速 a，2 h 时路程相同
a = F(1)  # 1*2 + a*4/2 = 4 -> a = 1
SB = 3 + a * 9 / 2; O['2023GK-72'] = pick({'A': 11.5, 'B': 11.75, 'C': 12, 'D': 12.25}, 8 + SB / 2)
O['2023JSA-58'] = pick({'A': 3000, 'B': 2800, 'C': 2400, 'D': 2000}, (F(4000) - F(3600, 3)) * 1)
outs = set()
for T in [F(20), F(30), F(45)]:
    # 以 17:30 为 0 点：小张 0 时刻步行；母亲照常 30-T 出发、单程 T；到家比往常早 10 -> 相遇时刻 t
    t = F(25)  # 待验证：到家时刻 = t + (t - (30 - T)) = 2t - 30 + T，往常 30 + T，早 10 -> 2t = 50
    assert (30 + T) - (2 * t - 30 + T) == 10
    outs.add(t)
O['2023SD-36'] = pick({'A': 20, 'B': 25, 'C': 15, 'D': 10}, outs.pop())
t_meet = F(15, 4); seg_down = 6 * t_meet; total = 15 + seg_down
O['2023ZJA-59'] = pick({'A': 38, 'B': 39, 'C': 76, 'D': 78}, 2 * (math.floor(total) + 1))
CB = F(80); CD = CB / 3; BD = math.sqrt(CB**2 + CD**2)
O['2023ZJA-67'] = 'A' if BD < 80 else 'B' if BD < 90 else 'C' if BD < 100 else 'D'
v = F(1000); assert (v + 500) * 2 == 2 * v * F(3, 2)
O['2024GD-44'] = pick({'A': 2000, 'B': 3000, 'C': 3600, 'D': 4000}, 2 * v * F(3, 2))   # 下山速度 2v、用时 1.5 h
r = F(100); R_ = r + 50; assert 2 * 3 * r / 5 == 4 * (2 * 3 * R_ / 30)
O['2024HB-75'] = pick({'A': 2, 'B': 3, 'C': 4, 'D': 6}, 3 * r * r / 10000)
x2 = F(900, 7); O['2024SD-60'] = pick({'A': 26, 'B': 28, 'C': 30, 'D': 34}, round(math.sqrt(9 * x2)))
v = F(180, 6); O['2024SZ-56'] = pick({'A': 6, 'B': 7.2, 'C': 9, 'D': 10.8}, 5 * v * 60 / 1000)
t = F(132, 4); O['2024ZJA-61'] = pick({'A': 165, 'B': 175, 'C': 185, 'D': 195}, 120 + t + 12 + 20)
O['2025GK-68'] = pick({'A': 2 + F(10, 60), 'B': F(9, 4), 'C': 2 + F(20, 60), 'D': F(5, 2)}, F(9, 2) / 2)
O['2025GK-74'] = pick({'A': 10, 'B': 15, 'C': 10 * math.sqrt(3), 'D': 15 * math.sqrt(3)}, (60 - 60 * math.sqrt(3) / (2 * math.sqrt(3))) / 3)
outs = set()
for x in [F(1), F(2), F(37, 10)]:
    y = 3 * x  # 由 1/x+2/y = 1/(1.2x)+2/(0.8y) 解得
    assert 1 / x + 2 / y == 1 / (F(6, 5) * x) + 2 / (F(4, 5) * y)
    outs.add(F(6, 5) * x / (F(4, 5) * y))
O['2025JSA-60'] = pick({'A': F(1, 3), 'B': F(2, 5), 'C': F(5, 12), 'D': F(1, 2)}, outs.pop())
v = F(54); assert v / 2 * F(10, 60) + F(27, 2) == v * F(20, 60)
O['2025ZJA-61'] = pick({'A': 54, 'B': 63, 'C': 72, 'D': 81}, v)
v = F(20); assert 30 * (F(1, 2) + 10 / v) + 10 == 2 * v
O['2020SZ1-48'] = pick({'A': 20, 'B': 18, 'C': 16, 'D': 15}, v)
x = F(6); assert (18 - x) / 8 + x / 4 == 3
O['2020SZS-16'] = pick({'A': 4, 'B': 6, 'C': 12, 'D': 18}, x)
s = F(360, 9)  # 丙乙速度差（第二次追上相隔 9 分钟）
a_ = (F(9, 2) * s - 8 * s) / (3 - 8)  # 3a + 8(s-a) = 4.5 s ，a=甲乙速度差
O['2021ZJA-71'] = pick({'A': 48, 'B': 84, 'C': 108, 'D': 144}, 3 * a_)
# 2022JSA-58：乙早 15 分钟出发不休息；甲 6 km/h 走 30 休 15；途中(不含起终点)相遇恰 2 次，乙速度最大 -> 用时最少
def jia_traj():
    tr = Traj(0, 0).wait(15)   # 以乙出发为 0 时刻
    for k in range(3):
        tr.move_to(3 * (k + 1), F(1, 10))
        if k < 2: tr.wait(15)
    return tr
best = None
for mins in [75, 120, 135, 150]:
    u = F(9, mins); yi = Traj(0, 0).move_to(9, u); jia = jia_traj()
    inner = sorted(set(m['x'] for m in meetings(jia, yi) if 0 < m['x'] < 9 and m['t'] > 0))
    if len(inner) == 2 and best is None:
        best = mins
O['2022JSA-58'] = pick({'A': 75, 'B': 120, 'C': 135, 'D': 150}, best)
rr = F(2); assert 36 + 18 * rr == 2 * (12 + 12 * rr)
O['2023SC-50'] = pick({'A': 48, 'B': 60, 'C': 66, 'D': 72}, 36 + 18 * rr)
plan = F(100); v2 = F(3000, 50); vavg = F(6000, 40); vend = 2 * vavg - v2; acc = (vend - v2) / 40
last = (vend - acc * 10 + vend) / 2; ratio = last / plan
O['2024SC-50'] = 'A' if ratio < F(18, 10) else 'B' if ratio < 2 else 'C' if ratio <= F(22, 10) else 'D'
vw, vl = F(8), F(6); Stot = 24 * (F((12 + 6) * 10, 6))   # 王:李=4:3 赋值 8、6；王到顶时李剩 6S，(12+6)×10=6S
O['2024SD-56'] = pick({'A': 30, 'B': 40, 'C': 50, 'D': 60}, (Stot / vl + Stot / 9) - (Stot / vw + Stot / 12))
syn = 1 / (1 - F(1, 12)) * F(36525, 100)
d = datetime.date(2024, 12, 8) + datetime.timedelta(days=round(syn))
O['2026CQ-58'] = 'B' if (d.year == 2026 and d.month <= 3) else '?'

data = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tasks_in/M04.json'))
official = {q['id']: q['answer_official'] for q in data['real']}
bad = [k for k, v in O.items() if v != official.get(k)]
print('自解:', {k: v for k, v in R.items()})
print('官方答案复算:', len(O), '道；不一致:', bad)
print('木星下次冲日（模型）:', d)
has_off = [q['id'] for q in data['real'] if q['answer_official']]
print('有官方答案但未复算:', sorted(set(has_off) - set(O)))
