# -*- coding: utf-8 -*-
"""Independent numeric verification of every M01 variant idea (v3).
For each variant the answer is recomputed from the stem data (brute force where uniqueness matters);
the script asserts that exactly one planned option matches and that it is the planned answer, and it
recomputes the error path claimed for each named distractor.  Run: python3 verify_v3.py"""
import os, re, sys, math, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan_days import DAYS

PLAN = {v['id']: v for d in DAYS for g in d['groups'] for v in g['variants']}
RES = {}

def parse(s):
    t = s.replace('$', '').replace(' ', '')
    m = re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}', t)
    if m: return F(int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'(\d+)/(\d+)', t)
    if m: return F(int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)%', t)
    if m: return F(m.group(1)) / 100
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)万', t)
    if m: return F(m.group(1)) * 10000
    m = re.fullmatch(r'-?\d+(?:\.\d+)?', t)
    if m: return F(t)
    return s

def close(a, b, tol):
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    return abs(F(a) - F(b)) <= tol

def check(vid, value, dist=None, tol=0, approx=None):
    """value: exact truth (number or option string). approx: if given, choose the option nearest to value
    and require distance <= approx while all others are farther than approx."""
    v = PLAN[vid]
    opts = v['opts']; vals = [parse(o) for o in opts]
    problems = []
    if len(set(opts)) != 4: problems.append('options not 4 distinct')
    if v['ans'] not in opts: problems.append('answer not among options')
    if approx is not None:
        hits = [o for o, x in zip(opts, vals) if not isinstance(x, str) and abs(F(x) - F(value)) <= approx]
    else:
        hits = [o for o, x in zip(opts, vals) if close(x, value, tol)]
    if len(hits) != 1: problems.append(f'hits={hits}')
    elif hits[0] != v['ans']: problems.append(f'computed {hits[0]} but planned {v["ans"]}')
    for o, dv in (dist or {}).items():
        if o not in opts: problems.append(f'distractor {o} not in options'); continue
        x = parse(o)
        tl = approx if approx is not None else tol
        if not close(x, dv, tl if tl else 0):
            problems.append(f'distractor {o} != error-path value {dv}')
        if o == v['ans']: problems.append(f'distractor {o} equals answer')
    RES[vid] = problems
    shown = value if isinstance(value, str) else (float(value) if F(value).denominator != 1 else int(value))
    print(('OK  ' if not problems else 'FAIL'), f'{vid:8s}', f'value={shown!s:>14s}', f'ans={v["ans"]}', '' if not problems else problems)

def uniq(xs):
    xs = list(dict.fromkeys(xs))
    assert len(xs) == 1, xs
    return xs[0]

# ============================== DAY 1 ==============================
# 1-1-1 learning hours
need = F(54, 12) - 1 * 2 - 2 * F(1, 2)
check('1-1-1', need * 45, {'202.5': F(54, 12) * 45, '112.5': (F(54, 12) - 2) * 45, '810': need * 45 * 12})
# 1-1-2 volunteer points with half above 300
def credited(raw): return raw if raw <= 300 else 300 + F(raw - 300, 2)
sol = uniq([h for h in range(0, 200) if credited(10 * h + 15 * 10) == 340])
check('1-1-2', sol, {'19': F(340 - 150, 10), '28': F(380 - 100, 10), '17': F(300 + F(40, 2) - 150, 10)})
# 1-2-1 renovated 37.5% less than not-renovated, difference 54
sol = uniq([(n, d) for n in range(1, 1000) for d in range(1, n) if F(d) == F(n) * F(5, 8) and n - d == 54])
mis = uniq([(n, d) for d in range(1, 1000) for n in range(d, 2000) if F(n) == F(d) * F(11, 8) and n - d == 54])
check('1-2-1', sum(sol), {'342': sum(mis), '198': mis[0], '144': sol[0]})
# 1-2-2 lychee/longan two weeks
b = uniq([b for b in range(1, 5000) if F(3, 2) * b * F(6, 10) - 60 == 2 * (F(b, 2) - 60)])
bm = uniq([b for b in range(1, 5000) if F(3, 2) * b * F(4, 10) - 60 == 2 * (F(b, 2) - 60)])
check('1-2-2', b + F(3, 2) * b, {'600': b, '900': F(3, 2) * b, '375': bm + F(3, 2) * bm})
# 1-2-3 four cities
sols = []
for gz in range(1, 10000):
    sz, fs, dg = F(gz) / F(6, 5), F(gz) / F(3, 2), F(gz, 2)
    if sz.denominator == fs.denominator == dg.denominator == 1 and sz - dg == 160: sols.append(gz + sz + fs + dg)
k_mis = F(160, 6); k_sf = F(160, 2)
check('1-2-3', uniq(sols), {'960': 36 * k_mis, '1200': 30 * 40, '2880': 36 * k_sf})
# 1-3-1 percentage points
edu = F(35, 100); med = edu + F(10, 100); old = 1 - edu - med
med_m = edu * F(11, 10); old_m = 1 - edu - med_m
check('1-3-1', F(300) / (med - old), {'2500': F(300) / (med_m - old_m), '1500': F(300) / old, '3000': F(300) / F(10, 100)})
# 1-3-2 three disbursements
def left(T, s1=-1, s2=+1):
    r1 = T - (F(T, 3) + s1 * 20); r2 = r1 - (F(3, 5) * r1 + s2 * 6); return r2
T = uniq([T for T in range(1, 3000) if left(T) == 50])
r1 = (F(50) + 6) / F(2, 5)
check('1-3-2', T, {'210': r1 / F(2, 3), '240': (r1 + 20) / F(2, 3), '135': ((F(50) - 6) / F(2, 5) - 20) / F(2, 3)})
# 1-4-1 clinic: total ratio 1.4, average ratio 0.7, 30 doctors, 480 visits
sols = [(n1, n2, t1, t2) for n1 in range(1, 30) for t1 in range(1, 480)
        for n2, t2 in [(30 - n1, 480 - t1)] if F(t2) == F(14, 10) * t1 and F(t2, n2) == F(7, 10) * F(t1, n1)]
n1, n2, t1, t2 = uniq(sols)
check('1-4-1', F(t2, n2), {'16': F(480, 30), '20': F(t1, n1), '28': F(t2, n1)})
# 1-4-2 trucks: counts 2:3 & 4:5 ; load 5:3:2 ; trips 2:3:4 ; small 180 t
cnt = [8, 12, 15]; load = [5, 3, 2]; trips = [2, 3, 4]
assert F(cnt[0], cnt[1]) == F(2, 3) and F(cnt[1], cnt[2]) == F(4, 5)
u = [c * l * t for c, l, t in zip(cnt, load, trips)]
def tot(w): return F(180, w[2]) * sum(w)
check('1-4-2', tot(u), {'636': tot([c * l for c, l in zip(cnt, load)]), '336': tot([c * t for c, t in zip(cnt, trips)]), '420': tot(cnt)})
# 1-5-1 dragon boat
x = uniq([x for x in range(11, 300) if F(x - 10, 2 * x + 2) == F(1, 4)])
check('1-5-1', x, {'11': x - 10, '42': 2 * x, '63': 3 * x})
# 1-5-2 grids
sols = []
for k in range(1, 100):
    for d in range(1, 300):
        A, B, C = 3 * k + d, 5 * k + d, 8 * k + d
        if 3 * A == 2 * B and A + 12 == B: sols.append((k, d, C))
k, d, C = uniq(sols)
check('1-5-2', C - 12, {'54': C, '48': 8 * k, '66': C + 12})
# 1-7-1 grain
T0 = uniq([T for T in range(1, 3000) if F(T) * F(9, 10) * F(6, 10) == 270])
check('1-7-1', T0, {'540': F(270) / F(1, 2), '450': F(270) / F(6, 10), '300': F(270) / F(9, 10)})
# 1-7-2 overlapping windows: 50 cases, first 30 at 60%, last 30 at 70%, cases 21-30 have 7 praised
a, b, ov = 30 * F(60, 100), 30 * F(70, 100), 7
assert a - ov <= 20 and b - ov <= 20 and a - ov >= 0 and b - ov >= 0
check('1-7-2', (a + b - ov) / 50, {'65%': (F(60, 100) + F(70, 100)) / 2, '78%': (a + b) / 50, '50%': (a + b - 2 * ov) / 50})
# 1-9-1 heat packs
n = uniq([n for n in range(1, 500) if 6 * n + 50 == 8 * n + 10]); Tt = 6 * n + 50; assert Tt % 5 == 0
check('1-9-1', Tt // 5 - n, {'20': n, '34': Tt // 5, '10': 50 // 5})
# 1-9-2 classrooms
n = uniq([n for n in range(2, 500) if 45 * n + 30 == 50 * (n - 1)])
check('1-9-2', 45 * n + 30, {'800': 50 * n, '720': 45 * n, '830': 50 * n + 30})
# 1-10-1 transfer with reversal
sols = []
for yi in range(1, 3600):
    jia = yi + 840
    if jia + yi != 3600: continue
    for m in range(1, jia):
        if (yi + m) - (jia - m) == 160: sols.append(m)
check('1-10-1', uniq(sols), {'1000': 840 + 160, '680': 840 - 160, '340': F(840 - 160, 2)})
# 1-10-2 half plus 10 three times
def remain(T, k=3):
    r = F(T)
    for _ in range(k): r = r - (r / 2 + 10)
    return r
T = uniq([T for T in range(1, 5000) if remain(T) == 15])
r = F(15)
for _ in range(3): r = r * 2 + 10
check('1-10-2', T, {'190': r, '120': (F(15 + 10) * 2 + 10) * 2, '240': ((F(15) + 10) * 2 + 10) * 2 * 2})
# 1-11-1 points mall
um = F(1); cup = F(5, 3) * um; cal = F(2, 3) * um
rem = 18 * cup - 6 * cup - 5 * um
check('1-11-1', math.floor(rem / cal), {'23': round(rem / cal + F(1, 1000)), '45': 18 * cup / cal, '10': math.floor(rem / F(3, 2))})
# 1-12-1 basketball/football
p, q = uniq([(p, q) for p in range(1, 400) for q in range(1, 400) if 3 * p + 2 * q == 620 and 2 * p + 3 * q == 680])
check('1-12-1', p + q, {'100': p, '160': q})
# 1-13-1 volunteers
vals = set()
for am in range(0, 81):
    for af in range(0, 36):
        bf = 35 - af; bm = 45 - am
        if bm >= 0 and am - bf == 9: vals.add(am + af)
jia = uniq(vals)
check('1-13-1', jia, {'36': 80 - jia, '45': 45, '35': 35})
# 1-15-1 AA
tot_ = 1260 + 780 + 420
check('1-15-1', 1260 - F(tot_, 4), {'615': F(tot_, 4), '440': 1260 - F(tot_, 3), '480': 1260 - 780})
# 1-15-2 rice money
each = F(8, 3); price = F(48) / each
check('1-15-2', (5 - each) * price, {'30': F(48 * 5, 8), '36': 2 * price})

# ============================== DAY 15 ==============================
# 15-1-1 BMI: weight 58..70 always within [18.5, 24)
def ok_h(h): return F(58) / (h * h) >= F(185, 10) and F(70) / (h * h) < 24
hs = [F(x, 100) for x in (165, 170, 175, 180)]
good = [h for h in hs if ok_h(h)]
check('15-1-1', uniq(good))
assert F(58) / F(170, 100) ** 2 >= F(185, 10) and not F(70) / F(170, 100) ** 2 < 24   # 1.70 passes only the light end
assert F(70) / F(180, 100) ** 2 < 24 and not F(58) / F(180, 100) ** 2 >= F(185, 10)   # 1.80 passes only the heavy end
# 15-1-2 carbon points
def day_pts(steps, rides, km, step_floor=True, metro_cap=True, from_zero=False):
    over = steps if from_zero else max(0, steps - 6000)
    s = (over // 1000) if step_floor else math.ceil(F(over, 1000))
    s = min(s, 10)
    m = rides * 2; m = min(m, 4) if metro_cap else m
    return s + m + F(km, 2)
check('15-1-2', 7 * day_pts(12500, 3, 4), {'91': 7 * day_pts(12500, 3, 4, step_floor=False), '98': 7 * day_pts(12500, 3, 4, metro_cap=False), '112': 7 * day_pts(12500, 3, 4, from_zero=True)})
# 15-2-1 talent apartments
sols = [(p, h, y) for h in range(1, 2600) for y in [2 * h] for p in [2600 - h - y] if p > 0 and p - (h + y) == 200]
p, h, y = uniq(sols)
check('15-2-1', F(p, h), {'2.5': F(p, h) - 1, '1.75': F(p, y), '3': F(h + y, h)})
# 15-2-2 five days, max-min = 30 (brute force over integer x)
def five(x): return [x, F(5, 4) * x, F(5, 4) * x + 10, F(7, 4) * x, F(7, 4) * x - 12]
sols = []
for x in range(4, 2000, 4):
    days = five(x)
    if all(F(dd).denominator == 1 and dd > 0 for dd in days) and max(days) - min(days) == 30: sols.append(tuple(days))
days = uniq(sols)
wrong = five(80)    # assumes day 3 is the maximum and day 1 the minimum: 0.25x + 10 = 30
check('15-2-2', sum(days[:3]), {'290': sum(wrong[:3]), '220': sum(days[:4]), '278': sum(days)})
# 15-3-1 afforestation
plan = uniq([P for P in range(1, 5000) if F(P) - F(P) * F(20, 100) * F(30, 100) == 470])
cut = F(plan) * F(6, 100)
check('15-3-1', cut, {'28.2': F(470) * F(6, 100), '94': F(470) * F(20, 100), '141': F(470) * F(30, 100)})
# 15-3-2 capture-recapture
N = F(120) * 150 / 6
check('15-3-2', N, {'2880': F(120) * 144 / 6, '3120': N + 120, '264': 120 + 150 - 6})
# 15-4-1 three souvenirs
sols = []
for k in range(1, 500):
    a_, b_, c_ = 9 * k, 12 * k, 10 * k
    if F(a_, b_) == F(3, 4) and F(b_, c_) == F(6, 5) and 120 * a_ + 80 * b_ + 60 * c_ == 132000: sols.append((a_, b_, c_))
a_, b_, c_ = uniq(sols)
check('15-4-1', b_ - c_, {'50': b_ // 12, '150': b_ - a_})
# 15-4-2 caregivers (250 residents)
sols = [z for z in range(0, 200) if (240 - 2 * z) >= 0 and (240 - 2 * z) % 10 == 0 and (z + 10) % 5 == 0 and z % 2 == 0
        and (240 - 2 * z) // 10 + (z + 10) // 5 + z // 2 == 41]
z = uniq(sols)
check('15-4-2', z, {'40': z + 10, '15': z // 2})
# 15-5-1 choir: final ratio 5:3, difference 60
sols = [(w, t) for w in range(1, 500) for t in range(1, 500) if (3 * w - 2 * t) * 3 == 5 * (w + t) and (3 * w - 2 * t) - (w + t) == 60]
w, t = uniq(sols)
check('15-5-1', 4 * w, {'240': (3 * w - 2 * t) + (w + t), '198': 3 * w, '120': 4 * 30})
# 15-5-2 tents 7:5:3:2
sols = [(k, x) for k in range(1, 200) for x in range(1, 7 * k) if 7 * k - x == 5 * k + 10 and 3 * k + x == 3 * (2 * k - 10)]
k, x = uniq(sols)
km = uniq([k for k in range(1, 200) if 3 * k + (2 * k) == 3 * (2 * k - 10)])
check('15-5-2', 7 * k, {'110': 7 * k - x, '100': 5 * k, '210': 7 * km})
# 15-6-1 two volunteer teams
sols = [(A, B) for B in range(4, 3000, 4) for A in [B + 300] if A % 5 == 0 and F(3, 5) * A + F(1, 4) * B == F(1, 2) * (A + B)]
A, B = uniq(sols)
check('15-6-1', F(3, 5) * A + F(1, 4) * B, {'245': F(3, 5) * B + F(1, 4) * A, '300': F(3, 5) * A, '420': F(3, 5) * (A + B)})
# 15-6-2 two tour groups
sols = [(a_, b_) for a_ in range(1, 30) for b_ in range(1, 30) if 3 * a_ + 4 * b_ == 2 * a_ + 5 * b_ and 80 <= 5 * a_ + 9 * b_ <= 95]
a_, b_ = uniq(sols)
check('15-6-2', 5 * a_, {'35': 35, '25': 25, '54': 9 * b_})
assert 14 * 7 > 95 and 14 * 5 < 80
# 15-7-1 graduates share +4 points
g24 = F(40); g25 = F(110) * F(44, 100)
check('15-7-1', g25 / g24 - 1, {'14.4%': F(104, 100) * F(110, 100) - 1, '14%': F(14, 100), '10%': F(10, 100)})
# 15-7-2 reservoir
orig = F(27, 10) / (F(3, 4) * F(4, 3) * F(9, 10))
check('15-7-2', orig, {'2.43': F(27, 10) * F(9, 10), '3.6': F(27, 10) / F(3, 4), '2.75': F(27, 10) / (1 - F(1, 4) + F(1, 3) - F(1, 10))}, approx=F(1, 100))
# 15-8-1 NEV share
check('15-8-1', F(30, 100) * F(14, 10) / F(112, 100), {'42%': F(42, 100), '58%': F(58, 100), '33.6%': F(30, 100) * F(112, 100)})
# 15-8-2 two counties
j24 = F(270) / F(108, 100)
y24 = uniq([y for y in range(1, 2000) if (j24 * F(108, 100) + y * F(115, 100)) == (j24 + y) * F(110, 100)])
check('15-8-2', y24 * F(115, 100), {'100': y24, '108': F(270) * F(2, 5)})
# 15-9-1 reading books
n = uniq([n for n in range(5, 2000, 5) if 5 * n + 20 == 6 * F(3, 5) * n + 4 * F(2, 5) * n])
check('15-9-1', n, {'520': 5 * n + 20, '104': F(5 * n + 20, 5)})
# 15-10-1 four window groups (brute force over final size x, original sizes must be integers)
sols = []
for x in range(1, 300):
    orig_ = [x - 6, x + 3, F(2 * x, 3), F(3 * x, 2)]
    if all(F(o).denominator == 1 and o > 0 for o in orig_) and max(orig_) - min(orig_) == 25 and sum(orig_) > 4 * x:
        sols.append((x, sum(orig_)))
x, total = uniq(sols)
check('15-10-1', total, {'120': 4 * x})
# 15-10-2 mutual doubling
sols = []
for A in range(1, 97):
    for B in range(1, 97 - A):
        C = 96 - A - B
        a_, b_, c_ = A, B, C
        a_, b_, c_ = a_ - b_ - c_, 2 * b_, 2 * c_
        b_, a_, c_ = b_ - a_ - c_, 2 * a_, 2 * c_
        c_, a_, b_ = c_ - a_ - b_, 2 * a_, 2 * b_
        if (a_, b_, c_) == (32, 32, 32): sols.append((A, B, C))
A, B, C = uniq(sols)
check('15-10-2', A, {'56': 56, '32': 32})
# 15-12-1 water barrels
L, Sm = uniq([(L, s) for L in range(1, 200) for s in range(1, 200) if 3 * L + 2 * s == 120 and 2 * L + 3 * s == 105])
check('15-12-1', (200 - 4 * L) // Sm, {'6': 200 // L, '8': 120 // Sm, '4': (200 - 4 * Sm) // L})
# 15-12-2 study tickets: prices 48/40/32, 150 tickets, 6080 yuan, equal sales of A and B
sols = [(a_, b_, 150 - a_ - b_) for a_ in range(0, 151) for b_ in range(0, 151 - a_)
        if 48 * a_ == 40 * b_ and 48 * a_ + 40 * b_ + 32 * (150 - a_ - b_) == 6080]
a_, b_, c_ = uniq(sols)
check('15-12-2', c_, {'50': a_, '60': b_})
# 15-13-1 leave-one-out averages
sums = [62 * 3, 60 * 3, 58 * 3, 64 * 3]
S4 = F(sum(sums), 3)
check('15-13-1', S4 - sums[0], {'62': 62, '52': S4 - sums[3], '64': S4 - sums[1]})
# 15-14-1 capital x months
w = [20 * 12, 40 * 9, 80 * 6]; dist_ = F(90) * F(7, 10)
check('15-14-1', dist_ * w[2] / sum(w), {'36': dist_ * F(80, 140), '40': F(90) * w[2] / sum(w), '21': dist_ * w[1] / sum(w)})
# 15-15-1 cold storage
check('15-15-1', F(3000 * 3, 10) + F(900, 3), {'1170': F(3900 * 3, 10), '1300': F(3900, 3), '1270': 1000 + F(900 * 3, 10)})
# 15-15-2 elevator
unit = F(54, 2 * 15)
check('15-15-2', 5 * unit - 3, {'9': 5 * unit, '2.4': F(54, 10) - 3, '15': F(54, 15) * 5 - 3})

# ============================== DAY 29 ==============================
# 29-1-1 desalination
sea = uniq([s for s in range(1, 100000) if F(55, 100) * s - F(45, 100) * s == 1802])
fresh = F(45, 100) * sea
def band(v):
    return '少于8000立方米' if v < 8000 else '8000～8100立方米之间' if v <= 8100 else '8100～8200立方米之间' if v <= 8200 else '多于8200立方米'
assert fresh != 8100 and fresh != 8200
check('29-1-1', band(fresh), {'8000～8100立方米之间': band(F(1800) / F(1, 10) * F(45, 100) - F(1, 1000)), '多于8200立方米': band(F(55, 100) * sea)})
# 29-1-2 drone spraying
mass = 5000 * F(12, 10); per = 1200 * F(25, 1000); mu = mass / per
check('29-1-2', math.floor(mu / 15), {'14': math.ceil(mu / 15), '11': math.floor(F(5000) / per / 15), '9': math.floor(F(5000) / F(12, 10) / per / 15)})
# 29-2-1 bus capacity: derive the large/medium capacity ratio from the 75% condition (any scale), then the extra buses
ks, totals, eqv = set(), set(), set()
for b_ in range(1, 80):
    for m_ in range(1, 80):
        if 8 * b_ + 12 * m_ != F(175, 100) * 8 * b_: continue
        k = (2 * 8 * b_ - (8 * b_ + 12 * m_)) / F(m_)          # additional medium buses
        ks.add(k); totals.add(F(2 * 8 * b_ - 8 * b_, m_)); eqv.add(F(2 * 8 * b_ - 8 * b_, b_))
check('29-2-1', uniq(ks), {'16': uniq(totals), '12': 12, '8': uniq(eqv)})
# 29-3-1 questionnaires
T = uniq([T for T in range(1, 10000) if all(v_.denominator == 1 for v_ in (F(T, 4), F(T, 4) * F(3, 4), F(3 * T, 4) * F(5, 6)))
          and F(3, 4) * T * F(5, 6) - F(1, 4) * T * F(3, 4) == 420])
check('29-3-1', T, {'840': F(420) / F(1, 2), '1120': F(420) / (F(5, 8) - F(1, 4)), '1680': 420 * 4})
# 29-3-2 two people at a bookstore
sols = [(a_, b_) for a_ in range(60, 1000) for b_ in range(60, 1000) if a_ - 60 == F(b_, 2) and b_ - 60 == F(2, 3) * a_]
a_, b_ = uniq(sols)
mis = uniq([(x, y) for x in range(60, 1000) for y in range(60, 1000) if x - 60 == F(y, 2) and y - 60 == F(2, 3) * (x - 60)])
check('29-3-2', a_ + b_, {'195': sum(mis), '225': a_ + b_ - 60, '150': b_})
# 29-4-1 boats
s, d = uniq([(s, d) for s in range(0, 19) for d in [18 - s] if 4 * d == 2 * 2 * s])
women = (2 * s - 10) + (4 * d - 30)
s2, d2 = uniq([(s, d) for s in range(0, 19) for d in [18 - s] if d == 2 * s])
check('29-4-1', 40 - women, {'20': 40 - ((2 * s2 - 10) + (4 * d2 - 30)), '14': women, '40': 40})
# 29-4-2 two price cuts
q = uniq([q for q in range(1, 1000) if F(q) / F(8, 10) - q == 15])
q1 = F(q) / F(8, 10); q2 = q1 + 25
check('29-4-2', 1 - q1 / q2, {'20%': F(20, 100), '33.3%': F(25) / 75, '40%': 1 - F(q) / q2}, approx=F(1, 1000))
# 29-5-1 two warehouses
sols = set()
for yi in range(3, 300, 3):
    for jia in range(1, 3000):
        out = yi // 3
        if jia - 3 * out == 12 * (yi - out): sols.add(F(jia, yi))
check('29-5-1', uniq(sols), {'8': F(24, 3), '13': F(12 * 3 + 3, 3), '12': 12})
# 29-5-2 red/white balls
r_, w_ = uniq([(3 * k, 5 * k) for k in range(1, 50) if 3 * k + 4 == 5 * k])
r_ += 4
p = F(math.comb(r_, 2), math.comb(r_ + w_, 2))
check('29-5-2', p, {'$\\frac{1}{4}$': F(r_, r_ + w_) ** 2, '$\\frac{9}{19}$': F(r_ * (r_ - 1), math.comb(r_ + w_, 2)), '$\\frac{1}{2}$': F(r_, r_ + w_)})
# 29-6-1 sorting test
M, W = 320, 400
t = uniq([t for t in range(1, 400) if 2 * t <= W and t <= M and (M - t) * 2 == (W - 2 * t) * 3])
check('29-6-1', 3 * t, {'280': 2 * t, '140': t, '300': 720 - 3 * t})
# 29-6-2 party share
men = F(3, 5) + F(1, 5); wom = F(2, 5) + F(4, 5)
check('29-6-2', (men * F(25, 100) + wom * F(40, 100)) / 2, {'32.5%': F(325, 1000), '31%': F(3, 5) * F(25, 100) + F(2, 5) * F(40, 100), '37%': F(1, 5) * F(25, 100) + F(4, 5) * F(40, 100)})
# 29-7-1 two schools (brute force)
sols = []
for a_ in range(3, 600, 3):
    for b_ in range(4, 600, 4):
        f1, g1 = a_ // 3, b_ // 4
        if f1 - g1 != 4: continue
        ra, rb = a_ - f1, b_ - g1
        if ra % 2 or rb % 3: continue
        if ra // 2 + rb // 3 == 30: sols.append(a_ - b_)
diff = uniq(sols)
lab = {-1: '少1人', 1: '多1人', -4: '少4人', 4: '多4人'}
check('29-7-1', lab[diff], {'多1人': lab[-diff], '多4人': lab[4]})
# 29-7-2 YoY and MoM chain
s24 = F(100); o24 = s24 * F(15, 10); o25 = o24 * F(11, 10); s25 = o25 / F(125, 100)
check('29-7-2', s25 / s24 - 1, {'35%': F(35, 100), '15%': F(15, 100)})
# 29-8-1 three towns: total +25%, A +150, B -20% and B25 = A25/2, C +50% and C24 = A24 + B24
sols = []
for a in range(1, 5000):
    j25 = a + 150; y25 = F(j25, 2); y24 = y25 / F(4, 5); b24 = a + y24; b25 = F(3, 2) * b24
    if j25 + y25 + b25 == F(5, 4) * (a + y24 + b24): sols.append((a, y24, b24, j25, y25, b25))
a, y24, b24, j25, y25, b25 = uniq(sols)
t24, t25 = a + y24 + b24, j25 + y25 + b25
check('29-8-1', b25 / t25, {'50%': b24 / t24, '75%': b25 / t24, '40%': b24 / t25})
# 29-8-2 per-capita vs total
check('29-8-2', F(108, 100) * F(96, 100) - 1, {'4%': F(4, 100), '12.5%': F(108, 100) / F(96, 100) - 1, '7.68%': F(8, 100) * F(96, 100)})
# 29-9-1 extinguishers
n, T = uniq([(n, 5 * n + 10) for n in range(1, 500) if F(125, 100) * (5 * n + 10) == 6 * n + 20])
check('29-9-1', (n + 6) * 7 - T, {'50': n * 7 - T, '52': (n + 6) * 7 - F(125, 100) * T})
# 29-9-2 staged distribution
n = uniq([n for n in range(11, 500) if 8 * n - 30 == 100 + 6 * (n - 10) + 12])
check('29-9-2', n, {'35': uniq([n for n in range(11, 500) if 8 * n - 30 == 100 + 6 * (n - 10)]),
                    '29': uniq([n for n in range(11, 500) if 8 * n - 30 == 100 + 6 * (n - 10) - 12])})
# 29-10-1 three granaries, final 2:3:4
sols = []
for A in range(1, 180):
    for B in range(1, 180 - A):
        C = 180 - A - B
        a_, b_, c_ = A - B, 2 * B, C
        b_, c_ = b_ - c_, 2 * c_
        c_, a_ = c_ - a_, 2 * a_
        if min(a_, b_, c_) > 0 and a_ * 3 == b_ * 2 and b_ * 4 == c_ * 3: sols.append((A, B, C))
A, B, C = uniq(sols)
check('29-10-1', A, {'55': B, '50': C})
# 29-10-2 three-team rotation (brute force over community sizes and team sizes)
sols = set()
for Bn in range(9, 60):
    An, Cn = Bn + 2, Bn + 4
    for a_ in range(0, An + 1):
        for c_ in range(0, Cn + 1):
            if An - a_ + c_ == Bn - 9 + a_ == Cn - c_ + 9: sols.add(a_)
check('29-10-2', uniq(sols), {'9': 9})
# 29-11-1 exchange chain
hkd = F(2781) / F(103, 100); cny = hkd / F(108, 100)
check('29-11-1', cny * F(101, 100), {'2500': cny, '2475': cny * F(99, 100), '2550': cny * F(102, 100)})
# 29-12-1 servers
sols = []
for z in range(1, 221):
    for y in range(0, 221 - z):
        x = 220 - y - z
        P1 = x + 2 * y + 4 * z
        if F(x, 2) + 2 * y + 8 * z == P1 and 4 * y + 8 * z == P1 and x % 2 == 0: sols.append((x, y, z))
x, y, z = uniq(sols)
check('29-12-1', y, {'20': z, '160': x, '80': 2 * y})
# 29-12-2 cyclic system
p, v, e = uniq([(p, v, e) for p in range(1, 60) for v in range(1, 60) for e in range(1, 60)
                if 3 * p + 2 * v + e == 52 and p + 3 * v + 2 * e == 38 and 2 * p + v + 3 * e == 42])
check('29-12-2', p + v + e, {'44': F(52 + 38 + 42, 3), '12': p, '26': F(52, 2)})
# 29-13-1 four contestants
sols = [(a_, b_, c_, d_) for a_ in range(60, 101) for b_ in [176 - a_] for c_ in [174 - a_] for d_ in [164 - c_] if b_ - d_ == 4]
a_, b_, c_, d_ = uniq(sols)
check('29-13-1', a_, {'85': b_, '87': 87, '88': 88})
# 29-13-2 rain gauges (relation independent of the free variables)
diffs = set()
for wu in range(10, 60):
    for c_ in [F(x, 2) for x in range(0, 200)]:
        ding = wu - 6; jy = 2 * c_ + 2
        if jy / 2 - (c_ + ding + wu) / 3 == 2: diffs.add(jy / 2 - wu)
dd = uniq(diffs)
lab = {F(1, 2): '高0.5毫米', F(-1, 2): '低0.5毫米', F(3, 2): '高1.5毫米', F(-3, 2): '低1.5毫米'}
check('29-13-2', lab[dd], {'高0.5毫米': lab[-dd]})
# 29-14-1 pre/post money
I = F(1)
V1 = uniq([F(k, 4) for k in range(1, 200) if F(2, 10) * F(k, 4) == F(16, 100) * (F(k, 4) + I)])
V2 = uniq([F(k, 4) for k in range(1, 400) if F(16, 100) * F(k, 4) == F(12, 100) * (F(k, 4) + 3 * I)])
check('29-14-1', V2 / (V1 + I) - 1, {'125%': V2 / V1 - 1, '180%': V2 / (V1 + I)})
# 29-14-2 cooperative dividends
pool = F(500000) * F(8, 10); base = 400 * 20; per_share = (pool - base) / 2000
check('29-14-2', 10 * per_share + 4 * 20, {'2000': pool / 2000 * 10, '1960': 10 * per_share, '2500': F(500000) / 2000 * 10})
# 29-15-1 two sharing schemes
stay = {'甲': [1, 2, 3], '乙': [1, 2, 3], '丙': [1, 2, 3], '丁': [1, 2], '戊': [1]}
night_n = {k: sum(1 for p_ in stay.values() if k in p_) for k in (1, 2, 3)}
plan1 = sum(F(1200, night_n[k]) for k in stay['甲'])
pn = sum(len(x_) for x_ in stay.values()); plan2 = F(3600, pn) * 3
check('29-15-1', plan1 - plan2, {'220': plan1 - F(3600, 5)})
# 29-15-2 carpool by segment
check('29-15-2', F(30) + F(30, 2) + F(30, 3), {'30': F(90, 3), '45': F(90 * 30, 30 + 20 + 10)})

# ============================== DAY 39 ==============================
# 39-1-1 subsidy months
def months(y1, m1, y2, m2): return (y2 - y1) * 12 + (m2 - m1) + 1
end_y, end_m = 2023 + (3 + 35 - 1) // 12, (3 + 35 - 1) % 12 + 1
assert months(2023, 3, end_y, end_m) == 36
mas = months(2023, 3, 2024, 10); phd = 36 - mas
check('39-1-1', mas * 800 + phd * 1500, {'39300': (mas + 1) * 800 + (phd - 1) * 1500, '40700': (mas - 1) * 800 + (phd + 1) * 1500, '54000': 36 * 1500})
# 39-1-2 rooftop PV
kw = 120000 * F(15, 100); kwh = kw * 1100; co2 = kwh * F(8, 10)
check('39-1-2', co2 / 20, {'99万': kwh / 20, '7.92万': co2 / 20 / 10, '792万': co2 / 20 * 10})
# 39-2-1 volunteer photos (brute force)
sols = set()
for single in range(1, 38):
    group = 38 - single
    if group != 2 * single + 2 or group % 2: continue
    trio = group // 2; pairs = group - trio
    for x in range(pairs + 1):            # Wang-Li
        for y in range(pairs + 1 - x):    # Wang-Chen
            z = pairs - x - y             # Li-Chen
            wang = trio + x + y; li = trio + x + z; chen = trio + y + z
            if chen != wang or wang - li != 4: continue
            for sl in range(single + 1):
                sw = 2 * sl; sc = single - sw - sl
                if sc >= 0 and sc == sw + sl: sols.add((li + sl, wang + sw, chen + sc, li))
li_t, wang_t, chen_t, li_g = uniq(sols)
check('39-2-1', li_t, {'27': wang_t, '29': chen_t, '19': li_g})
# 39-2-2 party branches
Bmax = max(B for B in range(1, 87) if 2 * B - 4 > 0 and 86 - (2 * B - 4) - B >= 2 * B - 4)
check('39-2-2', Bmax, {'19': math.ceil(F(94, 5))})
# 39-3-1 three classes
sols = []
for T in range(200, 3000):
    a_ = F(T - 60, 5) + 60; b_ = F(2 * (T - 60), 7) + 60; c_ = F(T - 48, 4) + 48
    if a_ + b_ + c_ == T and all(v_.denominator == 1 for v_ in (a_, b_, c_)): sols.append((T, a_, b_, c_))
T, a_, b_, c_ = uniq(sols)
check('39-3-1', b_, {'144': a_, '156': c_})
# 39-3-2 graduates exam
sols = []
for T in range(500, 601):
    fr = F(3 * T, 8); ot = T - fr
    if fr.denominator == 1 and (fr * F(2, 5)).denominator == 1 and (ot * F(4, 7)).denominator == 1:
        sols.append(fr * F(2, 5) + ot * F(4, 7))
T = 560
check('39-3-2', uniq(sols), {'260': F(5 * T, 8) * F(2, 5) + F(3 * T, 8) * F(4, 7), '280': F(T, 2)})
# 39-4-1 two workshops
A0, B0 = 4 * 5, 3 * 4
A1, B1 = A0 * F(12, 10), B0 * F(125, 100)
check('39-4-1', A1 / B1 - 1, {'100%': A1 / B0 - 1, '33.3%': A0 / B1 - 1, '37.5%': (A1 - B1) / A1}, approx=F(1, 1000))
# 39-4-2 prize values
vals_ = [F(40, 1), F(35, 5), F(25, 20)]; cnts = [1, 5, 20]; avg = F(100, 26)
above = sum(c for v_, c in zip(vals_, cnts) if v_ > avg)
check('39-4-2', F(above, 26), {'$\\frac{1}{26}$': F(1, 26), '$\\frac{3}{4}$': F(75, 100), '$\\frac{10}{13}$': F(20, 26)})
# 39-5-1 sorting centres: per-worker ratio 1.25, total ratio 1.75, 18 transferred
sols = [(n1, n2) for n1 in range(19, 1000) for n2 in range(1, 1000) if F(5, 4) * n1 == F(7, 4) * n2 and F(5, 4) * (n1 - 18) == n2 + F(5, 4) * 18]
n1, n2 = uniq(sols)
naive = uniq([(a1, a2) for a1 in range(19, 1000) for a2 in range(1, 1000) if a1 == F(7, 4) * a2 and a1 - 18 == a2 + 18])
# error path solved exactly: 1.25*a1 = 1.75*a2 and 1.25*(a1-18) = a2 + 18  (moved workers counted at B's efficiency)
_a1 = (F(5, 4) * 18 + 18) / (F(5, 4) - F(5, 4) / F(7, 4)); wrong = (_a1, F(5, 4) * _a1 / F(7, 4))
check('39-5-1', n2, {'48': naive[1], '54': wrong[1], '84': n1})
# 39-5-2 speed ratio change
def dist(va2, vb2):
    # meeting point 3/5 from A ; after meeting: A needs 2 parts, B needs 3 parts (5 parts total)
    tA = F(2) / va2; short = 3 - vb2 * tA
    return F(28) / short * 5
check('39-5-2', dist(F(3) * F(2, 3), F(2) * F(5, 4)), {'140': dist(F(2), F(2)), '105': dist(F(3), F(5, 2))})
# 39-6-1 two clinics
sols = set()
for x in range(1, 200):            # Jia: doctors 3x, nurses x
    for y in range(1, 200):        # Yi: doctors y, nurses y
        if (3 * x + y) != 2 * (x + y): continue
        for t in range(1, 16):
            s_ = 15 - t
            if F(s_, 2 * y) == 3 * F(t, 4 * x): sols.add((5 * t + 2 * s_, 5 * s_ + 2 * t))
right, swapped = uniq(sols)
check('39-6-1', right, {'57': swapped, '30': 2 * 15, '75': 5 * 15})
# 39-6-2 conditional probability
g1, g2 = F(4) * F(1, 2), F(5) * F(2, 3)
check('39-6-2', g2 / (g1 + g2), {'$\\frac{3}{8}$': g1 / (g1 + g2), '$\\frac{2}{3}$': F(2, 3), '$\\frac{5}{9}$': F(5, 9)})
# 39-7-1 marketing budget
check('39-7-1', F(23, 97), {'23.0%': F(23, 100), '24.5%': F(23, 94), '26.0%': F(26, 100)}, approx=F(5, 10000))
# 39-7-2 export share
ex24, im24 = F(8000) * F(6, 10), F(8000) * F(4, 10)
ex25, im25 = ex24 * F(11, 10), im24 * F(95, 100)
pp = (ex25 / (ex25 + im25) - F(6, 10)) * 100
check('39-7-2', pp, {'6': (ex25 / 8000 - F(6, 10)) * 100, '15': 15}, approx=F(1, 10))
# 39-7-3 five fairs (brute force on integer amounts)
sols = []
for s1 in range(1, 400):
    s2 = F(12, 10) * s1; s3 = s2 / (1 - F(1, 6))
    front = s1 + s2 + s3; back = F(3, 2) * front
    s4 = back / (2 + F(1, 3)); s5 = s4 * F(4, 3)
    if s5 - s3 == 84: sols.append((s1, s2, s3, s4, s5))
s1, s2, s3, s4, s5 = uniq(sols)
def band2(v): return '不到50万元' if v < 50 else '50～60万元之间' if v <= 60 else '60～70万元之间' if v <= 70 else '70万元以上'
check('39-7-3', band2(s4 - s1), {'70万元以上': band2(s5 - s1), '50～60万元之间': band2(s4 - s2), '不到50万元': band2(s4 - s3)})
# 39-8-1 tourism halves: +10%, +25%, full year +19%
r = uniq([F(x, y) for x in range(1, 50) for y in range(1, 50) if F(10, 100) * x + F(25, 100) * y == F(19, 100) * (x + y) and math.gcd(x, y) == 1])
check('39-8-1', r / (r + 1), {'60%': 1 / (r + 1), '66.7%': r, '50%': F(1, 2)}, approx=F(1, 1000))
# 39-8-2 contribution
rest = (F(6, 100) - F(20, 100) * F(15, 100)) / F(80, 100)
check('39-8-2', rest, {'3%': F(6, 100) - F(20, 100) * F(15, 100), '4.8%': F(6, 100) * F(80, 100)})
# 39-9-1 milk and eggs
n = uniq([n for n in range(1, 500) if ((8 * n - 6) - 6 * n) - ((5 * n - 3) - 4 * n) == 18])
milk, egg = 8 * n - 6, 5 * n - 3
def buy(rm, re_):
    k = 1
    while rm * k * n < milk or re_ * k * n < egg: k += 1
    return rm * k * n - milk + re_ * k * n - egg, re_ * k * n - egg
c32, e32 = buy(3, 2); c43, e43 = buy(4, 3)
check('39-9-1', min(c32, c43), {'51': c32, '24': e43})
# 39-9-2 rooms
cands = set()
for r_ in range(1, 200):
    ppl = 3 * r_ + 10
    used = r_ - 3
    if 4 * (used - 1) < ppl < 4 * used: cands.add(ppl)
hit = [o for o in PLAN['39-9-2']['opts'] if int(o) in cands]
check('39-9-2', int(uniq(hit)))
assert 76 == 3 * 22 + 10 and 76 == 4 * 19 and 88 == 3 * 26 + 10 and 88 % 4 == 0 and (80 - 10) % 3 != 0
# 39-10-1 four-class rotation: A->B, B->C, C->D, D->A ; solve each class's balance for every (n, x)
offs = set()
for n0 in range(5, 60):
    A, B, C, D = n0 + 2, n0, n0 + 5, n0 + 1
    assert (A + B + C + D) % 4 == 0
    avg = (A + B + C + D) // 4
    for x in range(0, B + 1):
        a = avg - B + x          # B: B - x + a = avg
        c = C + x - avg          # C: C - c + x = avg
        d = D + c - avg          # D: D - d + c = avg
        if min(a, c, d) < 0 or a > A or c > C or d > D: continue
        assert A - a + d == avg  # A: A - a + d = avg (consistency)
        offs.add((c - x, a - x, C - B))
co, ao, cb = uniq(offs)
check('39-10-1', f'$x+{co}$', {'$x+2$': f'$x+{ao}$', '$x+5$': f'$x+{cb}$'})
# 39-10-2 three book corners
sols = []
for A in range(4, 600, 4):
    for B in range(1, 600 - A):
        C = 600 - A - B
        a_ = A - A // 4; b_ = B + A // 4
        if b_ % 3: continue
        c_ = C + b_ // 3; b_ = b_ - b_ // 3
        if a_ * 4 == b_ * 3 and b_ * 5 == c_ * 4: sols.append((A, B, C, b_))
A, B, C, bfin = uniq(sols)
check('39-10-2', B, {'300': bfin * F(3, 2), '200': bfin, '150': C})
# 39-11-1 points supermarket (maximize item count)
best = max((o + r_ + t, o, r_, t) for o in range(1, 7) for r_ in range(1, 20) for t in range(1, 50) if 15 * o + 5 * r_ + 2 * t == 90)
check('39-11-1', best[0], {'45': F(90, 2), '35': best[3]})
# 39-11-2 flour combos
units = 1200; bun, bao = units // 600, units // 400
rest_ = units * F(4, 5)
check('39-11-2', math.floor(rest_ / (2 * bun + bao)), {'171': math.floor(F(units) / (2 * bun + bao)), '138': math.ceil(rest_ / (2 * bun + bao)), '120': math.floor(rest_ / (2 * bao + bun))})
# 39-12-1 masks
sols = [(a_, b_, 2100 - a_ - b_) for a_ in range(1, 2100) for b_ in range(1, 2100 - a_)
        if 3 * a_ + 2 * b_ == 4 * (2100 - a_ - b_) and a_ + (2100 - a_ - b_) == 2 * b_]
a_, b_, c_ = uniq(sols)
check('39-12-1', b_, {'600': a_, '800': c_})
# 39-12-2 underdetermined system: the combination must be the same for every positive solution (prices in 0.1 yuan)
combos = set()
for p10 in range(1, 300):
    for n10 in range(1, 300):
        f10 = 280 - 3 * p10 - 7 * n10
        if f10 > 0 and 4 * p10 + 10 * n10 + f10 == 370: combos.add(F(p10 + n10 + f10, 10))
check('39-12-2', uniq(combos), {'9': F(37 - 28), '19': F(28 - 9)})
# 39-13-1 orchards (redundant condition must be consistent)
sols = set()
for jy in range(0, 51):
    yy = 50 - jy
    for jn in range(0, 21):
        yn = 20 - jn
        if jy - yn == 14 and 3 * jn == yy: sols.add(jy + jn)
check('39-13-1', uniq(sols), {'36': 70 - uniq(sols)})
# 39-13-2 judges
S_ = uniq([F(x, 10) for x in range(300, 600) if F(x, 10) - (F(x, 10) - 36) - (F(x, 10) - F(372, 10)) == F(276, 10)])
H = S_ - 36; L = S_ - F(372, 10)
check('39-13-2', H, {'8.4': L})
# 39-14-1 village cold-chain
xv = uniq([x for x in range(0, 1000) if F(400, 100 + x) == F(4, 3)])
check('39-14-1', F(100 + 100 + xv, 400 + 100 + 100 + xv), {'33.3%': F(200, 600), '42.9%': F(300, 700)}, approx=F(1, 1000))
# 39-14-2 partnership and margin
dist_ = F(21) * 6; profit = dist_ / F(7, 10)
check('39-14-2', profit / F(15, 100), {'840': dist_ / F(15, 100), '1000': F(21) * 5 / F(7, 10) / F(15, 100), '2800': dist_ / F(3, 10) / F(15, 100)})
# 39-15-1 minibus
R = uniq([R for R in range(1, 5000) if F(R, 6) - F(R, 7) == 10])
check('39-15-1', R, {'240': uniq([R for R in range(1, 5000) if F(R, 6) - F(R, 8) == 10]),
                     '360': uniq([R for R in range(1, 5000) if F(R, 6) - (R - 2 * F(R, 12)) / 6 == 10])})
# 39-15-2 dinner AA
n = uniq([n for n in range(3, 100) if any(F(Tt, n - 2) - F(Tt, n) == 20 and F(Tt, n) - F(Tt, n + 4) == 20 for Tt in range(1, 5000))])
check('39-15-2', n)

# ============================== summary ==============================
planned = set(PLAN); checked = set(RES)
missing = planned - checked; extra = checked - planned
bad = [k for k, v in RES.items() if v]
print('variants planned', len(planned), 'checked', len(checked), 'missing', sorted(missing), 'extra', sorted(extra), 'FAIL', bad)
sys.exit(1 if (bad or missing or extra) else 0)
