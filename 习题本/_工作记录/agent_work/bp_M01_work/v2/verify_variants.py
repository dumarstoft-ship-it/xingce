"""M01 blueprint: independent numeric check of every planned variant.
Each check recomputes the answer from the stem data (brute force where uniqueness matters)
and asserts that exactly one of the planned options equals it.
Run: python3 verify_variants.py   (prints one line per variant, FAIL lines if any)"""
from fractions import Fraction as F
import math, itertools

RES = {}
def check(vid, value, options, answer, tol=None, note=''):
    """options: list; answer: the option we plan as correct. value: computed truth."""
    def eq(a, b):
        if isinstance(a, str) or isinstance(b, str):
            return a == b
        if tol is None:
            return F(a) == F(b) if not isinstance(a, float) and not isinstance(b, float) else abs(a - b) < 1e-9
        return abs(float(a) - float(b)) <= tol
    hits = [o for o in options if eq(o, value)]
    ok = (len(hits) == 1 and hits[0] == answer and len(set(map(str, options))) == 4)
    RES[vid] = ok
    print(f"{'OK  ' if ok else 'FAIL'} {vid:8s} value={value!s:>14s} answer={answer!s:>10s} options={options} {note}")

def solve_unique(pred, space):
    s = [x for x in space if pred(x)]
    return s

# ======================= DAY 1 =======================
# 1-1-1 carbon reverse
monthly = F(54000, 12)
diesel = (monthly - 1500 * F(6, 10) - 200 * 2) / F(5, 2)
check('1-1-1', diesel, [1280, 1800, 3200, 15360], 1280,
      note=f'dist: {monthly/F(5,2)}, {monthly-900-400}, {diesel*12}')
# 1-1-2 volunteer points: holiday 10h x10x1.5 ; >300 half ; credited 340 -> weekday hours
def credited(h_week, h_hol=10):
    raw = 10 * h_week + 15 * h_hol
    return raw if raw <= 300 else 300 + F(raw - 300, 2)
sol = [h for h in range(0, 100) if credited(h) == 340]
check('1-1-2', sol[0], [17, 19, 23, 28], 23, note=f'unique={len(sol)==1}')
# 1-2-1 renovated is 37.5% less than not-renovated; not - done = 54 -> total
x = F(54) / (1 - F(5, 8)); done = x * F(5, 8)
check('1-2-1', x + done, [144, 198, 234, 342], 234, note=f'not={x} done={done}; reversed-base total={54/F(3,8)+54/F(3,8)*F(11,8)}')
# 1-2-2 two-stage sales
def _two_stage(b):
    jia = F(3, 2) * b                 # 甲库存是乙的1.5倍
    jia1, yi1 = jia * F(6, 10), F(b) * F(1, 2)   # 第一天甲卖出40%、乙卖出一半
    return jia1 - 60 == 2 * (yi1 - 60)   # 第二天各卖60件后甲剩余是乙剩余的2倍
sol = [b for b in range(1, 5000) if _two_stage(b)]
b = sol[0]; check('1-2-2', b + F(3, 2) * b, [375, 600, 900, 1500], 1500, note=f'yi={b} jia={F(3,2)*b} unique={len(sol)==1}')
# 1-2-3 four cities: GZ=1.2SZ=1.5FS=2DG ; SZ-DG=160
sol = []
for A in range(1, 5000):
    B = F(A) / F(6, 5); C = F(A) / F(3, 2); D = F(A, 2)
    if B - D == 160: sol.append((A, B, C, D))
A, B, C, D = sol[0]
check('1-2-3', A + B + C + D, [960, 1200, 1440, 2880], 1440, note=f'{sol}')
# 1-3-1 percentage points
wind = F(35, 100); pv = wind + F(10, 100); st = 1 - wind - pv
check('1-3-1', F(300) / (pv - st), [1000, 1200, 1500, 2500], 1200,
      note=f'pp-misread: {F(300)/((wind*F(11,10))-(1-wind-wind*F(11,10)))}')
# 1-3-2 three disbursements
sol = []
for T in range(1, 2000):
    r1 = T - (F(T, 3) - 20); r2 = r1 - (F(3, 5) * r1 + 6)
    if r2 == 50: sol.append(T)
check('1-3-2', sol[0], [135, 180, 210, 240], 180, note=f'unique={len(sol)==1}')
# 1-4-1 job fairs
sol = []
for n1 in range(1, 50):
    n2 = 50 - n1
    for t1 in range(1, 881):
        t2 = 880 - t1
        if F(t2) == F(6, 5) * t1 and F(t2, n2) == F(4, 5) * F(t1, n1): sol.append((n1, n2, t1, t2))
n1, n2, t1, t2 = sol[0]
check('1-4-1', F(t2, n2), [16, F(88, 5), 20, 24], 16, note=f'{sol}')
# 1-4-2 trucks
cnt = [8, 12, 15]; load = [5, 3, 2]; trips = [2, 3, 4]
units = [c * l * t for c, l, t in zip(cnt, load, trips)]
per = F(180, units[2])
check('1-4-2', per * sum(units), [336, 420, 462, 636], 462, note=f'units={units}')
# 1-5-1 party:non-party
sol = [(k, 4 * k) for k in range(1, 200) if 2 * (k + 10) == 4 * k - 2]
k = sol[0][0]; check('1-5-1', k + 10, [11, 21, 42, 63], 21, note=f'{sol}')
# 1-5-2 grids 3:5:8 ; equal additions ; A:B=2:3 ; C->A 12 -> A=B ; ask C now
sol = []
for kk in range(1, 100):
    for d in range(1, 200):
        A, B, C = 3 * kk + d, 5 * kk + d, 8 * kk + d
        if 3 * A == 2 * B and A + 12 == B: sol.append((kk, d, C - 12))
check('1-5-2', sol[0][2], [42, 48, 54, 66], 42, note=f'{sol}')
# 1-6-1 grain
check('1-7-1', F(280) / (F(8, 10) * F(7, 10)), [350, 400, 500, 560], 500)
# 1-6-2 overlapping windows
first25 = 25 * F(60, 100); last25 = 25 * F(72, 100); overlap = 8
check('1-7-2', (first25 + last25 - overlap) / 40, [F(425, 1000), F(625, 1000), F(66, 100), F(825, 1000)], F(625, 1000))
# 1-7-1 heat packs
sol = [(n, 6 * n + 50) for n in range(1, 100) if 6 * n + 50 == 8 * n + 10]
n, T = sol[0]
check('1-9-1', T // 5 - n, [10, 14, 20, 34], 14, note=f'n={n} T={T} T%5={T%5}')
# 1-7-2 buses
sol = [(n, 45 * n + 30) for n in range(2, 100) if 45 * n + 30 == 50 * (n - 1)]
check('1-9-2', sol[0][1], [720, 750, 800, 830], 750, note=f'{sol}')
# 1-8-1 transfer
sol = [m for m in range(1, 3600) if any((y + m) - (y + 840 - m) == 160 for y in [1000])]
check('1-10-1', sol[0], [340, 500, 680, 1000], 500, note=f'{sol}')
# 1-8-2 half plus ten, three times, 15 left
sol = []
for T in range(1, 2000):
    r = F(T)
    for _ in range(3):
        r = r - (r / 2 + 10)
    if r == 15: sol.append(T)
check('1-10-2', sol[0], [120, 190, 240, 260], 260, note=f'unique={len(sol)==1}')
# 1-9-1 points mall: 3 cups = 5 umbrellas ; 2 umbrellas = 3 calendars ; budget 18 cups ; spend 6 cups + 5 umbrellas
u = F(6); c = F(5, 3) * u; t = F(2, 3) * u
rem = 18 * c - 6 * c - 5 * u
check('1-11-1', math.floor(rem / t), [10, 22, 23, 45], 22, note=f'exact={rem/t}')
# 1-10-1 two purchases
sol = [(p, q) for p in range(1, 400) for q in range(1, 400) if 3 * p + 2 * q == 620 and 2 * p + 3 * q == 680]
check('1-12-1', sum(sol[0]), [100, 160, 260, 300], 260, note=f'{sol}')
# 1-11-1 volunteers: total 80, women 35, jia men - yi women = 9 -> jia total (check all decompositions)
vals = set()
for am in range(0, 81):
    for af in range(0, 36):
        bf = 35 - af
        if am - bf != 9: continue
        bm = 80 - 35 - am
        if bm < 0: continue
        vals.add(am + af)
check('1-13-1', vals.pop() if len(vals) == 1 else ('MULTI', vals), [35, 36, 44, 45], 44)
# 1-12-1 AA trip
tot = 1260 + 780 + 420; avg = F(tot, 4)
check('1-15-1', 1260 - avg, [440, 480, 615, 645], 645, note=f'avg={avg} 3-person={1260-F(tot,3)}')
# 1-12-2 rice money
each = F(8, 3); price = F(48) / each
check('1-15-2', (5 - each) * price, [30, 36, 42, 45], 42, note=f'yi gets {(3-each)*price}')

# ======================= DAY 15 =======================
# 15-1-1 heart-rate interval -> age
def ok_age(a):
    lo = (220 - a) * F(6, 10); hi = (220 - a) * F(8, 10)
    return lo <= 117 and 126 <= hi
opts = [22, 58, 64, 68]
hits = [a for a in opts if ok_age(a)]
check('15-1-1', hits[0] if len(hits) == 1 else ('MULTI', hits), opts, 58,
      note=f'valid ages={[a for a in range(1,120) if ok_age(a)][0]}..{[a for a in range(1,120) if ok_age(a)][-1]}')
# 15-1-2 carbon points with caps
def day_points(steps=12500, metro=3, km=4):
    walk = min((max(steps - 6000, 0)) // 1000, 10)
    met = min(metro * 2, 4)
    return walk + met + F(km, 2)
check('15-1-2', 7 * day_points(), [84, 91, 98, 112], 84)
# 15-2-1 buses
sol = []
for E in range(1, 2601):
    for H in range(1, 2601 - E):
        M = 2600 - E - H
        if M > 0 and E - (H + M) == 200 and 2 * H == M: sol.append((E, H, M))
E, H, M = sol[0]
check('15-2-1', F(E, H), [F(7, 4), F(5, 2), 3, F(7, 2)], F(7, 2), note=f'{sol}')
# 15-2-2 five days, max-min=30 -> first three days total (x real, all values integer)
sol = []
for x4 in range(1, 2000):
    x = F(x4, 4)
    d = [x, F(5, 4) * x, x + F(5, 4) * x - 30, F(7, 4) * x, F(7, 4) * x - 15]
    if min(d) <= 0: continue
    if max(d) - min(d) == 30 and all(v.denominator == 1 for v in d): sol.append((x, d))
check('15-2-2', sum(sol[0][1][:3]), [120, 150, 180, 210], 150, note=f'n_sol={len(sol)} {sol}')
# 15-3-1 compression
sol = [T for T in range(1, 2000) if T - F(3, 10) * F(2, 10) * T == 470]
T = sol[0]; check('15-3-1', F(3, 10) * F(2, 10) * T, [F(282, 10), 30, 94, 141], 30, note=f'T={T}')
# 15-3-2 lychee/longan/wampee
sol = []
for li in range(1, 2000):
    lo = F(4, 3) * li; wa = lo * F(5, 6)
    if 12 * li + 8 * lo + 6 * wa == 13200: sol.append((li, lo, wa))
li, lo, wa = sol[0]
check('15-3-2', lo - wa, [50, 100, 150, 200], 100, note=f'{sol}')
# 15-4-1 per-capita multiple
cnt = [1, 4, 10]; tot = [3, 4, 2]
pc = [F(t, c) for t, c in zip(tot, cnt)]
check('15-4-1', pc[0] / pc[2], [F(3, 2), 10, 15, 20], 15)
# 15-4-2 elder care staffing
sol = []
for z in range(0, 201, 2):
    y = z + 10
    x = 200 - y - z
    if x < 0 or x % 10 or y % 5: continue
    if x // 10 + y // 5 + z // 2 == 41: sol.append((x, y, z))
check('15-4-2', sol[0][2], [20, 30, 40, 50], 40, note=f'{sol}')
# 15-5-1 men 3x women ; remove 2t men add t women ; men = 1.5 women ; diff 60
sol = []
for w in range(1, 500):
    for t in range(1, 500):
        m = 3 * w
        if 2 * (m - 2 * t) == 3 * (w + t) and (m - 2 * t) - (w + t) == 60: sol.append((w, t, 4 * w))
check('15-5-1', sol[0][2], [300, 336, 360, 420], 336, note=f'{sol}')
# 15-5-2 bus depots 5:4:3:2
sol = []
for kk in range(1, 100):
    for a in range(1, 5 * kk):
        J, Y, B, D = 5 * kk - a, 4 * kk + 10, 3 * kk + a, 2 * kk - 10
        if D > 0 and J == Y and 2 * B == 5 * D: sol.append((kk, a, 5 * kk))
check('15-5-2', sol[0][2], [60, 70, 75, 80], 75, note=f'{sol}')
# 15-6-1 school merger
sol = []
for A in range(5, 3000, 5):
    for Bn in range(4, 3000, 4):
        if A - Bn != 300: continue
        mA, mB = F(3, 5) * A, F(1, 4) * Bn
        if mA + mB == (A + Bn) - (mA + mB): sol.append((A, Bn, mA + mB))
check('15-6-1', sol[0][2], [245, 300, 350, 420], 350, note=f'{sol}')
# 15-6-2 two classes in range
sol = []
for a in range(1, 30):
    for b in range(1, 30):
        if 3 * a + 4 * b == 2 * a + 5 * b and 80 <= 5 * a + 9 * b <= 95: sol.append((a, b, 5 * a))
check('15-6-2', sol[0][2], [25, 30, 35, 54], 30, note=f'{sol}')
# 15-7-1 percentage points
g = F(44, 100) * F(11, 10) / F(40, 100) - 1
check('15-7-1', g, [F(10, 100), F(14, 100), F(144, 1000), F(21, 100)], F(21, 100))
# 15-7-2 reservoir
check('15-7-2', F(18, 10) / (F(8, 10) * F(5, 4) * F(9, 10)), [F(162, 100), F(189, 100), 2, F(225, 100)], 2,
      note=f'additive-misread={F(18,10)/F(95,100)}')
# 15-8-1 share change
check('15-8-1', F(30, 100) * F(14, 10) / F(112, 100), [F(336, 1000), F(375, 1000), F(42, 100), F(58, 100)], F(375, 1000))
# 15-8-2 two counties
sol = []
for a in range(1, 1000):
    for b in range(1, 1000):
        if F(108, 100) * a == 270 and F(108, 100) * a + F(115, 100) * b == F(11, 10) * (a + b): sol.append((a, b))
check('15-8-2', F(115, 100) * sol[0][1], [100, 108, 115, 135], 115, note=f'{sol}')
# 15-9-1 books: 5 each +20 ; boys 6 girls 4 exact ; boys:girls 3:2
sol = [n for n in range(5, 1000, 5) if 5 * n + 20 == 6 * F(3, 5) * n + 4 * F(2, 5) * n]
check('15-9-1', sol[0], [80, 100, 104, 520], 100, note=f'{sol}')
# 15-10-1 groups: +6, -3, x1.5, -1/3 ; max-min of originals = 25 -> original total
sol = []
for E in range(1, 400):
    g = [F(E - 6), F(E + 3), F(E) / F(3, 2), F(E) / F(2, 3)]
    if min(g) <= 0 or any(v.denominator != 1 for v in g): continue
    if max(g) - min(g) == 25: sol.append((E, g, sum(g)))
check('15-10-1', sol[0][2], [115, 120, 122, 128], 122, note=f'{sol}  removed={sol[0][2]-4*sol[0][0]}')
# 15-10-2 three communities doubling chain, final 32 each
sol = []
for a in range(1, 96):
    for b in range(1, 96 - a):
        c = 96 - a - b
        x, y, z = a, b, c
        x, y, z = x - y - z, 2 * y, 2 * z
        if x < 0: continue
        y, x, z = y - x - z, 2 * x, 2 * z
        if y < 0: continue
        z, x, y = z - x - y, 2 * x, 2 * y
        if z < 0: continue
        if (x, y, z) == (32, 32, 32): sol.append((a, b, c))
check('15-10-2', sol[0][0], [32, 44, 52, 56], 52, note=f'{sol}')
# 15-11-1 tanks
sol = [(L, S) for L in range(1, 100) for S in range(1, 100) if 3 * L + 2 * S == 120 and 2 * L + 3 * S == 105]
L, S = sol[0]
check('15-12-1', (200 - 4 * L) // S, [4, 5, 6, 8], 5, note=f'L={L} S={S} exact={F(200-4*L, S)}')
# 15-11-2 three goods, A amount = B amount
sol = []
for a in range(1, 151):
    for b in range(1, 151 - a):
        c = 150 - a - b
        if c > 0 and 36 * a == 30 * b and 36 * a + 30 * b + 24 * c == 4560: sol.append((a, b, c))
check('15-12-2', sol[0][2], [30, 40, 50, 60], 40, note=f'{sol}')
# 15-12-1 excluding-one averages
ex = {'甲': 62, '乙': 60, '丙': 58, '丁': 64}
sums = {k: 3 * v for k, v in ex.items()}
tot = F(sum(sums.values()), 3)
ind = {k: tot - s for k, s in sums.items()}
check('15-13-1', ind['甲'], [52, 58, 62, 64], 58, note=f'{ind}')
# 15-13-1 partnership: dividends 30:20 = capital ratio ; yi adds 60 -> equal
sol = [(3 * m, 2 * m) for m in range(1, 1000) if 2 * m + 60 == 3 * m]
check('15-14-1', sol[0][0], [120, 150, 180, 240], 180, note=f'{sol}')
# 15-14-1 cold store: rent 3000 by 5:3:2 ; power 900 equal ; jia paid all -> yi owes
yi = F(3000) * F(3, 10) + F(900, 3)
check('15-15-1', yi, [1170, 1200, 1270, 1300], 1200, note=f'swap-rules={F(3000,3)+900*F(3,10)}')
# 15-14-2 elevator: 54 wan, floors 2-6 coef 1..5, 2 households each, prepaid 3
unit = F(54) / (2 * sum(range(1, 6)))
check('15-15-2', 5 * unit - 3, [F(24, 10), 6, 9, 15], 6, note=f'unit={unit}')

if __name__ == '__main__' and False:
    pass

# ======================= DAY 29 =======================
# 29-1-1 desalination: 1 m3 sea -> 0.45 fresh + 0.55 brine ; brine - fresh = 1802 -> fresh range
sea = F(1802) / F(10, 100); fresh = sea * F(45, 100)
def rng(v):
    return 'A' if v < 8000 else 'B' if v < 8100 else 'C' if v <= 8200 else 'D'
check('29-1-1', rng(fresh), ['A', 'B', 'C', 'D'], 'C', note=f'fresh={fresh} (approx-1800 gives {F(1800)/F(10,100)*F(45,100)})')
# 29-1-2 honey biscuits: 15 g each, 3% honey ; density 1.4 g/mL ; 1.5 L ; boxes of 20 (full boxes)
honey_g = 1500 * F(14, 10); per = 15 * F(3, 100); biscuits = math.floor(honey_g / per)
check('29-1-2', biscuits // 20, [119, 166, 233, 234], 233, note=f'biscuits={honey_g/per}')
# 29-2-1 trucks: 8 big ; +12 small -> +75% ; third trip = 2x first ; all 8 big used -> small needed
big_in_small = F(12) / (F(75, 100) * 8)   # 1 big = 2 small
need_small = (2 * 8 * big_in_small) - 8 * big_in_small
check('29-2-1', need_small, [8, 12, 16, 20], 16, note=f'1 big = {big_in_small} small')
# 29-3-1 survey: paper 1/4 (valid 3/4), online 3/4 (valid 5/6) ; online valid - paper valid = 420
sol = [N for N in range(4, 5000, 4) if (F(3, 4) * N * F(5, 6)) - (F(1, 4) * N * F(3, 4)) == 420]
check('29-3-1', sol[0], [840, 960, 1050, 1680], 960, note=f'{sol}')
# 29-3-2 two people: jia-60 = yi/2 ; yi-60 = 2/3 jia
sol = [(j, y) for j in range(61, 1000) for y in range(61, 1000) if 2 * (j - 60) == y and 3 * (y - 60) == 2 * j]
check('29-3-2', sum(sol[0]), [195, 270, 285, 300], 285, note=f'{sol}')
# 29-4-1 badminton: 18 courts ; doubles people = 2 x singles people ; boys singles 10, doubles 30
sol = []
for s in range(0, 19):
    d = 18 - s
    if 4 * d == 2 * (2 * s):
        boys = 10 + 30; girls = (2 * s - 10) + (4 * d - 30)
        sol.append((s, d, boys - girls))
check('29-4-1', sol[0][2], [20, 22, 26, 28], 26, note=f'{sol}')
# 29-4-2 two price cuts: first -20% -> +15 units ; second -> +25 more units ; second cut %
n = F(15) / (F(1) / F(8, 10) - 1); n1 = n + 15; n2 = n1 + 25
cut2 = 1 - n1 / n2
check('29-4-2', cut2, [F(20, 100), F(25, 100), F(1, 3), F(40, 100)], F(25, 100), note=f'n={n}')
# 29-5-1 ice reverse: small loses 1/3 ; big loses 3x small's loss ; after big = 12 x small -> before ratio
sol = []
for s in range(3, 300, 3):
    for Bv in range(1, 5000):
        loss_s = F(s, 3); loss_b = 3 * loss_s
        if Bv - loss_b == 12 * (s - loss_s): sol.append(F(Bv, s))
check('29-5-1', sol[0] if len(set(sol)) == 1 else ('MULTI', set(sol)), [8, 9, 12, 13], 9)
# 29-5-2 balls 3:5 ; +4 red -> 1:1 ; P(two red)
sol = [k for k in range(1, 100) if 3 * k + 4 == 5 * k]
k = sol[0]; red, white = 3 * k + 4, 5 * k
p = F(math.comb(red, 2), math.comb(red + white, 2))
check('29-5-2', p, [F(9, 38), F(1, 4), F(9, 19), F(1, 2)], F(9, 38), note=f'red={red} white={white}')
# 29-6-1 exam: applicants 900 (4:5) ; passed m:f 1:2 ; failed 5:4
sol = []
for pm in range(0, 401):
    pf = 2 * pm
    fm, ff = 400 - pm, 500 - pf
    if ff > 0 and 4 * fm == 5 * ff: sol.append(pm + pf)
check('29-6-1', sol[0], [300, 360, 450, 540], 450, note=f'{sol}')
# 29-6-2 three layers (redesigned): depts equal size ; jia m:f 3:2 ; yi 1:4 ; party rate men 25%, women 40%
jm, jf, ym, yf = F(3), F(2), F(1), F(4)
party = F(25, 100) * (jm + ym) + F(40, 100) * (jf + yf)
share = party / 10
check('29-6-2', share, [F(31, 100), F(325, 1000), F(34, 100), F(37, 100)], F(34, 100),
      note=f'simple-avg={F(65,200)} jia-ratio={F(3,5)*F(25,100)+F(2,5)*F(40,100)} yi-ratio={F(1,5)*F(25,100)+F(4,5)*F(40,100)}')
# 29-7-1 two streets: 1/3 and 1/4 out (jia out - yi out = 6) ; then 1/2 and 1/3 of remaining ; second round total 30
sol = [(x, y) for x in range(3, 600, 3) for y in range(4, 600, 4)
       if F(x, 3) - F(y, 4) == 6 and F(1, 2) * (x - F(x, 3)) + F(1, 3) * (y - F(y, 4)) == 30]
x, y = sol[0]
check('29-7-1', '多6人' if x - y == 6 else str(x - y), ['少6人', '多6人', '少12人', '多12人'], '多6人', note=f'{sol}')
# 29-7-2 scenic spot: 2025-10 mom +25%, yoy +10% ; 2024-10 = 1.5 x 2024-09 -> 2025-09 yoy
s2409 = F(100); s2410 = s2409 * F(3, 2); s2510 = s2410 * F(11, 10); s2509 = s2510 / F(5, 4)
check('29-7-2', s2509 / s2409 - 1, [F(15, 100), F(22, 100), F(32, 100), F(35, 100)], F(32, 100))
# 29-8-1 three firms: A +100 ; B -25% and B25 = A25/2 ; C +40% and C24 = A24+B24 ; total +20% -> C share 2025 (approx)
sol = []
for a in range(1, 5000):
    A25 = a + 100; B25 = F(A25, 2); B24 = B25 / F(3, 4); C24 = a + B24; C25 = C24 * F(7, 5)
    if A25 + B25 + C25 == F(6, 5) * (a + B24 + C24): sol.append((a, B24, C24, A25, B25, C25))
a, B24, C24, A25, B25, C25 = sol[0]
share = C25 / (A25 + B25 + C25)
opts = [F(50, 100), F(54, 100), F(58, 100), F(62, 100)]
nearest = min(opts, key=lambda o: abs(o - share))
check('29-8-1', nearest, opts, F(58, 100), note=f'{sol} share={float(share):.4f} (2024 share={float(C24/(a+B24+C24)):.3f})')
# 29-8-2 per-capita income +8%, population -4% -> total income growth
check('29-8-2', F(108, 100) * F(96, 100) - 1, [F(368, 10000), F(4, 100), F(432, 10000), F(125, 1000)], F(368, 10000))
# 29-9-1 disinfectant: 5 each +10 left ; +25% -> 6 each +20 left ; +6 shops, 7 each -> min extra bottles
sol = [(n, 5 * n + 10) for n in range(1, 300) if F(5, 4) * (5 * n + 10) == 6 * n + 20]
n, T = sol[0]
check('29-9-1', (n + 6) * 7 - T, [50, 52, 92, 100], 92, note=f'n={n} T={T}')
# 29-9-2 segmented distribution: 8 each -> short 30 ; first 10 get 10, rest 6 -> 12 left
sol = [n for n in range(11, 500) if 8 * n - 30 == 10 * 10 + 6 * (n - 10) + 12]
check('29-9-2', sol[0], [29, 35, 41, 44], 41, note=f'{sol}')
# 29-10-1 three warehouses 180 ; ops ; final 2:3:4
def ops3(a, b, c):
    a, b = a - b, 2 * b
    b, c = b - c, 2 * c
    c, a = c - a, 2 * a
    return a, b, c
sol = [(a, b, 180 - a - b) for a in range(1, 180) for b in range(1, 180 - a) if ops3(a, b, 180 - a - b) == (40, 60, 80)]
check('29-10-1', sol[0][0], [50, 55, 75, 90], 75, note=f'{sol}')
# 29-10-2 rotation numeric: A=B+2, C=A+2 ; teams rotate A->B->C->A ; equal ; B team 9 -> A team
hits = set()
for Bn in range(9, 60):
    A_, C_ = Bn + 2, Bn + 4
    avg = F(A_ + Bn + C_, 3)
    b = 9
    for a in range(0, A_ + 1):
        for c in range(0, C_ + 1):
            if A_ - a + c == avg and Bn - b + a == avg and C_ - c + b == avg: hits.add(a)
check('29-10-2', hits.pop() if len(hits) == 1 else ('MULTI', hits), [7, 9, 11, 13], 11)
# 29-11-1 Macau: 2781 MOP ; 1 HKD = 1.03 MOP ; 100 CNY = 108 HKD ; fee 1% of CNY exchanged
cny = F(2781) / F(103, 100) / F(108, 100)
check('29-11-1', cny * F(101, 100), [2475, 2500, 2525, 2550], 2525, note=f'cny before fee={cny}')
# 29-12-1 servers: power 1,2,4 ; year1 N=220 ; year2 A/2, B same, C x2 same power ; year3 A=0, B x2 (of year2), C same as year2, same power
sol = []
for z in range(1, 220):
    for y in range(1, 220 - z):
        x = 220 - y - z
        if x <= 0 or x % 2: continue
        P1 = x + 2 * y + 4 * z
        P2 = x // 2 + 2 * y + 8 * z
        P3 = 0 + 4 * y + 8 * z
        if P1 == P2 == P3: sol.append((x, y, z))
check('29-12-1', sol[0][1] if len(sol) == 1 else ('MULTI', sol), [20, 40, 80, 160], 40, note=f'{sol}')
# 29-12-2 three-day records
import numpy as np
A_ = np.array([[3, 2, 1], [1, 3, 2], [2, 1, 3]], dtype=float); bvec = np.array([52, 38, 42], dtype=float)
pv = np.linalg.solve(A_, bvec)
check('29-12-2', round(float(pv.sum()), 9), [20, 22, 24, 26], 22, note=f'prices={pv}')
# 29-13-1 four windows: A+B=176, C+D=164, A+C=174, B-D=4
sol = [(a, b, c, d) for a in range(0, 101) for b in range(0, 101) for c in range(0, 101) for d in [b - 4]
       if a + b == 176 and c + d == 164 and a + c == 174]
check('29-13-1', sol[0][0] if len(sol) == 1 else ('MULTI', sol), [85, 87, 88, 91], 91, note=f'{sol}')
# 29-13-2 averages: A+B = 2C+2 ; D = E-6 ; (A+B)/2 = (C+D+E)/3 + 2 -> compare (A+B)/2 with E (symbolic via 2 random E values)
outs = set()
for E in [F(80), F(91, 2)]:
    D = E - 6
    # unknowns C and S=A+B : S = 2C+2 ; S/2 = (C+D+E)/3 + 2
    # -> C+1 = (C+D+E)/3 + 2 -> 3C+3 = C+D+E+6 -> C = (D+E+3)/2
    C = (D + E + 3) / 2; S = 2 * C + 2
    outs.add(S / 2 - E)
v = outs.pop() if len(outs) == 1 else None
check('29-13-2', '低0.5分' if v == F(-1, 2) else str(v), ['高0.5分', '低0.5分', '高1.5分', '低1.5分'], '低0.5分')
# 29-14-1 dilution: 20% -> 16% after I ; second 3I -> 12% ; V2(pre2)/post1 - 1
I = F(1)
V1 = [v for v in [F(i, 2) for i in range(1, 200)] if F(20, 100) * v / (v + I) == F(16, 100)][0]
post1 = V1 + I
V2 = [v for v in [F(i, 2) for i in range(1, 400)] if F(16, 100) * v / (v + 3 * I) == F(12, 100)][0]
check('29-14-1', V2 / post1 - 1, [F(50, 100), F(80, 100), F(125, 100), F(180, 100)], F(80, 100), note=f'V1={V1} post1={post1} V2={V2}')
# 29-14-2 cooperative: 2000 shares (400 cash) ; 500k x 80% ; cash share guarantee 20 first ; zhang 6 land + 4 cash
dist = F(500000) * F(8, 10); per = (dist - 400 * 20) / 2000
check('29-14-2', 10 * per + 4 * 20, [1960, 2000, 2040, 2500], 2040, note=f'per share={per}')
# 29-15-1 homestay: 1200/night, 3 nights ; A,B,C 3 nights ; D first 2 ; E first 1
nights = [{'甲', '乙', '丙', '丁', '戊'}, {'甲', '乙', '丙', '丁'}, {'甲', '乙', '丙'}]
s1 = sum(F(1200, len(nt)) for nt in nights if '甲' in nt)
pn = sum(len(nt) for nt in nights); s2 = F(3600, pn) * 3
check('29-15-1', s1 - s2, [20, 40, 60, 220], 40, note=f'scheme1={s1} scheme2={s2}')
# 29-15-2 ride share segments 0-10 (jia), 10-20 (jia,yi), 20-30 (all) ; fare 90 evenly per km
seg = [(30, ['甲']), (30, ['甲', '乙']), (30, ['甲', '乙', '丙'])]
jia = sum(F(f, len(p)) for f, p in seg if '甲' in p)
check('29-15-2', jia, [30, 45, 55, 60], 55)

# ======================= DAY 39 =======================
# 39-1-1 talent subsidy by month: 2023-03 .. 2026-02 (36 months) ; master until 2024-10, doctor from 2024-11
months = [(2023 + (2 + i) // 12, (2 + i) % 12 + 1) for i in range(36)]
tot = sum(800 if (y, m) <= (2024, 10) else 1500 for y, m in months)
check('39-1-1', tot, [39300, 40000, 40700, 54000], 40000, note=f'first={months[0]} last={months[-1]}')
# 39-1-2 PV -> trees
trees = 120000 * F(15, 100) * 1100 * F(8, 10) / 20
check('39-1-2', trees / 10000, [F(792, 100), F(792, 10), 99, 792], F(792, 10))
# 39-2-1 photos: verify unique via brute force
sol = set()
T = 38
for s in range(1, T):
    h = 2 * s + 2
    if s + h != T: continue
    fam = F(h, 2); pairs = h - fam
    for fm in range(0, int(pairs) + 1):
        for fc in range(0, int(pairs) - fm + 1):
            mc = pairs - fm - fc
            cg, dg, mg = fam + fc + mc, fam + fm + fc, fam + fm + mc
            if cg != dg or dg != mg + 4: continue
            for cs in range(0, s + 1):
                for ds in range(0, s - cs + 1):
                    ms = s - cs - ds
                    if cs == ds + ms and ds == 2 * ms: sol.add(mg + ms)
check('39-2-1', sol.pop() if len(sol) == 1 else ('MULTI', sol), [19, 21, 27, 29], 21)
# 39-2-2 three branches: A=2B-4, C>=A, A+B+C=86 -> max B
best = max(Bv for Bv in range(1, 87) if (2 * Bv - 4) >= 0 and 86 - (2 * Bv - 4) - Bv >= 2 * Bv - 4)
check('39-2-2', best, [16, 18, 19, 20], 18)
# 39-3-1 three payers: jia pays 60 -> left = 1/4 (others) ; yi pays 60 -> 2/5 ; bing pays 60*0.8 -> 1/3
sol = []
for Tt in range(200, 1500):
    x = F(60 + F(1, 4) * Tt, F(5, 4)); y = F(60 + F(2, 5) * Tt, F(7, 5)); z = F(48 + F(1, 3) * Tt, F(4, 3))
    if x + y + z == Tt: sol.append((Tt, x, y, z))
check('39-3-1', sol[0][2], [144, 156, 180, 192], 180, note=f'{sol}')
# 39-3-2 applicants N in [500,600], 3/8 fresh ; pass 2/5 of fresh, 4/7 of others ; all counts integer
sol = []
for N in range(500, 601):
    fr = F(3, 8) * N; ot = N - fr
    p = F(2, 5) * fr + F(4, 7) * ot
    if fr.denominator == 1 and (F(2, 5) * fr).denominator == 1 and (F(4, 7) * ot).denominator == 1: sol.append((N, p))
check('39-3-2', sol[0][1] if len(sol) == 1 else ('MULTI', sol), [280, 284, 290, 296], 284, note=f'{sol}')
# 39-4-1 two workshops: people 3:2, per-capita 4:5 ; jia per-capita +25%, yi people +20% -> yi per-capita +? to equal
J = 3 * (4 * F(5, 4)); Y = (2 * F(6, 5)) * 5
check('39-4-1', J / Y - 1, [F(20, 100), F(25, 100), F(30, 100), F(50, 100)], F(25, 100), note=f'J={J} Y={Y}')
# 39-4-2 prizes: value shares 40/35/25 ; counts 1:5:20 ; P(value > average)
cnts = [1, 5, 20]; shares = [F(40), F(35), F(25)]
per = [s / c for s, c in zip(shares, cnts)]; avg = sum(shares) / sum(cnts)
p = F(sum(c for c, v in zip(cnts, per) if v > avg), sum(cnts))
check('39-4-2', p, [F(1, 26), F(3, 13), F(3, 4), F(10, 13)], F(3, 13), note=f'per={per} avg={avg}')
# 39-5-1 workshops efficiency: jia eff 1.2, capacity jia = 1.5 yi ; move 20 (keep efficiency) -> equal
sol = []
for n1 in range(21, 1000):
    for n2 in range(1, 1000):
        if F(12, 10) * n1 == F(3, 2) * n2 and F(12, 10) * (n1 - 20) == n2 + F(12, 10) * 20: sol.append((n1, n2))
check('39-5-1', sol[0][0], [96, 110, 120, 150], 120, note=f'{sol}')
# 39-5-2 ratio travel: speeds 3:2 ; after meeting jia -1/3, yi +1/4 ; when jia reaches B, yi 28 km from A
L = F(1)
meet_from_A = L * F(3, 5)
vj, vy = F(3) * F(2, 3), F(2) * F(5, 4)
t = (L - meet_from_A) / vj
yi_left = meet_from_A - vy * t
check('39-5-2', F(28) / yi_left, [140, 240, 280, 350], 280)
# 39-6-1 two layers: jia m:f 3:1, yi 1:1, merged 2:1 ; party m:f 5:1 and 2:1 ; yi female-party share = 3x jia's ; female party total 15
sol = []
for a in range(1, 50):
    for b in range(1, 50):
        if (3 * a + b) != 2 * (a + b): continue
        Nj, Ny = 4 * a, 2 * b
        for t_ in range(1, 50):
            for s_ in range(1, 50):
                if F(s_, Ny) == 3 * F(t_, Nj) and t_ + s_ == 15 and 5 * t_ <= 3 * a and t_ <= a and 2 * s_ <= b and s_ <= b:
                    sol.append((a, b, t_, s_, 5 * t_ + 2 * s_))
vals = set(x[4] for x in sol)
check('39-6-1', vals.pop() if len(vals) == 1 else ('MULTI', vals), [36, 45, 48, 60], 48, note=f'example={sol[:2]}')
# 39-6-2 conditional probability
g1, g2 = F(4, 9), F(5, 9); f1, f2 = F(1, 2), F(3, 5)
check('39-6-2', g2 * f2 / (g1 * f1 + g2 * f2), [F(2, 5), F(5, 9), F(3, 5), F(2, 3)], F(3, 5))
# 39-7-1 budget adjustment
Bt = F(100); staff, pub, proj = 50, 30, 20
cut = F(pub) * F(20, 100); proj2 = proj + cut / 2; total2 = Bt - cut / 2
share = proj2 / total2
opts = [F(230, 1000), F(237, 1000), F(245, 1000), F(260, 1000)]
check('39-7-1', min(opts, key=lambda o: abs(o - share)), opts, F(237, 1000), note=f'share={float(share):.4f}')
# 39-7-2 export share change (percentage points)
ex, im = F(4800), F(3200); ex2, im2 = ex * F(11, 10), im * F(95, 100)
pp = (ex2 / (ex2 + im2) - ex / (ex + im)) * 100
opts = [F(25, 10), F(35, 10), 6, 15]
check('39-7-2', min(opts, key=lambda o: abs(o - pp)), opts, F(35, 10), note=f'pp={float(pp):.3f}')
# 39-8-1 H1 share of last year's expense: H1 -20%, H2 -15%, total -17%
sol = [F(h1, 100) for h1 in range(1, 100) if F(h1) * F(80, 100) + F(100 - h1) * F(85, 100) == F(83)]
check('39-8-1', sol[0], [F(40, 100), F(50, 100), F(60, 100), F(2, 3)], F(40, 100))
# 39-8-2 five sessions [35,49,56,90,120]
sol = []
for s1 in range(1, 500):
    s2 = F(s1) * F(14, 10); s3 = s2 / F(875, 1000)
    back = F(3, 2) * (s1 + s2 + s3); s4 = back / (1 + F(4, 3)); s5 = s4 * F(4, 3)
    if s5 - s3 == 64: sol.append((s1, s2, s3, s4, s5))
s1, s2, s3, s4, s5 = sol[0]
d = s4 - s1
rngs = ['不到50万元', '50~60万元', '60~70万元', '70万元以上']
lab = rngs[0] if d < 50 else rngs[1] if d < 60 else rngs[2] if d < 70 else rngs[3]
check('39-8-2', lab, rngs, '50~60万元', note=f'{sol} s4-s1={d}')
# 39-8-3 other industries growth: NEV base share 20%, growth 15% ; total growth 6%
other = (F(6, 100) - F(20, 100) * F(15, 100)) / F(80, 100)
check('39-8-3', other, [F(3, 100), F(375, 10000), F(4, 100), F(48, 1000)], F(375, 10000))
# 39-9-1 two goods with two ratio plans -> minimal purchase
sol = [n for n in range(1, 200) if (8 * n - 6 - 6 * n) - (5 * n - 3 - 4 * n) == 18]
n = sol[0]; Mk, Ek = 8 * n - 6, 5 * n - 3
best = None
for rm, re in [(3, 2), (4, 3)]:
    for kk in range(1, 100):
        if rm * kk * n >= Mk and re * kk * n >= Ek:
            buy = rm * kk * n - Mk + re * kk * n - Ek
            best = buy if best is None else min(best, buy); break
check('39-9-1', best, [24, 30, 51, 54], 30, note=f'n={n} M={Mk} E={Ek}')
# 39-9-2 rooms: 3 per room -> 10 without room ; 4 per room -> 3 rooms empty and one room not full (>=1)
opts = [76, 80, 82, 88]
def feasible(P):
    for r in range(1, 200):
        if 3 * r + 10 != P: continue
        used = r - 3
        if used <= 0: continue
        full = P // 4; rem = P - 4 * full
        if full == used - 1 and 1 <= rem <= 3: return True
    return False
hits = [o for o in opts if feasible(o)]
check('39-9-2', hits[0] if len(hits) == 1 else ('MULTI', hits), opts, 82, note=f'all feasible={[P for P in range(1,300) if feasible(P)]}')
# 39-10-1 four companies rotation symbolic: B=n, A=n+2, C=n+5, D=n+1 ; A->B->C->D->A
rel = set()
for n_ in range(3, 30):
    A_, B_, C_, D_ = n_ + 2, n_, n_ + 5, n_ + 1
    avg = F(A_ + B_ + C_ + D_, 4)
    for b in range(0, B_ + 1):
        for a in range(0, A_ + 1):
            for c in range(0, C_ + 1):
                for d in range(0, D_ + 1):
                    if A_ - a + d == avg and B_ - b + a == avg and C_ - c + b == avg and D_ - d + c == avg:
                        rel.add(c - b)
check('39-10-1', 'x+3' if rel == {3} else str(rel), ['x+1', 'x+2', 'x+3', 'x+5'], 'x+3')
# 39-10-2 600 boxes: jia gives 1/4 of own to yi ; yi gives 1/3 of current to bing ; final 3:4:5
sol = []
for a in range(4, 600, 4):
    for b in range(0, 600 - a):
        c = 600 - a - b
        a1, b1 = a - a // 4, b + a // 4
        if b1 % 3: continue
        b2, c2 = b1 - b1 // 3, c + b1 // 3
        if 4 * a1 == 3 * b2 and 5 * b2 == 4 * c2: sol.append((a, b, c))
check('39-10-2', sol[0][1], [150, 200, 250, 300], 250, note=f'{sol}')
# 39-11-1 points: 1 oil = 3 rice ; 2 rice = 5 tissue ; budget = 6 oil ; each >=1 ; exact ; max items
best = 0
for o in range(1, 7):
    for r in range(1, 19):
        rem = F(90) - 15 * o - 5 * r
        if rem >= 2 and (rem / 2).denominator == 1:
            best = max(best, o + r + int(rem / 2))
check('39-11-1', best, [35, 37, 41, 45], 37)
# 39-11-2 two exchange routes for 5000 CNY
r1 = 5000 * F(108, 100) * F(103, 100); r2 = 5000 * F(99, 100) * F(110, 100)
check('39-11-2', r1 - r2, [55, 62, 117, 150], 117, note=f'route1={r1} route2={r2}')
# 39-12-1 homogeneous system: 3A+2B=4C ; A+C=2B ; total 2100
sol = [(a, b, 2100 - a - b) for a in range(1, 2100) for b in range(1, 2100 - a)
       if 3 * a + 2 * b == 4 * (2100 - a - b) and a + (2100 - a - b) == 2 * b]
check('39-12-1', sol[0][1], [600, 700, 800, 1050], 700, note=f'{sol}')
# 39-12-2 3 pens+7 notebooks+1 folder=31.5 ; 4+10+1=42 -> 1+1+1 (check invariant over solutions)
vals = set()
for p10 in range(1, 200):
    p = F(p10, 10)
    nb = (F(105, 10) - p) / 3
    f = F(315, 10) - 3 * p - 7 * nb
    if nb > 0 and f > 0: vals.add(p + nb + f)
check('39-12-2', vals.pop() if len(vals) == 1 else ('MULTI', vals), [10, F(21, 2), 11, 12], F(21, 2))
# 39-13-1 samples: total 70, valid 50 ; jia valid - yi invalid = 14 ; jia invalid = yi valid / 3 -> jia total
sol = []
for av in range(0, 71):
    for ai in range(0, 71):
        for bv in range(0, 71):
            bi = 70 - av - ai - bv
            if bi < 0: continue
            if av + bv == 50 and av - bi == 14 and 3 * ai == bv: sol.append(av + ai)
check('39-13-1', set(sol).pop() if len(set(sol)) == 1 else ('MULTI', set(sol)), [30, 34, 36, 40], 34, note=f'{len(sol)} decompositions')
# 39-13-2 judges: drop max&min avg 9.2 ; drop max avg 9.0 ; drop min avg 9.3 -> max score
# unknowns S,H,L
from fractions import Fraction as Fr
H = None
for S10 in range(400, 500):
    S = Fr(S10, 10)
    Hh = S - 36; Ll = S - Fr(372, 10)
    if S - Hh - Ll == Fr(276, 10): H = Hh; L_ = Ll; SS = S
check('39-13-2', H, [F(94, 10), F(96, 10), F(98, 10), 10], F(96, 10), note=f'S={SS} L={L_}')
# 39-14-1 operation converted to capital: jia 400, yi 100 + x ; 4:3 -> x ; year2 yi +100 -> yi share
x = [v for v in range(1, 1000) if F(400, 100 + v) == F(4, 3)][0]
check('39-14-1', F(200 + x, 400 + 200 + x), [F(1, 3), F(3, 7), F(1, 2), F(3, 5)], F(1, 2), note=f'x={x}')
# 39-14-2 profit: capital 3:2:1 ; 30% retained ; bing gets 21 ; net margin 15%
prof = F(21) * 6 / F(7, 10)
check('39-14-2', prof / F(15, 100), [840, 1000, 1200, 2800], 1200, note=f'profit={prof}')
# 39-15-1 minibus: 6 originally ; 2 join paying half share ; each original saves 10
sol = [Tt for Tt in range(1, 3000) if F(Tt, 6) - F(Tt, 7) == 10]
check('39-15-1', sol[0], [240, 360, 420, 480], 420, note=f'{sol}')
# 39-15-2 dinner: n people ; 2 fewer -> +20 each ; 4 more -> -20 each
sol = [(n_, Tt) for n_ in range(3, 100) for Tt in range(1, 5000)
       if F(Tt, n_ - 2) - F(Tt, n_) == 20 and F(Tt, n_) - F(Tt, n_ + 4) == 20]
check('39-15-2', sol[0][0], [6, 8, 10, 12], 8, note=f'{sol}')

bad = [k for k, v in RES.items() if not v]
print('\nTOTAL', len(RES), 'FAIL', len(bad), bad)
