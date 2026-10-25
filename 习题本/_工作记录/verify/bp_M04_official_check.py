# -*- coding: utf-8 -*-
"""M04：对有官方答案的真题逐题独立复算，核对官方答案（用于"官方答案存疑"排查）。"""
from fractions import Fraction as F
import math, json, sys

def pick(opts, val, tol=1e-6):
    hits = [k for k, v in opts.items() if abs(float(v) - float(val)) < tol]
    return hits[0] if len(hits) == 1 else ("?", val, hits)

def solve_lin(f, lo, hi, it=200):
    """单调函数二分求根"""
    flo = f(lo)
    for _ in range(it):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0):
            lo = m
        else:
            hi = m
    return (lo + hi) / 2

R = {}
# 2022HB-70 环形：直径两端出发同向，甲10min/圈，乙12min/圈
L = 1.0; R["2022HB-70"] = pick({"A":30,"B":60,"C":15,"D":45}, (L/2)/(L/10 - L/12))
# 2023SD-43 三角形 v-t：20km/20min
R["2023SD-43"] = pick({"A":100,"B":108,"C":116,"D":120}, 20*2/(20/60))
# 2024GK-66 甲1.2v 4h = 乙 v*1 + (v+30)*3
v = solve_lin(lambda v: 1.2*v*4 - (v + 3*(v+30)), 1, 1000)
R["2024GK-66"] = pick({"A":540,"B":510,"C":600,"D":570}, 1.2*v*4)
# 2024JSA-52 窗口看对面车 420m 3.6s
rel = 420/3.6*3.6  # m/s -> km/h
R["2024JSA-52"] = pick({"A":210,"B":240,"C":450,"D":630}, rel - 180)
# 2025GD-38 父子
k = 100/60; R["2025GD-38"] = pick({"A":35,"B":30,"C":25,"D":15}, 40*k/(k+1))
# 2025SC-55
vz = 150/2.5; tz = 135/vz; R["2025SC-55"] = pick({"A":75,"B":90,"C":108,"D":120}, 135/(tz-1))
# 2025SD-52  S/2/6 + S/2/3 + 0.25 = 2.5
S = solve_lin(lambda S: S/12 + S/6 + 0.25 - 2.5, 0.1, 100); R["2025SD-52"] = pick({"A":9,"B":10,"C":12,"D":13.5}, S)
# 2020HB-67 狗
R["2020HB-67"] = pick({"A":1100,"B":1000,"C":960,"D":880}, 80*(1200-100)/(40+60))
# 2020HB-73 往返：平路 a，坡 b：a/9*2 + b/6 + b/18 = 1；由于坡等距平均=9，往返=1h*9
# 用两个不同的 a 验证结果与 a 无关
outs=set()
for a in [0.5,1,2,3]:
    b = (1 - 2*a/9)/(1/6+1/18)
    outs.add(round(a+b,9))
R["2020HB-73"] = pick({"A":3.5,"B":4.5,"C":5.5,"D":6.5}, outs.pop()) if len(outs)==1 else "?"
# 2020JSA-58
jia_q = 500; jia_3q = 1500; yi_3q = 2400; S = (jia_3q+yi_3q)/0.75
fast, slow = (yi_3q, jia_3q)
R["2020JSA-58"] = pick({"A":1350,"B":1600,"C":1800,"D":1950}, S - S*slow/fast)
# 2020SD-36
R["2020SD-36"] = pick({"A":1.2,"B":1.5,"C":1.6,"D":2.0}, (2000+200+400*2)/2000)
# 2020SZS-27  小李 v，小王往返 30min 后 1.2v 追，在乙地(15km)追上
v = solve_lin(lambda v: (15/v) - (0.5 + 15/(1.2*v)), 0.5, 50); R["2020SZS-27"] = pick({"A":4,"B":4.5,"C":5,"D":6}, v)
# 2020ZJB-14  用多个 t 验证第二天速度与 t 无关
outs=set()
for t in [1,2,3.5]:
    s = (80*(7*t+5) - 400)/2
    outs.add(round(s/(4*t),9))
R["2020ZJB-14"] = pick({"A":70,"B":75,"C":80,"D":85}, outs.pop()) if len(outs)==1 else "?"
# 2021JSA-54
x = solve_lin(lambda x: (x+10)*120 - 100*x - 2800, 1, 1000); R["2021JSA-54"] = pick({"A":4.2,"B":4.5,"C":4.8,"D":5.4}, (x+10)*60/1000)
# 2021SC2-47
v = 1.0  # 原速时间 T0：1.2 倍速省 10 分 => T0 = 60 min
T0 = solve_lin(lambda T: T - T/1.2 - 10, 1, 1000)
vv = solve_lin(lambda v: (2/v + (v*T0/60 - 2)/(1.3*v))*60 - (T0-10), 2.01, 100)
R["2021SC2-47"] = pick({"A":5.4,"B":7.2,"C":8.5,"D":9.6}, vv*T0/60)
# 2021ZJA-62  AB:BC=3:4
AB, BC = 3, 4
v = (AB + BC/2)/150
back = BC/(2*v) + AB/(v*(1-1/3))
R["2021ZJA-62"] = pick({"A":165,"B":170,"C":190,"D":195}, back)
# 2021ZJA-72
inc = math.sqrt(160**2-80**2)/60
R["2021ZJA-72"] = pick({"A":math.sqrt(2),"B":math.sqrt(3),"C":4*math.sqrt(3)/3,"D":2*(math.sqrt(3)-1)}, inc)
# 2022GK-65 前25%从15匀加速到21（时间上均匀），其余21；前半程比后半程多3分钟
S = solve_lin(lambda S: ((S/4)/18 + (S/4)/21) - (S/2)/21 - 3/60, 0.1, 1000)
R["2022GK-65"] = "D" if S > 25 else ("C" if S > 24 else ("B" if S > 23 else "A"))
# 2022GK-68  枚举整数速度
ans=None
for a in range(1,20):
    for b in range(1,20):
        if abs(b-0.6*a)>1e-9: continue
        d1 = math.hypot(17-a, 8-b); d4 = math.hypot(17-4*a, 8-4*b)
        if abs(d1-13)<1e-9 and abs(d4-5)<1e-9 and 4*a>=17 and 4*b>=8:
            diff = (17/a - 8/b)*60
            ans = "D" if diff>10 else ("C" if diff>0 else ("B" if diff<-10 else "A"))
R["2022GK-68"] = ans
# 2022SC2-50 甲:乙逆流=200:120；甲顺=1.8甲逆
ve, vy = 5.0, 3.0; vd = 1.8*ve
t = solve_lin(lambda t: (900 - vd*(t - 900/ve)) - vy*t, 900/ve, 900/vy)
R["2022SC2-50"] = pick({"A":270,"B":390,"C":510,"D":630}, vy*t)
# 2023GD-38 三段，蛙跳与竞走等距
outs=set()
for frog in [0.3,0.6,0.9]:
    t_walk = frog*2/6; t_swim = 2 - frog - t_walk
    outs.add(round(2*frog*2 + 3*t_swim,9))
R["2023GD-38"] = pick({"B":6,"C":8,"D":12}, outs.pop()) if len(outs)==1 else "A"
# 2023GK-72 甲初速 u=1，乙 2；甲匀加速 a；2h 时甲路程=乙路程
a = solve_lin(lambda a: (1*2 + 0.5*a*4) - 2*2, 0, 10)
SB = 1*3 + 0.5*a*9; tB = SB/2
R["2023GK-72"] = pick({"A":11.5,"B":11.75,"C":12,"D":12.25}, 8 + tB)
# 2023JSA-58
vy=1; vj=3; tY=4000/vy; ride = (4000-400)/vj
R["2023JSA-58"] = pick({"A":3000,"B":2800,"C":2400,"D":2000}, (tY-ride)*vy)
# 2023SD-36  以 5:30 为 0 点；母亲照常 (30-T) 出发，单程 T 分钟；车速 c、步速 w
# 相遇时刻 t 满足 w*t + c*(t-30+T) = c*T；到家时刻 2t-30+T；比往常(30+T)早 10 分钟
outs=set()
for T in [20.0, 30.0, 45.0]:
    def g(t):  # 早到分钟数 - 10
        return (30+T) - (2*t - 30 + T) - 10
    t = solve_lin(g, 0.0, 30.0)
    cw = t/(30-t)  # 由 t(w+c)=30c 反推 c/w，检验可行(>1)
    assert cw > 1
    outs.add(round(t,6))
R["2023SD-36"] = pick({"A":20,"B":25,"C":15,"D":10}, outs.pop()) if len(outs)==1 else ("?",outs)
# 2023ZJA-59
v_up, v_down = 4, 6; seg_up = 15; tt = seg_up/v_up; seg_down = v_down*tt
total = seg_up + seg_down  # 以 1.31km 为单位
per = math.floor(total + 1e-9) + 1   # 0,1,...,floor(total) 处各采一份
R["2023ZJA-59"] = pick({"A":38,"B":39,"C":76,"D":78}, 2*per)
# 2023ZJA-67
AC = 320*3/4; CB = 320 - AC; CD = CB/3; BD = math.hypot(CB, CD)
R["2023ZJA-67"] = "A" if BD<80 else ("B" if BD<90 else ("C" if BD<100 else "D"))
# 2024GD-44
v = solve_lin(lambda v: (v + 500)*2 - 2*v*1.5, 1, 100000)  # 上山速度 v（米/时）
R["2024GD-44"] = pick({"A":2000,"B":3000,"C":3600,"D":4000}, v + 2*v*1)
# 2024HB-75
r = solve_lin(lambda r: (2*3*r)/5 - 4*(2*3*(r+50))/30, 1, 10000)
R["2024HB-75"] = pick({"A":2,"B":3,"C":4,"D":6}, 3*r*r/10000)
# 2024SD-60
x = math.sqrt(900/7); R["2024SD-60"] = pick({"A":26,"B":28,"C":30,"D":34}, round(3*x))
# 2024SZ-56
v = 180/6/1  # (6v-5v)*6=180
R["2024SZ-56"] = pick({"A":6,"B":7.2,"C":9,"D":10.8}, 5*v*60/1000)
# 2024ZJA-61
t = solve_lin(lambda t: (120 + t + 12) - 5*t, 0, 1000)
R["2024ZJA-61"] = pick({"A":165,"B":175,"C":185,"D":195}, 120 + t + 12 + 20)
# 2025GK-68
L = 3*(1+2); jia_half = L/2
R["2025GK-68"] = pick({"A":2+10/60,"B":2.25,"C":2+20/60,"D":2.5}, jia_half/2)
# 2025GK-74
n = 120/2; v = solve_lin(lambda v: n/v - (math.sqrt(3)*n)/(2*math.sqrt(3)*v) - 3, 0.1, 1000)
R["2025GK-74"] = pick({"A":10,"B":15,"C":10*math.sqrt(3),"D":15*math.sqrt(3)}, v)
# 2025JSA-60  枚举 x
outs=set()
for x in [1.0, 2.0, 3.7]:
    y = solve_lin(lambda y: (1/x + 2/y) - (1/(1.2*x) + 2/(0.8*y)), 0.01, 1000)
    outs.add(round((1.2*x)/(0.8*y),9))
R["2025JSA-60"] = pick({"A":1/3,"B":2/5,"C":5/12,"D":1/2}, outs.pop()) if len(outs)==1 else "?"
# 2025ZJA-61
v = solve_lin(lambda v: (v/2*10/60 + 13.5) - v*20/60, 1, 1000)
R["2025ZJA-61"] = pick({"A":54,"B":63,"C":72,"D":81}, v)
# 2020SZ1-48
v = solve_lin(lambda v: 30*(0.5 + 10/v) - (2*v - 10), 10.5, 100)
R["2020SZ1-48"] = pick({"A":20,"B":18,"C":16,"D":15}, v)
# 2020SZS-16
x = solve_lin(lambda x: (18-x)/8 + x/4 - 3, 0, 18)
R["2020SZS-16"] = pick({"A":4,"B":6,"C":12,"D":18}, x)
# 2021ZJA-71
# d1=3a, d1+d2=4.5*(a+b), d2=8*b, a+b=360/9
s = 360/9
a = solve_lin(lambda a: 3*a + 8*(s-a) - 4.5*s, 0, s)
R["2021ZJA-71"] = pick({"A":48,"B":84,"C":108,"D":144}, 3*a)
# 2022JSA-58：二分最大速度，使途中(不含起终点)相遇恰 2 次
def jia_pos(t):  # 分钟，甲 0 时刻出发
    if t <= 0: return 0.0
    cyc = 45.0; k = int(t//cyc); r = t - k*cyc
    pos = 3*k + (min(r,30)/30)*3
    return min(pos, 9.0)
def meetings(u):  # 乙速度 km/min，提前 15 分钟出发；数"位置相同"的区间段数（不含起终点）
    cnt=0; prev=None; N=200000; T=9/u - 15
    for i in range(1, N):
        t = -15 + (T+15)*i/N
        d = u*(t+15) - jia_pos(t)
        s = 0 if abs(d)<1e-9 else (1 if d>0 else -1)
        x = u*(t+15)
        if prev is not None and s != prev and 0 < x < 9:
            cnt += 1
        prev = s if s!=0 else prev
    return cnt
best=None
for mins in [75,120,135,150]:
    u = 9/mins
    # 用更稳健的判定：在 (0,9) 内乙的直线与甲阶梯函数的"交点/接触点"个数
    pts=set()
    for kk in range(0,4):
        # 甲行走段 [45kk, 45kk+30] 位置 3kk + (t-45kk)/10
        # 解 u(t+15) = 3kk + (t-45kk)/10
        if abs(u-0.1)>1e-12:
            t=(3*kk - 4.5*kk - 15*u)/(u-0.1)
            if 45*kk-1e-9<=t<=45*kk+30+1e-9:
                x=u*(t+15)
                if 1e-9<x<9-1e-9: pts.add(round(x,6))
        # 甲休息段 [45kk+30, 45kk+45] 位置 3kk+3
        t=(3*kk+3)/u - 15
        if 45*kk+30-1e-9<=t<=45*kk+45+1e-9:
            x=3*kk+3
            if 1e-9<x<9-1e-9: pts.add(round(x,6))
    if len(pts)==2 and best is None:
        best=mins
R["2022JSA-58"] = pick({"A":75,"B":120,"C":135,"D":150}, best) if best else "?"
# 2023SC-50  甲 2w，乙 w；N = 36 + u*18/w；N/2 = 12 + u*12/w
r = solve_lin(lambda r: (36 + 18*r) - 2*(12 + 12*r), 0, 100)
R["2023SC-50"] = pick({"A":48,"B":60,"C":66,"D":72}, 36 + 18*r)
# 2024SC-50
plan=100; S=12000; s1=3000; s2=3000; v2=s2/50; s3=S-s1-s2; vavg=s3/40; vend=2*vavg - v2
acc=(vend-v2)/40; last=(vend - acc*10 + vend)/2
ratio=last/plan
R["2024SC-50"] = "A" if ratio<1.8 else ("B" if ratio<2.0 else ("C" if ratio<=2.2 else "D"))
# 2024SD-56
vw, vl = 8, 6  # 小王:小李 = (1/2):(3/8)
Sx = solve_lin(lambda S: 24*S - (24*S*vl/vw) - (vw*1.5 + vl)*10, 0.01, 1000)
tot=24*Sx
R["2024SD-56"] = pick({"A":30,"B":40,"C":50,"D":60}, (tot/vl + tot/(vl*1.5)) - (tot/vw + tot/(vw*1.5)))
# 2026CQ-58
import datetime
syn = 1/(1 - 1/12)*365.25
d = datetime.date(2024,12,8) + datetime.timedelta(days=round(syn))
R["2026CQ-58"] = ("B" if (d.year==2026 and d.month<=3) else "?", str(d))

official = {q['id']: q['answer_official'] for q in json.load(open(sys.argv[1]))['real']}
bad=[]
for k,v in R.items():
    got = v[0] if isinstance(v, tuple) else v
    ok = (got == official.get(k))
    print(k, "计算:", v, "官方:", official.get(k), "OK" if ok else "<<< 不一致")
    if not ok: bad.append(k)
print("复核题数:", len(R), "不一致:", bad)
