# Independent brute-force / direct solves for D14 (M14) candidates.
# Each solver computes the value from the stem data, then maps it onto the
# option letters exactly as printed in the crop (real) or packet (teacher).
from fractions import Fraction as F
from itertools import permutations, combinations
from math import gcd, isqrt

res = {}

def pick(opts, pred):
    hits = [k for k, v in opts.items() if pred(v)]
    return hits

def record(qid, opts, pred, value, expect):
    hits = pick(opts, pred)
    ok = (len(hits) == 1 and hits[0] == expect)
    res[qid] = (hits, value, expect, ok)

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

# ---------------- REAL ----------------
# 2021HB-64: N<=100, N%9==7, N%11==9
sol = [n for n in range(1, 101) if n % 9 == 7 and n % 11 == 9]
record('2021HB-64', {'A': 98, 'B': 97, 'C': 96, 'D': 95}, lambda v: v in sol, sol, 'B')

# 2019JSA-53: minimal N with N%3==2, N%5==3, N%7==4
n = next(n for n in range(1, 10**4) if n % 3 == 2 and n % 5 == 3 and n % 7 == 4)
record('2019JSA-53', {'A': 23, 'B': 53, 'C': 88, 'D': 158}, lambda v: v == n, n, 'B')

# 2018ZJA-57: actual <200, %5==2, %8==7, %7==6 ; ratio (213-N)/213
sol = [n for n in range(1, 200) if n % 5 == 2 and n % 8 == 7 and n % 7 == 6]
assert len(sol) == 1
r = F(213 - sol[0], 213)
rng = {'A': (0, F(20, 100)), 'B': (F(20, 100), F(25, 100)), 'C': (F(25, 100), F(30, 100)), 'D': (F(30, 100), 1)}
record('2018ZJA-57', rng, lambda v: v[0] < r < v[1], (sol, float(r)), 'B')

# 2018GK-63: 369 A + 412 B; equal batch size s, fewest batches (>1), exactly one mixed batch
tot = 369 + 412
cands = []
for s in sorted(divisors(tot), reverse=True):
    if s == tot:  # one batch: "分批" implies more than one
        continue
    # A fills batches first (order irrelevant): mixed batch exists iff 369 % s != 0
    if 369 % s != 0 and 412 % s != 0 and (369 % s) + (412 % s) == s:
        cands.append((s, 412 % s))
        break
record('2018GK-63', {'A': 14, 'B': 32, 'C': 57, 'D': 65}, lambda v: v == cands[0][1], cands, 'C')

# 2020GKD-66: min X with X(X+1)/2 % 48 == 0
X = next(x for x in range(1, 1000) if (x * (x + 1) // 2) % 48 == 0)
rng = {'A': (41, 60), 'B': (61, 10**9), 'C': (1, 19), 'D': (20, 40)}
record('2020GKD-66', rng, lambda v: v[0] <= X <= v[1], X, 'D')

# 2015ZJA-71: 10 cards flipped by divisors -> odd flips face up; max-min
up = [k for k in range(1, 11) if len([d for d in range(1, 11) if k % d == 0]) % 2 == 1]
val = max(up) - min(up)
record('2015ZJA-71', {'A': 2, 'B': 4, 'C': 6, 'D': 8}, lambda v: v == val, (up, val), 'D')

# 2023SC-54: ab -> ba -> a0b with equal hourly increments; fare = a0b - ab
sols = []
for a in range(1, 10):
    for b in range(1, 10):
        x0, x1, x2 = 10 * a + b, 10 * b + a, 100 * a + b
        if x1 - x0 == x2 - x1 and x1 > x0:
            sols.append(x2 - x0)
record('2023SC-54', {'A': 82, 'B': 86, 'C': 90, 'D': 95}, lambda v: v in sols, sols, 'C')

# 2020SZ1-53: 4 distinct integers, pairwise sums {23,27,30,31,34,max hidden}
found = set()
for a in range(1, 40):
    for b in range(a + 1, 40):
        for c in range(b + 1, 40):
            for d in range(c + 1, 40):
                s = sorted([a + b, a + c, a + d, b + c, b + d, c + d])
                if s[:5] == [23, 27, 30, 31, 34] and s[5] > 34:
                    found.add(d)
record('2020SZ1-53', {'A': 17, 'B': 18, 'C': 21, 'D': 23}, lambda v: v in found, found, 'C')

# 2019ZJA-71: digits 1..9 once, three 3-digit multiples of 9, max sum
best = 0
digs = list(range(1, 10))
for p in permutations(digs):
    n1 = p[0] * 100 + p[1] * 10 + p[2]
    n2 = p[3] * 100 + p[4] * 10 + p[5]
    n3 = p[6] * 100 + p[7] * 10 + p[8]
    if n1 % 9 == 0 and n2 % 9 == 0 and n3 % 9 == 0:
        best = max(best, n1 + n2 + n3)
record('2019ZJA-71', {'A': 2007, 'B': 2394, 'C': 2448, 'D': 2556}, lambda v: v == best, best, 'C')

# 2022SC2-49: sales from 6/6, +1 per day, 6/16 = 22; total June
tot = sum(22 + (d - 16) for d in range(6, 31))
record('2022SC2-49', {'A': 555, 'B': 600, 'C': 645, 'D': 690}, lambda v: v == tot, tot, 'B')

# 2024GK-65: jia +m/day, yi -2m/day, day5 equal, yi 5-day sum = 2*jia ; yi1/jia1
m = F(1)
# unknown a1 (jia day1), b1 (yi day1): b1-8m = a1+4m ; sum_b = 5b1 - 20m ; sum_a = 5a1 + 10m
# => b1 = a1 + 12m ; 5(a1+12m) - 20m = 2(5a1+10m) -> 5a1 + 40m = 10a1 + 20m -> a1 = 4m
a1 = 4 * m; b1 = a1 + 12 * m
assert 5 * b1 - 20 * m == 2 * (5 * a1 + 10 * m) and b1 - 8 * m == a1 + 4 * m
ratio = b1 / a1
record('2024GK-65', {'A': 6, 'B': 7, 'C': 4, 'D': 5}, lambda v: v == ratio, ratio, 'C')

# 2021ZJA-68: base year rev a; year k (k=1..15) = a + 1.5k ; 14th FYP = 0.8*(12th+13th)
# solve linear in a
def S(lo, hi, a):
    return sum(a + F(3, 2) * k for k in range(lo, hi + 1))
# S(11,15,a) = 0.8*(S(1,10,a)) -> 5a + c1 = 0.8(10a + c2)
c1 = S(11, 15, 0); c2 = S(1, 10, 0)
a = (c1 - F(4, 5) * c2) / (F(8) - 5)
total = S(1, 15, a)
rng = {'A': (0, 300), 'B': (300, 330), 'C': (330, 360), 'D': (360, 10**9)}
record('2021ZJA-68', rng, lambda v: v[0] < total < v[1], (a, float(total)), 'C')

# 2024SD-55: distinct integer scores, adjacent diff 5; 3 below 70; above-70 mean 82
sols = []
for lo in range(0, 70):           # lowest score
    for n in range(4, 40):        # total people
        sc = [lo + 5 * i for i in range(n)]
        below = [s for s in sc if s < 70]
        above = [s for s in sc if s > 70]
        if len(below) == 3 and above and F(sum(above), len(above)) == 82:
            sols.append(F(len(above), n))
sols = set(sols)
rng = {'A': (0, F(1, 2)), 'B': (F(1, 2), F(6, 10)), 'C': (F(6, 10), F(7, 10)), 'D': (F(7, 10), 1)}
assert len(sols) == 1
r = list(sols)[0]
record('2024SD-55', rng, lambda v: v[0] < r < v[1], float(r), 'C')

# 2022GK-70: peach +5000/mo, orange +2000/mo; Q1 peach - orange = -45000 ; full-year diff
# d1 = p1 - o1 ; Q1 diff = 3 d1 + (5000-2000)*(0+1+2) ; year diff = 12 d1 + 3000*66
d1 = F(-45000 - 3000 * 3, 3)
yd = 12 * d1 + 3000 * 66
opts = {'A': ('less', 0, 50000), 'B': ('less', 50000, 10**12), 'C': ('more', 0, 50000), 'D': ('more', 50000, 10**12)}
def pred(v):
    kind, lo, hi = v
    if kind == 'less':
        return yd < 0 and lo < -yd < hi
    return yd > 0 and lo < yd < hi
record('2022GK-70', opts, pred, yd, 'A')   # crop order (official file letter B refers to another order)

# 2023GKD-67: daily +200 ; week3 total = 2 * week1 total ; first day reaching 10000
for x in range(0, 20000):
    w1 = sum(x + 200 * i for i in range(0, 7))
    w3 = sum(x + 200 * i for i in range(14, 21))
    if w3 == 2 * w1:
        break
day = next(n for n in range(1, 1000) if x + 200 * (n - 1) >= 10000)
record('2023GKD-67', {'A': 37, 'B': 38, 'C': 39, 'D': 40}, lambda v: v == day, (x, day), 'D')

# 2022GD-40: layers increase by 1 downward; remove top 3 layers + 3 from each of remaining 10 -> 99
sols = []
for top in range(1, 200):
    layers = [top + i for i in range(13)]
    removed = sum(layers[:3]) + 3 * 10
    if removed == 99:
        sols.append(sum(l - 3 for l in layers[3:]))
record('2022GD-40', {'A': 245, 'B': 265, 'C': 305, 'D': 325}, lambda v: v in sols, sols, 'B')

# 2026GK-80: month k (1..12) = w + (k-1)k ; Q1 = 0.18T ; H1 = 0.48T ; year - T in units of k
# Let k = 1 (scale). unknown w, T: 3w + 3 = 0.18T ; 6w + 15 = 0.48T
from fractions import Fraction
kk = Fraction(1)
# solve: from first T = (3w+3)/0.18 ; plug into second
# 6w + 15 = 0.48*(3w+3)/0.18 = (8/3)(3w+3) = 8w + 8  -> w = 3.5
w = Fraction(7, 2)
T = (3 * w + 3 * kk) / Fraction(18, 100)
assert 6 * w + 15 * kk == Fraction(48, 100) * T
year = sum(w + (k - 1) * kk for k in range(1, 13))
excess = year - T
record('2026GK-80', {'A': 21, 'B': 28, 'C': 33, 'D': 44}, lambda v: v == excess, (w, T, year, excess), 'C')

# 2021GKD-70: day production = 0.6x + 1000*floor((d-1)/4) ; 80-day total = 88x ; first day cum>=1e6
# solve x: sum_{d=1..80} (0.6x + 1000*floor((d-1)/4)) = 48x + 1000*4*sum(0..19) = 88x
x = Fraction(1000 * 4 * sum(range(20)), 40)
cum = 0; dday = None
for d in range(1, 200):
    cum += Fraction(6, 10) * x + 1000 * ((d - 1) // 4)
    if cum >= 10**6:
        dday = d; break
record('2021GKD-70', {'A': 54, 'B': 56, 'C': 58, 'D': 60}, lambda v: v == dday, (x, dday), 'B')

# 2024ZJA-63: k-th expression: first = ((k-1)%4)+1 , second = 2k-1 ; sum = 2021
ks = [k for k in range(1, 5000) if ((k - 1) % 4 + 1) + (2 * k - 1) == 2021]
record('2024ZJA-63', {'A': 507, 'B': 1010, 'C': 1012, 'D': 1014}, lambda v: v in ks, ks, 'B')

# 2024ZJA-66: repeatedly remove odd positions (renumbered)
arr = list(range(1, 101))
while len(arr) > 1:
    arr = [arr[i] for i in range(len(arr)) if (i + 1) % 2 == 0]
record('2024ZJA-66', {'A': 32, 'B': 50, 'C': 64, 'D': 100}, lambda v: v == arr[0], arr, 'C')

# 2022SZ-60: newborn pair end of Jan; adult after 1 month; from then births every month
young, adult = 1, 0   # end of Jan
for month in range(2, 8):  # Feb..Jul ends
    young, adult = adult, adult + young   # adults give birth; young mature
total = young + adult
record('2022SZ-60', {'A': 8, 'B': 13, 'C': 21, 'D': 36}, lambda v: v == total, total, 'B')

# ---- reserve reals (classifier / easy) ----
n = next(n for n in range(1001, 5000) if n % 5 == 0 and (n + 3) % 4 == 0 and (n + 2) % 3 == 0 and (n + 1) % 2 == 0)
record('2026HB-68', {'A': 1015, 'B': 1025, 'C': 1035, 'D': 1045}, lambda v: v == n, n, 'D')
# 2026HB-76: B(/2) -> D(*3) -> A(+6) -> C(-5) = 13
xs = [x for x in [4, 6, 8, 12] if (x / 2) * 3 + 6 - 5 == 13]
record('2026HB-76', {'A': 4, 'B': 6, 'C': 8, 'D': 12}, lambda v: v in xs, xs, 'C')
record('2023GD-32', {'A': 32, 'B': 34, 'C': 36, 'D': 38}, lambda v: v % 3 == 2 and v % 4 == 2, None, 'D')
# 2022HB-68
sols = [(4 * b + 1, b, 4 * (4 * b + 1) + 1) for b in range(2, 90) if (4 * b + 1) + b + 4 * (4 * b + 1) + 1 == 90]
record('2022HB-68', {'A': 2, 'B': 3, 'C': 4, 'D': 5}, lambda v: v in [s[1] for s in sols], sols, 'C')
record('2020SZ1-51', {'A': 45, 'B': 46, 'C': 47, 'D': 48},
       lambda v: any(abs((10 * a + b) - (10 * b + a)) == v for a in range(1, 10) for b in range(0, 10)), None, 'A')
sols = [10 * t + u for t in range(1, 10) for u in range(0, 10) if t + u == 10 and (10 * t + u) - (10 * u + t) == 1796 - 1742]
record('2020JSA-62', {'A': 64, 'B': 73, 'C': 82, 'D': 91}, lambda v: v in sols, sols, 'C')
sols = [n for n in range(100, 1000) if sum(map(int, str(n))) == 19 and (n // 10) % 10 - n % 10 == 2
        and int(str(n)[::-1]) - n == 99]
record('2019JSA-58', {'A': 397, 'B': 586, 'C': 675, 'D': 964}, lambda v: v in sols, sols, 'B')
tot = sum(5000 + 100 * (d - 15) for d in range(1, 32))
record('2016ZJA-69', {'A': 163100, 'B': 158100, 'C': 155000, 'D': 150000}, lambda v: v == tot, tot, 'B')
# spiral turning numbers: walk the square spiral and record corners
def turning(nmax):
    # generate positions of 1..N on square spiral, turning numbers are where direction changes
    x = y = 0; dx, dy = 1, 0; seg = 1; num = 1; out = []
    # Ulam spiral: steps 1,1,2,2,3,3,...
    steps_list = []
    k = 1
    while len(steps_list) < 2 * nmax + 4:
        steps_list += [k, k]; k += 1
    for s in steps_list:
        num += s
        out.append(num)   # number at which direction changes
    return out
tn = turning(30)
record('2016JSA-70', {'A': 123, 'B': 131, 'C': 132, 'D': 133}, lambda v: v == tn[21], tn[:8] + [tn[21]], 'D')
nn = next(n for n in range(1, 100) if n * (n + 1) // 2 == 105)
record('2022HB-62', {'A': 3, 'B': 5, 'C': 8, 'D': 10}, lambda v: v == nn - 9, nn, 'B')
v = sum(int(str(8) * i) for i in range(1, 6))
record('2021HB-61', {'A': 9864, 'B': 9872, 'C': 98752, 'D': 98760}, lambda x: x == v, v, 'D')
sols = set()
for a in range(0, 100):
    for d in range(1, 60):
        ages = [a + i * d for i in range(4)]
        if sum(ages) == 142 and 47 in ages:
            sols.add(ages[-1])
record('2024JSA-56', {'A': 65, 'B': 70, 'C': 83, 'D': 90}, lambda v: v in sols, sols, 'B')
# 2020SD-42
for xx in range(1, 1000):
    a1 = 8 * xx  # from a+8x = 2a
    if a1 + 10 * xx == 900:
        break
tot = sum(a1 + i * xx for i in range(12))
record('2020SD-42', {'A': 7200, 'B': 7650, 'C': 8100, 'D': 8550}, lambda v: v == tot, tot, 'C')

# ---------------- TEACHER ----------------
# T019: 5 consecutive dates product 7893600
sols = [s + 4 for s in range(1, 28) if s * (s + 1) * (s + 2) * (s + 3) * (s + 4) == 7893600]
record('T019', {'A': 25, 'B': 26, 'C': 27, 'D': 28}, lambda v: v in sols, sols, 'B')
# T024: 4 consecutive ages, oldest <=30, product % 2700 == 0 and % 81 != 0
sols = [s + 3 for s in range(1, 28) if (s * (s + 1) * (s + 2) * (s + 3)) % 2700 == 0 and (s * (s + 1) * (s + 2) * (s + 3)) % 81 != 0]
record('T024', {'A': 25, 'B': 26, 'C': 27, 'D': 28}, lambda v: v in sols, sols, 'D')
# T208: 1-digit * 2-digit * 3-digit = 3930, min sum
best = min(a + b + c for a in range(1, 10) for b in range(10, 100) for c in range(100, 1000) if a * b * c == 3930)
record('T208', {'A': 144, 'B': 146, 'C': 148, 'D': 162}, lambda v: v == best, best, 'A')
# T209: product 2004
ss = {a + b + c for a in range(1, 10) for b in range(10, 100) for c in range(100, 1000) if a * b * c == 2004}
record('T209', {'A': 100, 'B': 180, 'C': 179, 'D': 178}, lambda v: v in ss, ss, 'B')
# T207: distinct numbers from 1..10, product 144 ; Zhang's sum > Li's
trip = [c for c in combinations(range(1, 11), 3) if c[0] * c[1] * c[2] == 144]
sums = sorted({sum(c) for c in trip})
record('T207', {'A': 19, 'B': 17, 'C': 16, 'D': 14}, lambda v: v == max(sums) and len(sums) == 2, (trip, sums), 'A')
# T210: lamps 51..100, switches 2,3,5 multiples, pressed once each
on = [k for k in range(51, 101) if (sum(1 for p in (2, 3, 5) if k % p == 0)) % 2 == 1]
record('T210', {'A': 22, 'B': 23, 'C': 26, 'D': 28}, lambda v: v == len(on), len(on), 'D')
# T211: players 1..50, floor 1 gives all one; floor k>=2 gives if n % k == 0 (k up to 60) ; exactly 3
cnt = sum(1 for n in range(1, 51) if 1 + sum(1 for k in range(2, 61) if n % k == 0) == 3)
record('T211', {'A': 1, 'B': 4, 'C': 7, 'D': 10}, lambda v: v == cnt, cnt, 'B')
# T212: <100 people, group sizes (N>1 groups, size>1) exactly 6 possibilities
ok = [n for n in range(2, 100) if len([d for d in divisors(n) if 1 < d < n]) == 6]
record('T212', {'A': 32, 'B': 48, 'C': 56, 'D': 64}, lambda v: v == max(ok) - min(ok), (ok, max(ok) - min(ok)), 'D')
# T213/T214
record('T213', {'A': 2, 'B': 6, 'C': 46, 'D': 92}, lambda v: v == len(divisors(92)), len(divisors(92)), 'B')
record('T214', {'A': 76, 'B': 120, 'C': 167, 'D': 168}, lambda v: v == sum(divisors(92)), sum(divisors(92)), 'D')
# T215: rectangles from 156 unit squares
rects = {(min(a, 156 // a), max(a, 156 // a)) for a in divisors(156)}
record('T215', {'A': 5, 'B': 6, 'C': 7, 'D': 8}, lambda v: v == len(rects), len(rects), 'B')
# T216
L = 60
record('T216', {'A': 37, 'B': 53, 'C': 74, 'D': 106}, lambda v: v == L // 4 + L // 5 + L // 6, None, 'A')
# T217: roses
tot = sum((2 if k % 2 == 0 else 0) + (3 if k % 3 == 0 else 0) + (1 if (k % 2 and k % 3) else 0) for k in range(1, 101))
record('T217', {'A': 215, 'B': 232, 'C': 312, 'D': 416}, lambda v: v == tot, tot, 'B')
# T218
n = next(n for n in range(1, 5000) if n % 3 == 2 and n % 5 == 3 and n % 7 == 2 and n % 11 == 8)
record('T218', {'A': 128, 'B': 233, 'C': 338, 'D': 443}, lambda v: v == n, n, 'C')
opt_ok = {k: (v % 3, v % 5, v % 7, v % 11) for k, v in {'A': 128, 'B': 233, 'C': 338, 'D': 443}.items()}
# T219
rs = {x % 12 for x in range(1, 1000) if x % 3 == 2 and x % 4 == 3}
record('T219', {'A': 1, 'B': 5, 'C': 9, 'D': 11}, lambda v: rs == {v}, rs, 'D')
# T220: x<100, (x-5)%4==0, (x+5)%7==0, max
xs = [x for x in range(-200, 100) if (x - 5) % 4 == 0 and (x + 5) % 7 == 0]
record('T220', {'A': 65, 'B': 89, 'C': 93, 'D': 97}, lambda v: v == max(xs), max(xs), 'C')
# T221: x in 200..299, x%3==0, (x+1)%5==0, (x+2)%7==0 ; day index (today = day1) when count % 13 == 0
xs = [x for x in range(200, 300) if x % 3 == 0 and (x + 1) % 5 == 0 and (x + 2) % 7 == 0]
assert len(xs) == 1
x = xs[0]
k = next(k for k in range(1, 40) if (x + k - 1) % 13 == 0)
record('T221', {'A': 9, 'B': 10, 'C': 11, 'D': 12}, lambda v: v == k, (x, k), 'B')
record('T018', {'A': 8, 'B': 9, 'C': 10, 'D': 11}, lambda v: v == k, (x, k), 'C')
# T223
sols = [n for n in range(100, 1000) if sum(map(int, str(n))) == 16 and (n // 10) % 10 == n % 10 - 3
        and int(str(n)[2] + str(n)[1] + str(n)[0]) - n == 495]
record('T223', {'A': 169, 'B': 358, 'C': 469, 'D': 736}, lambda v: v in sols, sols, 'B')
# T224: five-digit, left3 = 5*right2 ; moved = 2*orig + 75
sols = []
for r2 in range(10, 100):
    l3 = 5 * r2
    if 100 <= l3 <= 999:
        orig = l3 * 100 + r2
        new = r2 * 1000 + l3
        if new == 2 * orig + 75:
            sols.append(orig)
record('T224', {'A': 22545, 'B': 17535, 'C': 12525, 'D': 11575}, lambda v: v in sols, sols, 'C')
# T227: remove positions pattern even, even, odd, odd, even, even, ...
arr = list(range(1, 101)); t = 0
pat = ['even', 'even', 'odd', 'odd']
while len(arr) > 1:
    kind = pat[t % 4]
    if kind == 'even':
        arr = [arr[i] for i in range(len(arr)) if (i + 1) % 2 == 1]
    else:
        arr = [arr[i] for i in range(len(arr)) if (i + 1) % 2 == 0]
    t += 1
record('T227', {'A': 77, 'B': 53, 'C': 39, 'D': 27}, lambda v: v == arr[0], (arr, t), 'A')
# T142: 7 books AP integer, max 26, original total 100, paid extra (new total > 100) ;
# swapped one book: extra = new_price - old_price, new price <= 26 => extra < 26
mins = set()
for lo in range(1, 26):
    if (26 - lo) % 6 == 0:
        dd = (26 - lo) // 6
        if dd <= 0: continue
        prices = [lo + i * dd for i in range(7)]
        S = sum(prices)
        extra = S - 100
        # exists a book in new list (the new one) with price p and old price p-extra >0
        if extra > 0 and any(p - extra >= 1 for p in prices):
            mins.add(lo)
record('T142', {'A': 2, 'B': 6, 'C': 8, 'D': 14}, lambda v: v in mins, mins, 'C')
# T146: bonus 100,300,500,... -> 100 n^2 ; m^2+n^2 = 100, m,n>=1
sols = [(m, n) for m in range(1, 11) for n in range(m, 11) if m * m + n * n == 100]
record('T146', {'A': 15, 'B': 16, 'C': 17, 'D': 14}, lambda v: v in [m + n for m, n in sols], sols, 'D')
# T147: 1..n minus own rank = 70
sols = [(n, n * (n + 1) // 2 - 70) for n in range(1, 30) if 1 <= n * (n + 1) // 2 - 70 <= n]
record('T147', {'A': 7, 'B': 8, 'C': 9, 'D': 10}, lambda v: v in [s[1] for s in sols], sols, 'B')
# T150: rows 16..31 seats, no adjacent
tot = sum((s + 1) // 2 for s in range(16, 32))
record('T150', {'A': 188, 'B': 192, 'C': 196, 'D': 200}, lambda v: v == tot, tot, 'B')
# T145: geometric ratio 2, a_n - S_{n-1} = 5 -> a1 = 5
a1 = 5
record('T145', {'A': 70, 'B': 85, 'C': 80, 'D': 75}, lambda v: v == a1 * (1 + 2 + 4 + 8), None, 'D')
# T137
sols = [(a, a + 2, a + 4, a + 6) for a in range(-50, 50) if a % 2 and 4 * a + 12 == 32]
record('T137', {'A': 945, 'B': 1875, 'C': 2745, 'D': 3465}, lambda v: v == sols[0][0] * sols[0][1] * sols[0][2] * sols[0][3], sols, 'D')
# T140 / T141
record('T140', {'A': 8, 'B': 64, 'C': 32, 'D': 16}, lambda v: v == 2 ** 6, None, 'B')
mins_ = next(t for t in range(1, 20) if 2 ** t - 1 >= 50)
record('T141', {'A': 5, 'B': 6, 'C': 7, 'D': 8}, lambda v: v == mins_, mins_, 'B')
# T144
tot = sum(k for k in range(1, 65) if k % 3)
record('T144', {'A': 2408, 'B': 1387, 'C': 1408, 'D': 1487}, lambda v: v == tot, tot, 'B')
# T206
def nprime_factors(n):
    c = 0; p = 2
    while p * p <= n:
        while n % p == 0:
            n //= p; c += 1
        p += 1
    return c + (1 if n > 1 else 0)
first = next(n for n in range(100, 1000) if nprime_factors(n) == 3)
record('T206', {'A': 100, 'B': 102, 'C': 104, 'D': 105}, lambda v: v == first, first, 'B')
# T151: tetrahedral 7 layers
tot = sum(k * (k + 1) // 2 for k in range(1, 8))
record('T151', {'A': 60, 'B': 64, 'C': 80, 'D': 84}, lambda v: v == tot, tot, 'D')
# T152: white->black ; black->black+white ; row1 = white 1
w, b = 1, 0
for row in range(2, 11):
    w, b = b, b + w
record('T152', {'A': 34, 'B': 21, 'C': 13, 'D': 8}, lambda v: v == w, (w, b), 'B')

bad = 0
for k, (hits, value, expect, ok) in res.items():
    flag = 'OK ' if ok else '!! '
    if not ok: bad += 1
    print(flag, k, 'hits=', hits, 'expect=', expect, 'value=', value)
print('total', len(res), 'bad', bad)
print('T218 option residues (mod 3,5,7,11):', opt_ok)
