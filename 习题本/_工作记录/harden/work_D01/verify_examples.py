from fractions import Fraction as F
from itertools import product

out = []
def chk(name, cond, info=""):
    out.append(("OK " if cond else "BAD") + " " + name + " " + str(info))

# VB1: two independent hypothetical transfers, total constant
A, B = 105, 75
chk("VB1 jia->yi 45 => yi=2*jia", (B + 45) == 2 * (A - 45), (A - 45, B + 45))
chk("VB1 yi->jia 30 => jia=3*yi", (A + 30) == 3 * (B - 30), (A + 30, B - 30))
# uniqueness: solve jia-45 = T/3, jia+30 = 3T/4
T = F(75) / (F(3, 4) - F(1, 3))
chk("VB1 total", T == 180, T)
# wrong path: sequential application
sols = []
for a in range(0, 400):
    for b in range(0, 400):
        a1, b1 = a - 45, b + 45
        if b1 != 2 * a1:
            continue
        a2, b2 = a1 + 30, b1 - 30
        if a2 == 3 * b2:
            sols.append((a, b))
chk("VB1 sequential-misread has integer sol?", True, sols[:3])

# VB2: four days, given max-min, case analysis
def days(x):
    return [x, F(3, 2) * x, F(5, 2) * x - 15, 2 * x - 5]
good = []
for x in range(1, 200):
    d = days(x)
    if any(v.denominator != 1 for v in map(F, d)) or min(d) <= 0:
        continue
    if max(d) - min(d) == 21:
        good.append((x, [int(v) for v in d], int(sum(d))))
chk("VB2 unique x with max-min=21", len(good) == 1, good)
x = 26
d = days(x)
chk("VB2 trap x=26 (assume day4 max): total", True, (int(sum(d)), [int(v) for v in d]))

# VC1
T = 360
a, b, c = 120, 90, 150
chk("VC1", a * 2 == b + c and b * 3 == a + c and c - a == 30 and a + b + c == T)

# VC2
Bud = 650
chk("VC2", F(4, 10) * Bud - 50 == F(35, 100) * (Bud - 50), (F(4, 10) * Bud, Bud - 50))
chk("VC2 trap", F(5, 100) * 1000 == 50)

# VM2: two units, unequal sizes, two layers
jia_m, jia_f, yi_m, yi_f = 45, 15, 20, 20
chk("VM2 merged 13:7", F(jia_m + yi_m, jia_f + yi_f) == F(13, 7))
pj_m, pj_f, py_m, py_f = F(jia_m, 3), F(jia_f * 2, 5), F(yi_m, 4), F(yi_f, 2)
chk("VM2 party ints", all(v.denominator == 1 for v in (pj_m, pj_f, py_m, py_f)), (pj_m, pj_f, py_m, py_f))
chk("VM2 party ratio", F(pj_m + py_m, pj_f + py_f) == F(5, 4), F(pj_m + py_m, pj_f + py_f))
# wrong: equal sizes 40/40
e_m = F(30, 3) + F(20, 4)
e_f = F(10 * 2, 5) + F(20, 2)
chk("VM2 equal-size trap ratio", True, F(e_m, e_f))

# VN: quantities 12 -> 15 -> 18 same money, second cut 0.4 yuan
p0 = F(3)
M = 12 * p0
p1 = M / 15
p2 = M / 18
chk("VN", p1 - p2 == F(2, 5), (p0, p1, p2, M))

# VD2: capital x months, 30% retained
w_jia = 30 * 12
w_yi = 50 * 4 + 30 * 8
w_bing = 40 * 5
P = F(21) / (F(7, 10) * F(w_bing, w_jia + w_yi + w_bing))
chk("VD2 weights/profit", (w_jia, w_yi, w_bing) == (360, 440, 200) and P == 150, P)

# VE1
k = 6
jia0, yi0 = 25 * k, 15 * k
x = k
jia1, yi1 = jia0 - x, yi0 + x
chk("VE1 step1 3:2", F(jia1, yi1) == F(3, 2), (jia1, yi1))
y = 2 * k
chk("VE1 step2 4:3", F(jia1, yi1 + y) == F(4, 3), (jia1, yi1 + y, y, jia0 + yi0))

# VL1 tongbi/huanbi
s24_9 = F(100)
s24_10 = s24_9 * F(3, 2)
s25_10 = s24_10 * F(11, 10)
s25_9 = s25_10 / F(5, 4)
chk("VL1", s25_9 / s24_9 - 1 == F(32, 100), s25_9)

# VF2: average standard
n = 45
m, f = 30, 15
chk("VF2", 6 * n + 45 == 8 * m + 5 * f, (6 * n + 45, 8 * m + 5 * f))
# trap simple average 6.5
chk("VF2 trap 90", 6 * 90 + 45 == F(13, 2) * 90)

# VF1: 'not full' inequality
sol = [nn for nn in range(1, 100) if 8 * (nn - 1) < 5 * nn + 22 < 8 * nn]
chk("VF1 rooms", sol == [8, 9], (sol, [5 * nn + 22 for nn in sol]))

# VG2 rotation numeric
nn = 20
jia, yi, bing = nn, nn - 3, nn + 6
avg = F(jia + yi + bing, 3)
g_yi = 6
g_jia = g_yi + 4
g_bing = g_jia + 1
chk("VG2", jia - g_jia + g_bing == avg and yi - g_yi + g_jia == avg and bing - g_bing + g_yi == avg, (avg, g_jia, g_yi, g_bing))

# VH1 equal sales -> inverse ratio -> pack
sols = []
for a_ in range(0, 201):
    for b_ in range(0, 201 - a_):
        c_ = 200 - a_ - b_
        if 60 * a_ == 40 * b_ and 60 * a_ + 40 * b_ + 50 * c_ == 9800:
            sols.append((a_, b_, c_))
chk("VH1 unique", sols == [(40, 60, 100)], sols)

# VI2 homogeneous
from fractions import Fraction
# 4(3B+5S) = 3(5B+2S) -> 3B = 14S
Bg, Sm = 14, 3
tot = 4 * (3 * Bg + 5 * Sm)
chk("VI2", tot == 3 * (5 * Bg + 2 * Sm), (tot, F(tot, 4 * Bg)))

# VI1 coefficient matching
pa, pb, pc = 6, 3, 2
S1 = 4 * pa + 7 * pb + pc
S2 = 5 * pa + 9 * pb + pc
chk("VI1", 4 * S1 - 3 * S2 == pa + pb + pc, (S1, S2, 4 * S1 - 3 * S2))
# check independence of individual prices: another price set with same S1,S2
alt = []
for qa, qb in product(range(0, 20), range(0, 20)):
    qc = S1 - 4 * qa - 7 * qb
    if qc >= 0 and 5 * qa + 9 * qb + qc == S2:
        alt.append((qa, qb, qc, qa + qb + qc))
chk("VI1 multiple price sets same total", len(alt) > 1 and len(set(t[3] for t in alt)) == 1, alt[:4])

# VK1 ride-share by segment
seg = [30, 30, 30]
jia_p = F(seg[0], 3)
yi_p = F(seg[0], 3) + F(seg[1], 2)
bing_p = F(seg[0], 3) + F(seg[1], 2) + seg[2]
chk("VK1", (jia_p, yi_p, bing_p) == (10, 25, 55) and jia_p + yi_p + bing_p == 90)

# VK2 head-count change
sol = []
for nn in range(3, 100):
    for TT in range(1, 5000):
        if F(TT, nn) - F(TT, nn + 2) == 30 and F(TT, nn - 2) - F(TT, nn) == 50:
            sol.append((nn, TT))
chk("VK2", sol == [(8, 1200)], sol)

for line in out:
    print(line)
