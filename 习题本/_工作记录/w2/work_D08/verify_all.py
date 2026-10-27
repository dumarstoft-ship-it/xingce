# Brute-force checks of every real item considered for D08 (M02).
from fractions import Fraction as F
from itertools import product
res = {}

def pick(val, opts):
    hits = [k for k, v in opts.items() if v == val]
    return hits

# 2026GD-43: a>b>c>d positive ints, a+b=100, b+c=96, c+d=80 -> d ?
sols = []
for b in range(1, 100):
    a, c = 100 - b, 96 - b
    d = 80 - c
    if min(a, b, c, d) >= 1 and a > b > c > d:
        sols.append((a, b, c, d))
res['2026GD-43'] = (sols, 'A' if len({s[3] for s in sols}) == 1 and sols[0][3] == 33 else '?')

# 2021SC2-50: zhang>all, li<all, wang>liu; z+w=34, w+l=20, l+li=16 -> z-w
sols = []
for w in range(1, 34):
    z, l = 34 - w, 20 - w
    li = 16 - l
    if min(z, w, l, li) >= 1 and z > max(w, l, li) and li < min(z, w, l) and w > l:
        sols.append((z, w, l, li, z - w))
res['2021SC2-50'] = sols

# 2023SD-40: 50% < m/n < 60%, min n
n = next(n for n in range(1, 50) if any(F(1, 2) < F(m, n) < F(3, 5) for m in range(n + 1)))
res['2023SD-40'] = n

# 2018ZJA-64: 13a+6b=83 -> spend 52a+34b
sols = [(a, b, 52 * a + 34 * b) for a in range(0, 10) for b in range(0, 20) if 13 * a + 6 * b == 83]
res['2018ZJA-64'] = sols

# 2021HB-74: max 60x+43y<=250
best = max((60 * x + 43 * y, x, y) for x in range(5) for y in range(6) if 60 * x + 43 * y <= 250)
res['2021HB-74'] = (best, best[0] / 250)

# 2020ZJB-11: 2*(50x+36y)=2220, x+y in 21..29
sols = [(x, y, x - y) for x in range(0, 30) for y in range(0, 30) if 2 * (50 * x + 36 * y) == 2220 and 21 <= x + y <= 29]
res['2020ZJB-11'] = sols

# 2025ZJA-62: 2pt attempts 8p (made 5p), 3pt attempts 9q (made 4q), p,q>=1, FT made f<=7, 10p+12q+f=25
sols = [(p, q, f, f / 7) for p in range(1, 4) for q in range(1, 4) for f in range(0, 8) if 10 * p + 12 * q + f == 25]
res['2025ZJA-62'] = sols

# 2020ZJB-13: right x, wrong y, blank z arithmetic progression; 10x-5y-3z=95; total in options
opts = {'A': 15, 'B': 30, 'C': 36, 'D': 45}
ok = []
for k, tot in opts.items():
    for x in range(0, tot + 1):
        for y in range(0, tot + 1 - x):
            z = tot - x - y
            if x - y == y - z and 10 * x - 5 * y - 3 * z == 95:
                ok.append((k, x, y, z))
res['2020ZJB-13'] = ok

# 2023ZJA-69: 30 x 2g, 8 x 5g; which w in 2..100 not representable
rep = {2 * a + 5 * b for a in range(31) for b in range(9)}
res['2023ZJA-69'] = [w for w in range(2, 101) if w not in rep]

# 2015JSA-34: total=22k+1, (k-1) groups equal size m<=32
sols = []
for k in range(2, 200):
    N = 22 * k + 1
    if N % (k - 1) == 0 and N // (k - 1) <= 32:
        sols.append((k, N, N // (k - 1)))
res['2015JSA-34'] = sols

# 2015JSA-38: B+W=193; B+15 = m(W-15)+6, m>=1; min B
sols = []
for W in range(16, 194):
    B = 193 - W
    Wp = W - 15
    rhs = B + 15 - 6
    if rhs % Wp == 0 and rhs // Wp >= 1:
        sols.append((B, W, rhs // Wp))
res['2015JSA-38'] = min(sols)

# 2017JSA-67: x+y+z=100, 300x+500y+2000z=36000, all >=1
sols = [(x, y, 100 - x - y) for x in range(1, 100) for y in range(1, 100) if 100 - x - y >= 1 and 300 * x + 500 * y + 2000 * (100 - x - y) == 36000]
res['2017JSA-67'] = sols
sols0 = [(x, y, 100 - x - y) for x in range(0, 101) for y in range(0, 101) if 100 - x - y >= 0 and 300 * x + 500 * y + 2000 * (100 - x - y) == 36000]
res['2017JSA-67_allow0'] = sols0

# 2016GK-63: a full, b 90%, c 50%; a+b+c=20; 2000a+1800b+1000c+20*170=27000
sols = [(a, b, 20 - a - b) for a in range(21) for b in range(21 - a) if 2000 * a + 1800 * b + 1000 * (20 - a - b) + 3400 == 27000]
res['2016GK-63'] = sols

# 2022JSA-61 (reserve): x+y+z=30, 10x+5y+z=89 -> z
sols = [(x, y, 30 - x - y) for x in range(31) for y in range(31 - x) if 10 * x + 5 * y + (30 - x - y) == 89]
res['2022JSA-61'] = sols

# 2025SC-51: a+b+c=2.3, 2a+b-c=2.2 -> a+3b+7c (solve with param b)
vals = set()
for b10 in range(0, 24):
    b = F(b10, 10)
    # a + c = 2.3 - b ; 2a - c = 2.2 - b -> 3a = 4.5 - 2b
    a = (F(45, 10) - 2 * b) / 3
    c = F(23, 10) - b - a
    vals.add(a + 3 * b + 7 * c)
res['2025SC-51'] = vals

# 2020SZ1-49: 11 works, 3 got 0 votes; votes 6,7,8; x 3-vote, y 2-vote, z 1-vote
# feasibility: need a 0/1 matrix 3 judges x 8 works with row sums 6,7,8 and column sums in {1,2,3}
from itertools import combinations
feas = []
for x in range(9):
    for y in range(9 - x):
        z = 8 - x - y
        if 3 * x + 2 * y + z != 21:
            continue
        cols = [3] * x + [2] * y + [1] * z
        # check realizable (Gale-Ryser for 3 rows)
        rows = sorted([6, 7, 8], reverse=True)
        ok = True
        for kk in range(1, 4):
            if sum(rows[:kk]) > sum(min(c, kk) for c in cols):
                ok = False
        feas.append((x, y, z, ok))
res['2020SZ1-49'] = feas

# 2023JSA-56: x+y+z=24, 3x+5y+8z=127, max y
sols = [(x, y, 24 - x - y) for x in range(25) for y in range(25 - x) if 3 * x + 5 * y + 8 * (24 - x - y) == 127]
res['2023JSA-56'] = (sols, max(s[1] for s in sols))

# 2024JSA-55: x+y+z=100, 888x+88y+8z=2480, min z
sols = [(x, y, 100 - x - y) for x in range(101) for y in range(101 - x) if 888 * x + 88 * y + 8 * (100 - x - y) == 2480]
res['2024JSA-55'] = (sols, min(s[2] for s in sols))

# 2018JSA-61: 17x+30y+40z=406, all>=1, max x+y+z
sols = [(x, y, z) for x in range(1, 24) for y in range(1, 14) for z in range(1, 11) if 17 * x + 30 * y + 40 * z == 406]
res['2018JSA-61'] = (sols, max(sum(s) for s in sols))

# 2020SC1206-50: 28a+32b+33c=400, max c (a,b>=0 and >=1 variants)
s0 = [(a, b, c) for a in range(15) for b in range(13) for c in range(13) if 28 * a + 32 * b + 33 * c == 400]
res['2020SC1206-50'] = (s0, max(s[2] for s in s0), max(s[2] for s in s0 if min(s) >= 1))

# 2025JSA-68: teachers t, students s=110-t, ropeway k<=110: 45s+70k=11750
sols = [(t, 110 - t, k) for t in range(111) for k in range(111) if 45 * (110 - t) + 70 * k == 11750]
res['2025JSA-68'] = sols

# T205: 24 | d5792? find first digit options among 3,5,7,9 with some last digit
okT = sorted({f for f in range(1, 10) for l in range(10) if int(f'{f}579{l}') % 24 == 0})
res['T205'] = okT

# 2019ZJA-76: R = M + S; S - S/3 = M + S/3 -> S=3M, R=4M, total 8M in 11..19
sols = [(4 * m, m, 3 * m, 4 * m * 1.0 + (m + 3 * m) * 0.6) for m in range(1, 5) if 10 < 8 * m < 20]
res['2019ZJA-76'] = sols

# 2020GKD-68: L = 0.8(Z+C), Z = 1.6C, total 300..399, then min add to make /7
sols = []
for C in range(1, 400):
    Z = F(16, 10) * C
    if Z.denominator != 1: continue
    L = F(8, 10) * (Z + C)
    if L.denominator != 1: continue
    T = int(L + Z + C)
    if 300 <= T <= 399:
        sols.append((int(L), int(Z), C, T, (-T) % 7))
res['2020GKD-68'] = sols

# 2022SD-41: N products: jia 5N/3, yi 3N/4, bing 7N/5 integers; total in [1000,1200]
sols = []
for N in range(1, 2000):
    if N % 3 or N % 4 or N % 5: continue
    j, y, b = 5 * N // 3, 3 * N // 4, 7 * N // 5
    if 1000 <= j + y + b <= 1200:
        sols.append((N, j, y, b, j + y + b))
res['2022SD-41'] = sols

# 2025SC-53: total n, red r; one sees r/(n-1)=1/5 (or (r-1)/(n-1)), other sees 2/11
sols = []
for n in range(2, 200):
    for r in range(0, n + 1):
        seen = {F(r, n - 1) if r <= n - 1 else None, F(r - 1, n - 1) if r >= 1 else None}
        if F(1, 5) in seen and F(2, 11) in seen:
            sols.append((n, r))
res['2025SC-53'] = sols

# 2024GKD-65: jia = 1.26 yi; bing-3 = yi+3; total 300..399; min y moved jia->bing so bing > 2*jia
sols = []
for yi in range(1, 400):
    jia = F(126, 100) * yi
    if jia.denominator != 1: continue
    bing = yi + 6
    T = int(jia) + yi + bing
    if 300 <= T <= 399:
        b2 = bing - 3
        ymin = next(y for y in range(0, 400) if b2 + y > 2 * (int(jia) - y))
        sols.append((int(jia), yi, bing, T, ymin))
res['2024GKD-65'] = sols

# 2021ZJA-57: small x (500,300,700 g), large y (700,1300,1000 g); grapes = 1/3 total; total > 300 kg; min dragonfruit
best = None
for x in range(0, 400):
    for y in range(0, 400):
        tot = 1500 * x + 3000 * y
        if tot <= 300000: continue
        if 3 * (300 * x + 1300 * y) != tot: continue
        dr = 500 * x + 700 * y
        if best is None or dr < best[0]:
            best = (dr, x, y)
res['2021ZJA-57'] = (best, best[0] / 1000)

# 2021JSA-61: male:female 7:3, grad:under 1:4, male_under = 4*female_grad; min (female_under - male_grad)
best = None
for N in range(10, 400, 10):
    male, fem, grad, und = 7 * N // 10, 3 * N // 10, N // 5, 4 * N // 5
    for fg in range(0, grad + 1):
        mu = 4 * fg
        mg = grad - fg
        fu = fem - fg
        if mu + mg != male or mu + fu != und or min(mu, mg, fu) < 0:
            continue
        d = fu - mg
        if d > 0 and (best is None or d < best[0]):
            best = (d, N, mu, mg, fu, fg)
res['2021JSA-61'] = best

# 2019GK-66: A + B in 301..399; A inv = 27% A; B inv:non = 8:13; B < A; B inv > A inv; min total non-inv
best = None
for A in range(1, 400):
    if (27 * A) % 100: continue
    Ainv = 27 * A // 100
    for k in range(1, 20):
        B = 21 * k
        if not (301 <= A + B <= 399) or not (B < A) or not (8 * k > Ainv):
            continue
        non = (A - Ainv) + 13 * k
        if best is None or non < best[0]:
            best = (non, A, B)
res['2019GK-66'] = best

# 2026GK-69 (reserve): A = 0.65 B, A+B+C=54
sols = [(int(F(65, 100) * B), B, 54 - B - int(F(65, 100) * B)) for B in range(1, 55) if (F(65, 100) * B).denominator == 1 and 54 - B - F(65, 100) * B >= 0]
res['2026GK-69'] = sols

# 2017GK-64 (reserve): 280a = 300b, min a
res['2017GK-64'] = next(a for a in range(1, 100) if (280 * a) % 300 == 0)

# 2026JS-66 (reserve): 2a+5b+8c=22, 3a+7b+11c=31.5 -> a+b+c
vals = set()
for c10 in range(0, 30):
    c = F(c10, 10)
    # 2a+5b = 22-8c ; 3a+7b = 31.5-11c
    det = 2 * 7 - 5 * 3
    a = ((22 - 8 * c) * 7 - 5 * (F(315, 10) - 11 * c)) / det
    b = (2 * (F(315, 10) - 11 * c) - 3 * (22 - 8 * c)) / det
    vals.add(a + b + c)
res['2026JS-66'] = vals

# 2021HB-62 (reserve): A,B,C sum 180; three rounds of doubling; final C = 7/26 final A
sols = []
for A in range(1, 180):
    for B in range(0, 180 - A):
        C = 180 - A - B
        a, b, c = A, B, C
        # day1 A gives to B,C doubling them
        a, b, c = a - b - c, 2 * b, 2 * c
        if a < 0: continue
        a, b, c = 2 * a, b - a - c, 2 * c
        if b < 0: continue
        a, b, c = 2 * a, 2 * b, c - a - b
        if c < 0: continue
        if 26 * c == 7 * a:
            sols.append((A, B, C, a, b, c))
res['2021HB-62'] = sols

for k, v in res.items():
    print(k, '=>', v)
