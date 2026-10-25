# Independent blind solver for revh_D (D04 economic-profit set), written from the stems only.
# Each question: brute-force / exact-fraction solve from stem data, then test all four options.
import json, math
from fractions import Fraction as F

Q = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/review/revh_D_questions.json'))
opts = {q['vid']: q['options'] for q in Q}
res = {}

def num(s):
    s = s.replace('约', '').replace('%', '')
    return F(s)

def report(vid, ans, note):
    res[vid] = ans
    print(f'{vid}: {ans}   | {note}')

# ---------- v01 ----------
cost = F(200) + F(200) * F(10, 100) + 35          # 255
need = cost * F(120, 100)                          # revenue after commission must cover cost*1.2
netf = F(9, 10) * F(85, 100)                       # actual deal = 0.9P, mall takes 15% of deal
Pmin = need / netf
ok = [k for k, v in opts['D04-math-h-v01'].items() if netf * num(v) - cost >= cost * F(1, 5)]
minok = min(ok, key=lambda k: num(opts['D04-math-h-v01'][k]))
report('D04-math-h-v01', minok, f'Pmin={Pmin}; options satisfying={ok}')

# ---------- v02 ----------
# a = 2024 frozen profit (>0), b = 2024 prepared-food loss (>0)
# 1.1a - 0.6b = 1.5(a-b)  ->  b/a = 0.4/0.9
r = (F(15, 10) - F(11, 10)) / (F(15, 10) - F(6, 10))
assert 1 - r > 0  # 2024 total profit positive so 'growth 50%' meaningful
good = []
for k, v in opts['D04-math-h-v02'].items():
    rr = num(v) / 100
    g = (F(11, 10) - F(6, 10) * rr) / (1 - rr) - 1
    good.append((k, float(g)))
best = min(good, key=lambda t: abs(t[1] - 0.5))
report('D04-math-h-v02', best[0], f'b/a={r}={float(r):.4f}; growth per option={good}')

# ---------- v03 ----------
def pay3(P):
    nat = min(P * F(2, 10), F(2000))
    city = min((P - nat) * F(1, 10), F(1000))
    return P - nat - city
sols = [P for P in range(1, 40001) if pay3(F(P)) == 8100]
# also check pay3 is strictly increasing so solution unique over reals: piecewise linear, slopes 0.72,0.9,1 >0
ok = [k for k, v in opts['D04-math-h-v03'].items() if pay3(num(v)) == 8100]
report('D04-math-h-v03', ok, f'integer solutions={sols}; option pays={ {k: float(pay3(num(v))) for k, v in opts["D04-math-h-v03"].items()} }')

# ---------- v04 ----------
c = F(100)
ok = []
for k, v in opts['D04-math-h-v04'].items():
    m = num(v) / 100 * c
    p = c + m
    if F(8, 10) * (F(11, 10) * p - c) == F(12, 10) * (p - c):
        ok.append(k)
# exact solve: 0.8(1.1p-c)=1.2(p-c) -> 0.88p-0.8c=1.2p-1.2c -> 0.4c=0.32p
p = F(4, 10) * c / F(32, 100)
report('D04-math-h-v04', ok, f'p={p}, margin/cost={(p - c) / c}')

# ---------- v05 ----------
ok = []
info = {}
for k, v in opts['D04-math-h-v05'].items():
    r0 = num(v) / 100
    r1 = (1 + r0) * F(11, 10) / F(12, 10) - 1
    info[k] = float((r0 - r1) * 100)
    if r0 - r1 == F(1, 10):
        ok.append(k)
# also: profit rate as profit/price (sales margin) interpretation
alt = []
for k, v in opts['D04-math-h-v05'].items():
    s0 = num(v) / 100
    # s = 1 - c/p ; new s1 = 1 - 1.2c/(1.1p) = 1 - (12/11)(1-s0)
    s1 = 1 - F(12, 11) * (1 - s0)
    if s0 - s1 == F(1, 10):
        alt.append(k)
report('D04-math-h-v05', ok, f'drop (pct pts) per option={info}; sales-margin reading matches={alt}')

# ---------- v06 ----------
ok = []
for k, v in opts['D04-math-h-v06'].items():
    y = num(v); x = F(1)
    before = 5 * x + 2 * y
    after = 5 * F(5, 10) * 3 * x + 2 * F(8, 10) * F(125, 100) * y
    if after == F(12, 10) * before:
        ok.append(k)
report('D04-math-h-v06', ok, 'weekly: 5 weekdays + 2 weekend days')

# ---------- v07 ----------
# Jan: n meals, fixed F0, food v. avg = F0/n + v. Mar: 1.25n, avg = 0.9*Jan.
# let f = F0/n: 0.8f + v = 0.9(f+v) -> v = f
f = F(1); v = f
assert F(8, 10) * f + v == F(9, 10) * (f + v)
jan = f + v; dbl = f / 2 + v
drop = (jan - dbl) / jan
ok = [k for k, vv in opts['D04-math-h-v07'].items() if num(vv) / 100 == drop]
report('D04-math-h-v07', ok, f'drop={drop}')

# ---------- v08 ----------
D = 3000
tc = {q: F(250) * D / q + F(6) * q / 2 for q in range(1, D + 1) if D % q == 0}
qbest = min(tc, key=tc.get)
ok = [k for k, vv in opts['D04-math-h-v08'].items() if int(num(vv)) == qbest]
report('D04-math-h-v08', ok, f'best batch={qbest}, cost={tc[qbest]}; option costs={ {k: float(tc[int(num(vv))]) for k, vv in opts["D04-math-h-v08"].items()} }')

# ---------- v09 ----------
def fee9(minutes, a, b):
    h = math.ceil(minutes / 60)
    return 3 * min(h, a) + b * max(h - a, 0)
params = []
for a in range(1, 30):
    # solve b from 甲 (260 min) then check 乙 (455 min)
    h1 = math.ceil(260 / 60)
    if h1 <= a:
        if 3 * h1 == 19:
            params.append((a, None))
        continue
    b = F(19 - 3 * a, h1 - a)
    if b <= 0:
        continue
    if fee9(455, a, b) == 34:
        params.append((a, b))
mx = []
for a, b in params:
    ts = [t for t in range(1, 48 * 60 + 1) if fee9(t, a, b) == 24]
    mx.append((a, b, min(ts) / 60 if ts else None, max(ts) / 60 if ts else None))
ok = [k for k, vv in opts['D04-math-h-v09'].items() if mx and num(vv) == F(mx[0][3]).limit_denominator()]
report('D04-math-h-v09', ok, f'(a,b,min_t,max_t) for 丙 = {mx}')

# ---------- v10 ----------
def pay10(n):
    orig = F(5 * n)
    t1 = min(orig, 100)
    t2 = min(max(orig - 100, 0), 50)
    t3 = max(orig - 150, 0)
    return t1 + F(8, 10) * t2 + F(5, 10) * t3
nmin = next(n for n in range(1, 1000) if pay10(n) / n <= 4)
ok = [k for k, vv in opts['D04-math-h-v10'].items() if int(num(vv)) == nmin]
report('D04-math-h-v10', ok, f'nmin={nmin}; avg(43)={float(pay10(43) / 43):.4f}, avg(44)={float(pay10(44) / 44):.4f}')

# ---------- v11 ----------
def tax11(x):
    x = F(x)
    t = F(0)
    t += F(3, 100) * min(x, 3000)
    t += F(10, 100) * min(max(x - 3000, 0), 9000)
    t += F(20, 100) * min(max(x - 12000, 0), 13000)
    return t
sol = [x for x in range(0, 19001) if tax11(x + 6000) - tax11(x) == 840]
ok = [k for k, vv in opts['D04-math-h-v11'].items() if int(num(vv)) in sol]
report('D04-math-h-v11', ok, f'solutions for 甲={sol[:5]}... count={len(sol)}')

# ---------- v12 ----------
def ok12(n):
    cost = 120000 + 40 * n
    prof = 60 * n - cost
    return F(prof, cost) >= F(1, 5)
nmin = next(n for n in range(1, 100000) if ok12(n))
ok = [k for k, vv in opts['D04-math-h-v12'].items() if int(num(vv)) == nmin]
report('D04-math-h-v12', ok, f'nmin={nmin}')

# ---------- v13 ----------
cands = {'no-build': 8000 * 30}
for kk in range(0, 6001):
    cands[f'build-{kk}'] = 90000 + 18 * kk + 30 * (8000 - kk)
best = min(cands, key=cands.get)
ok = [k for k, vv in opts['D04-math-h-v13'].items() if num(vv) * 10000 == cands[best]]
report('D04-math-h-v13', ok, f'best={best} {cands[best]}; build-max={cands["build-6000"]}; build-all-if-no-cap={90000 + 18 * 8000}')

# ---------- v14 ----------
def c14(t):
    jia = 80 * t
    yi = 1200 + 60 * max(t - 20, 0)
    bing = 2400 + 40 * max(t - 50, 0)
    return jia, yi, bing
good = [F(i, 100) for i in range(1, 10001) if (lambda j, y, b: y < j and y < b)(*c14(F(i, 100)))]
lo, hi = min(good), max(good)
# check contiguous
contig = len(good) == int((hi - lo) * 100) + 1
report('D04-math-h-v14', 'A' if (lo > 15 and lo <= F(1501, 100) and hi < 40 and hi >= F(3999, 100)) else '?', f'grid range=({float(lo)}, {float(hi)}), contiguous={contig}; eq at 15: {c14(F(15))}, at 40: {c14(F(40))}')

# ---------- v15 ----------
def prof15(n):
    vc = 100 * min(n, 3000) + 90 * max(n - 3000, 0)
    return 150 * n - 300000 - vc
nmin = next(n for n in range(0, 100000) if prof15(n) >= 150000)
ok = [k for k, vv in opts['D04-math-h-v15'].items() if int(num(vv)) == nmin]
report('D04-math-h-v15', ok, f'nmin={nmin}')

# ---------- v16 ----------
keep = F(9, 10) ** 2
avgp = F(75, 100) + F(25, 100) * F(1, 2)
target = F(1215, 100) * F(14, 10)
p16 = target / (keep * avgp)
ok = [k for k, vv in opts['D04-math-h-v16'].items() if num(vv) == p16]
report('D04-math-h-v16', ok, f'price={p16}; keep={keep}; avg factor={avgp}')

# ---------- v17 ----------
ordinary = F(85, 100) * 30 - 10 - 1
cmax = F(97, 100) * 30 - 10 - ordinary
ok = [k for k, vv in opts['D04-math-h-v17'].items() if num(vv) == cmax]
report('D04-math-h-v17', ok, f'cmax={cmax}')

# ---------- v18 ----------
kmin = next(k for k in range(0, 1501) if 60 * k - 24 * 1500 >= (60 - 30) * k)
ok = [k for k, vv in opts['D04-math-h-v18'].items() if int(num(vv)) == kmin]
report('D04-math-h-v18', ok, f'kmin={kmin}')

# ---------- v19 ----------
dem = [80] * 3 + [100] * 6 + [120] * 7 + [140] * 4
def tot19(q):
    s = 0
    for d in dem:
        sold = min(d, q)
        s += 12 * sold + 2 * (q - sold) - 8 * q
    return s
vals = {q: tot19(q) for q in (80, 100, 120, 140)}
qbest = max(vals, key=vals.get)
ok = [k for k, vv in opts['D04-math-h-v19'].items() if int(num(vv)) == qbest]
report('D04-math-h-v19', ok, f'totals={vals}; mean demand={sum(dem) / len(dem)}')

json.dump(res, open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/rev_h_D_work/my_answers.json', 'w'), ensure_ascii=False, indent=1)
