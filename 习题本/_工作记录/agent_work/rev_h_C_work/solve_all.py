# Independent blind solver for revh_C (D01 math hard replacements), written from the stems only.
from fractions import Fraction as F
import itertools

res = {}

def pick(opts, val):
    hits = [k for k, v in opts.items() if v == val]
    return hits

# v01: a (甲), b (乙); scheme1: b+35 = 3(a-35); scheme2: a+40 = 2(b-40); schemes are alternatives
sols = []
for a in range(36, 1000):
    for b in range(41, 1000):
        if b + 35 == 3 * (a - 35) and a + 40 == 2 * (b - 40):
            sols.append((a, b))
print('v01', sols)
# misreading: sequential
seq = []
for a in range(36, 1000):
    for b in range(0, 1000):
        a1, b1 = a - 35, b + 35
        if b1 == 3 * a1:
            a2, b2 = a1 + 40, b1 - 40
            if b2 > 0 and a2 == 2 * b2:
                seq.append((a, b))
print('v01 sequential misread', seq)
res['v01'] = sols

# v02: x first; second 0.8x; third = x+0.8x-30; fourth = 1.5x+15; max-min = 50; all positive integers
sols = []
for x5 in range(1, 2000):
    x = F(x5)  # integer orders
    s = [x, F(4, 5) * x, x + F(4, 5) * x - 30, F(3, 2) * x + 15]
    if any(v.denominator != 1 or v <= 0 for v in s):
        continue
    if max(s) - min(s) == 50:
        sols.append((x, [int(v) for v in s], int(sum(s))))
print('v02', sols)
# distractor checks
for name, (hi, lo) in {'max=3rd,min=2nd': (2, 1), 'max=4th,min=1st': (3, 0), 'max=4th,min=2nd': (3, 1)}.items():
    for x in range(1, 2000):
        s = [F(x), F(4, 5) * x, F(9, 5) * x - 30, F(3, 2) * x + 15]
        if s[hi] - s[lo] == 50 and all(v.denominator == 1 for v in s):
            print('   v02 assume', name, 'x=', x, [int(v) for v in s], 'total', int(sum(s)), 'actual max-min', max(s) - min(s))

# v03: 甲=(乙+丙)/3, 乙=(甲+丙)/4, 丙-乙=126
sols = []
for j in range(1, 2000):
    for y in range(1, 2000):
        b = y + 126
        if 3 * j == y + b and 4 * y == j + b:
            sols.append((j, y, b))
print('v03', sols)

# v04: T total, 0.15T dispatch; remove 20 -> ratio 10%
sols = []
for T in range(1, 5000):
    d = F(15, 100) * T
    if d.denominator != 1:
        continue
    if (d - 20) * 10 == (T - 20):
        sols.append((T, d))
print('v04', sols)

# v05: brute force on integer populations
sols = set()
for a in range(1, 60):          # 甲: planters 2a, breeders a
    for b in range(1, 60):      # 乙: planters b, breeders 2b
        if (2 * a + b) * 4 != (a + 2 * b) * 5:
            continue
        sp = F(1, 4) * 2 * a + F(1, 2) * b
        sb = F(1, 3) * a + F(2, 3) * 2 * b
        if any(v.denominator != 1 for v in (sp, sb)):
            continue
        r = sp / sb
        sols.add((r.numerator, r.denominator))
print('v05 ratios planters:breeders with shops', sols)
# equal-size misread
a = b = 6
sp = F(1, 4) * 2 * a + F(1, 2) * b; sb = F(1, 3) * a + F(2, 3) * 2 * b
print('   v05 if equal sizes', sp / sb)

# v06: M same; M/300 = p1, M/400 = p2, M/480 = p2 - 2
sols = []
for M100 in range(1, 100000):
    M = F(M100, 10)
    p1, p2, p3 = M / 300, M / 400, M / 480
    if p2 - p3 == 2:
        sols.append((M, p1, p2, p3))
print('v06', sols)

# v07: weights 甲 30*12, 乙 80*3 + 40*9, 丙 80*3 (Oct, Nov, Dec)
wj = 30 * 12
wy = 80 * 3 + 40 * 9
wb = 80 * 3
dist = F(16) * (wj + wy + wb) / wb
profit = dist / F(8, 10)
print('v07 weights', wj, wy, wb, 'distributable', dist, 'profit', profit)
# misreads
print('   v07 forget 20%:', dist, '; 乙 not reduced:', F(16) * (wj + 80 * 12 + wb) / wb / F(8, 10))

# v08: 本院 3k, 分院 k; transfer t: (3k-t):(k+t)=7:3; then 分院+20: (3k-t):(k+t+20)=3:2
sols = []
for k in range(1, 1000):
    for t in range(1, 3 * k):
        if 3 * (3 * k - t) == 7 * (k + t) and 2 * (3 * k - t) == 3 * (k + t + 20):
            sols.append((3 * k, k, t))
print('v08 (本院, 分院, 抽调)', sols)

# v09: 2024-08 = 100
a24_8 = F(100)
a24_9 = a24_8 * F(8, 10)
a25_9 = a24_9 * F(12, 10)
a25_8 = a25_9 / F(75, 100)
print('v09 growth', (a25_8 / a24_8 - 1) * 100, '%')

# v10: 其余 x, 露天 4x/3; gloves 6N+50 = 8*露天 + 5*其余
sols = []
for x in range(1, 3000):
    o = F(4, 3) * x
    if o.denominator != 1:
        continue
    N = x + o
    if 6 * N + 50 == 8 * o + 5 * x:
        sols.append((int(N), int(o), x, int(6 * N + 50)))
print('v10 (N, outdoor, other, gloves)', sols)

# v11: n rooms; S = 4n + 18; with 6 per room: exactly one room partially filled (1..5), others full, none empty
sols = []
for n in range(1, 500):
    S = 4 * n + 18
    # n-1 rooms full of 6, one room with r in 1..5
    r = S - 6 * (n - 1)
    if 1 <= r <= 5:
        sols.append((n, S, r))
print('v11', sols, 'max', max(s[1] for s in sols))

# v12: 甲 a, 乙 a-4, 丙 a+7; groups x (甲), 8 (乙), z (丙). After: 甲 a-x+z, 乙 a-4-8+x, 丙 a+7-z+8
sols = set()
for a in range(13, 200):
    for x in range(1, a):
        for z in range(1, a + 7):
            A, B, C = a - x + z, a - 12 + x, a + 15 - z
            if A == B == C:
                sols.add(x)
print('v12 甲 group size', sols)

# v13: forward simulate all integer splits
sols = []
for a in range(0, 201):
    for b in range(0, 201 - a):
        c = 200 - a - b
        A, B, C = a, b, c
        ok = True
        # step1: A gives B,C doubling
        give = B + C
        if give > A or B == 0 or C == 0:
            ok = False
        A, B, C = A - give, 2 * B, 2 * C
        if ok:
            give = A + C
            if give > B or A == 0 or C == 0:
                ok = False
            A, B, C = 2 * A, B - give, 2 * C
        if ok:
            give = A + B
            if give > C or A == 0 or B == 0:
                ok = False
            A, B, C = 2 * A, 2 * B, C - give
        if ok and 8 * C == 7 * A:
            sols.append(((a, b, c), (A, B, C)))
print('v13 strict-positive solutions', sols)
# allow zero holdings (degenerate)
sols0 = []
for a in range(0, 201):
    for b in range(0, 201 - a):
        c = 200 - a - b
        A, B, C = a, b, c
        A, B, C = A - B - C, 2 * B, 2 * C
        if A < 0: continue
        A, B, C = 2 * A, B - A - C, 2 * C
        if B < 0: continue
        A, B, C = 2 * A, 2 * B, C - A - B
        if C < 0: continue
        if 8 * C == 7 * A:
            sols0.append(((a, b, c), (A, B, C)))
print('v13 nonneg (incl. degenerate)', sols0)
# continuous family: check option values with real numbers
for a in (104, 107, 108, 116):
    c = F(7 * a - 500, 8); b = 200 - a - c
    A1, B1, C1 = a - b - c, 2 * b, 2 * c
    A2, B2, C2 = 2 * A1, B1 - A1 - C1, 2 * C1
    A3, B3, C3 = 2 * A2, 2 * B2, C2 - A2 - B2
    print('   v13 option a=', a, 'b,c=', b, c, 'states', (A1, B1, C1), (A2, B2, C2), (A3, B3, C3))

# v14: x 甲, y 乙, z 丙
sols = []
for x in range(0, 301):
    for y in range(0, 301 - x):
        z = 300 - x - y
        if 60 * x == 40 * y and 60 * x + 40 * y + 80 * z == 18400:
            sols.append((x, y, z))
print('v14', sols)

# v15: big x, small y; W = 5(5x+2y) = 6(2x+6y)
import math
sols = set()
for y in range(1, 200):
    for x in range(1, 400):
        if 5 * (5 * x + 2 * y) == 6 * (2 * x + 6 * y):
            W = 5 * (5 * x + 2 * y)
            sols.add((F(x, y), F(W, 8 * x), math.ceil(F(W, 8 * x))))
print('v15 (x:y, W/(8x), trips)', sols)

# v16: brute force positive solutions; check m+p+i invariant
vals = set()
for m in range(1, 60):
    for p in range(1, 30):
        i = 190 - 4 * m - 7 * p
        if i <= 0: continue
        if 5 * m + 9 * p + i == 240:
            vals.add(m + p + i)
print('v16 m+p+i over all positive integer solutions', vals)

# v17
rate = F(150, 50)
seg = [(18, ['甲', '乙']), (20, ['甲', '乙', '丙']), (12, ['乙', '丙'])]
pay = {'甲': 0, '乙': 0, '丙': 0}
for d, ppl in seg:
    for p in ppl:
        pay[p] += rate * d / len(ppl)
print('v17', pay)

# v18: n people, rent R
sols = []
for n in range(3, 500):
    for R in range(1, 20001):
        if R * 2 % (n * (n + 2)) == 0:
            pass
        p = F(R, n)
        if F(R, n + 2) == p - 30 and F(R, n - 2) == p + 50:
            sols.append((n, R, p))
print('v18', sols)
