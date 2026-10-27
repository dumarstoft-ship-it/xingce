# Independent blind solver for w2_r2 (written before opening the key).
# Every answer is derived from stem data by brute force / enumeration, not by plugging options.
from itertools import product
from math import gcd
from fractions import Fraction as F


def lcm(a, b):
    return a * b // gcd(a, b)


res = {}

# ---------------- D08 v01: 48x + 60y = 2700, x>=1, y>=1, x>=y ----------------
sols = [(x, y) for x in range(0, 2701 // 48 + 1) for y in range(0, 2701 // 60 + 1)
        if 48 * x + 60 * y == 2700]
ok = [(x, y) for x, y in sols if x >= 1 and y >= 1 and x >= y]
res['D08-v01'] = len(ok)
print('D08 v01 correct count:', len(ok), ok)
# error paths
print('  ignore x>=y (both>=1):', len([1 for x, y in sols if x >= 1 and y >= 1]))
print('  strict x>y:', len([1 for x, y in sols if x >= 1 and y >= 1 and x > y]))
print('  allow zero, no order:', len(sols), ' allow zero with x>=y:', len([1 for x, y in sols if x >= y]))

# ---------------- D08 v02: 甲>乙>丙>丁, 甲=2丙, 甲+乙=57, 丙+丁=34 ----------------
cand = []
for c in range(1, 60):
    a, b, d = 2 * c, 57 - 2 * c, 34 - c
    if min(a, b, c, d) >= 1 and a > b > c > d:
        cand.append((a, b, c, d))
print('D08 v02 solutions (甲乙丙丁):', cand)
res['D08-v02'] = sorted(set(x[3] for x in cand))
# error path: drop 丙>丁 or make it non-strict
loose = [(2 * c, 57 - 2 * c, c, 34 - c) for c in range(1, 60)
         if 34 - c >= 1 and 2 * c > 57 - 2 * c > c]
print('  without 丙>丁:', loose)
nonstrict = [(2 * c, 57 - 2 * c, c, 34 - c) for c in range(1, 60)
             if 34 - c >= 1 and 2 * c > 57 - 2 * c > c >= 34 - c]
print('  丙>=丁:', nonstrict)

# ---------------- D11 v01: two sets with fractions ----------------
# R = 预约, N = 未预约.  补交 = R/4 + 2N/5 ; 补交 = R - 9 ; N*(3/5) = 45
sol = []
for R in range(0, 1000, 4):
    for N in range(0, 1000, 5):
        if N * 3 // 5 == 45 and R // 4 + 2 * N // 5 == R - 9:
            sol.append((R, N, R + N))
print('D11 v01 (R,N,total):', sol)
res['D11-v01'] = [s[2] for s in sol]
# error paths
for R in range(0, 1000, 4):
    for N in range(0, 1000, 5):
        if N == 45 and R // 4 + 2 * N // 5 == R - 9:
            print('  treat 45 as all non-reserved -> total', R + N)
        if N * 3 // 5 == 45 and 2 * N // 5 == R - 9:
            print('  forget reserved who need supplement -> total', R + N)
        if N * 3 // 5 == 45 and R // 4 + 2 * N // 5 == R + 9:
            print('  read 少9 as 多9 -> total', R + N)

# ---------------- D11 v02: standard three-set ----------------
# enumerate 7 regions + none, total 74
A, B, C = 38, 34, 28
AB, AC, BC = 17, 12, 8
none = 6
found = set()
for abc in range(0, 18):
    ab, ac, bc = AB - abc, AC - abc, BC - abc
    a = A - ab - ac - abc
    b = B - ab - bc - abc
    c = C - ac - bc - abc
    regs = [a, b, c, ab, ac, bc, abc]
    if min(regs) < 0:
        continue
    if sum(regs) + none == 74:
        found.add((abc, ab + ac + bc, a + b + c))
print('D11 v02 (abc, exactly-two, exactly-one):', found)
res['D11-v02'] = sorted(set(f[1] for f in found))

# ---------------- D11 v03: region drawing ----------------
# 7 regions: a(餐) b(浴) c(医) ab ac bc abc + none ; total 140, at least one = 85% -> 119
tot = 140
atl = tot * 85 // 100
assert tot * 85 % 100 == 0
none = tot - atl
cs = set()
cnt = 0
for abc in [5]:
    ab = 20 - abc
    # a,b,c,ac,bc >= 0 with a+b+c+ab+ac+bc+abc = atl ;  none + a + b + ab == a + b + c
    for a in range(0, atl + 1):
        for b in range(0, atl + 1 - a):
            for c in range(0, atl + 1 - a - b):
                rest = atl - (a + b + c + ab + abc)
                if rest < 0:
                    continue
                if none + a + b + ab != a + b + c:
                    continue
                cnt += 1
                cs.add(c)
print('D11 v03 only-医 values:', cs, '(#feasible region assignments over a,b,c:', cnt, ')')
res['D11-v03'] = sorted(cs)
print('  forget none in not-医:', 0 + 15, '; use 20 as ab-only:', none + 20, '; both errors:', 20)

# ---------------- D11 v04: inclusion + ratios ----------------
# sets U(无人机) T(拖拉机) X(旋耕机); 8 regions; X subset of T
ans = set()
for regs in product(range(0, 81), repeat=3):
    pass  # placeholder (enumerate smartly below)
sols4 = []
# regions: u (U only), t (T only), x (X only), ut (U&T not X), ux (U&X not T), tx (T&X not U), utx, none
u, ut, nn = 14, 10, 18
for t in range(0, 81):
    for tx in range(0, 81):
        for utx in range(0, 81):
            x, ux = 0, 0  # X subset of T  => X-only and U&X-not-T are empty
            total = u + t + x + ut + ux + tx + utx + nn
            if total != 80:
                continue
            Xn = x + ux + tx + utx
            Tn = t + ut + tx + utx
            if 2 * (ux + utx) != Xn:  # half of X have U
                continue
            if 3 * (tx + utx) != Tn:  # 1/3 of T have X
                continue
            sols4.append((t, tx, utx, u + ut + ux + utx))
print('D11 v04 (t, tx, utx, |U|):', sols4)
res['D11-v04'] = sorted(set(s[3] for s in sols4))
# error: forget 'none'
alt = []
for t in range(0, 81):
    for tx in range(0, 81):
        for utx in range(0, 81):
            if u + t + ut + tx + utx != 80:
                continue
            if 2 * utx != tx + utx or 3 * (tx + utx) != t + ut + tx + utx:
                continue
            alt.append(u + ut + utx)
print('  forget none ->', alt)

# ---------------- D11 v05: two-set extremum ----------------
best = None
rec = []
for both in range(0, 89):
    a_only, b_only = 88 - both, 79 - both
    if min(a_only, b_only) < 0:
        continue
    none = 126 - (a_only + b_only + both)
    if none < 0 or none > 16:
        continue
    ex1 = a_only + b_only
    rec.append((ex1, both, none))
mn = min(rec)
print('D11 v05 min exactly-one:', mn, ' max:', max(rec))
res['D11-v05'] = mn[0]
print('  ignoring none<=16 (none>=0 only):',
      min(88 - b + 79 - b for b in range(0, 80) if 126 - (167 - b) >= 0))

# ---------------- D11 v06: three-set extremum ----------------
# brute force over 7 regions with totals: X=48, Y=44, Z=7, total 58, everyone at least one
best6 = None
arg6 = None
Z = 7
for z in range(0, Z + 1):            # Z only
    for xz in range(0, Z + 1 - z):   # X&Z only
        for yz in range(0, Z + 1 - z - xz):
            xyz = Z - z - xz - yz
            # remaining: x (X only), y (Y only), xy (X&Y only)
            # x + xy = 48 - xz - xyz ; y + xy = 44 - yz - xyz ; x+y+xy+z+xz+yz+xyz = 58
            X_rest = 48 - xz - xyz
            Y_rest = 44 - yz - xyz
            S = 58 - z - xz - yz - xyz    # x + y + xy
            xy = X_rest + Y_rest - S
            x_ = X_rest - xy
            y_ = Y_rest - xy
            if min(xy, x_, y_) < 0:
                continue
            ge2 = xy + xz + yz + xyz
            if best6 is None or ge2 < best6:
                best6, arg6 = ge2, (x_, y_, z, xy, xz, yz, xyz)
print('D11 v06 min >=2:', best6, arg6)
res['D11-v06'] = best6

# ---------------- D11 v07: periodic + inclusion-exclusion ----------------
def exactly_one(periods, days=61):
    c = 0
    for d in range(days):
        k = sum(1 for p in periods if d % p == 0)
        if k == 1:
            c += 1
    return c


def stats(periods, days=61):
    out = {}
    for d in range(days):
        k = sum(1 for p in periods if d % p == 0)
        out[k] = out.get(k, 0) + 1
    return out

# "每隔n天" = period n+1 (real-exam convention: 2015GK-72, 2016JSA-67, 2016GK-66, 2025JSA-69)
days = 30 + 31   # June 1 .. July 31 inclusive
p_conv = [7 + 1, 9 + 1, 11 + 1]
p_naive = [7, 9, 11]
print('D11 v07 period n+1:', exactly_one(p_conv, days), stats(p_conv, days))
print('        period n  :', exactly_one(p_naive, days), stats(p_naive, days))
res['D11-v07'] = exactly_one(p_conv, days)

print()
print('SUMMARY', res)
