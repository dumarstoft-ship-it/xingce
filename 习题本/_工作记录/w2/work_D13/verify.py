"""D13 (M13) answer verification: brute force / direct computation from stem data."""
from fractions import Fraction as F
import datetime as dt
from itertools import product

res = {}

def chk(name, got, expect):
    res[name] = (got, expect, got == expect)
    print(f"{name:16s} got={got!s:28s} expect={expect!s:10s} {'OK' if got == expect else '<<< MISMATCH'}")

# ---------------- 周期 ----------------
# 2025SD-55: Wang every 10 days ("隔9天"), Liu on Sat/Sun; day0 = Sunday both. next common day d>0; ask "再隔多少天" = d-1
def sd55():
    for d in range(1, 200):
        if d % 10 == 0 and d % 7 in (6, 0):  # day0 Sunday -> d%7==6 Saturday, 0 Sunday
            return d - 1
opts = {'A': 19, 'B': 20, 'C': 21, 'D': 22}
v = sd55(); chk('2025SD-55', [k for k, x in opts.items() if x == v], ['A'])

# 2023GD-40: 12 people cyclic; day k uses positions 5(k-1)+1..+5 (mod 12); first two security.
def sec_days(maxday=200):
    out = []
    for k in range(1, maxday):
        base = 5 * (k - 1)
        s = {(base) % 12 + 1, (base + 1) % 12 + 1}
        if 1 in s:
            out.append(k)
    return out
sd = sec_days()
gaps = sorted(set(b - a for a, b in zip(sd, sd[1:])))
chk('2023GD-40', max(gaps), 7)  # option C=7

# 2017GK-63: workdays rotate among 4; July 5 (Fri) Xiaoling; next Monday on which Xiaoling cleans.
def gk63():
    year = 2019  # July 5 2019 is Friday
    d0 = dt.date(year, 7, 5)
    assert d0.weekday() == 4
    idx = 0
    d = d0
    while True:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            idx += 1
            if idx % 4 == 0 and d.weekday() == 0:
                return f"{d.month}/{d.day}"
chk('2017GK-63', gk63(), '7/29')

# T171 bikes: 100 bikes before 7:00; from 7:00 every 20s one leaves; 7:00 +30, every 15 min +30.
def t171():
    stock = 100
    empty = []
    # simulate in seconds from 7:00
    for s in range(0, 3 * 3600):
        if s % 900 == 0:
            stock += 30
        if s % 20 == 0 and s > 0:
            if stock > 0:
                stock -= 1
        if stock == 0:
            empty.append(s)
    first = empty[0]
    return first
f = t171(); hh = 7 + f // 3600; mm = (f % 3600) / 60
print('   T171 first empty at', hh, mm)
chk('T171', 'C' if (hh == 8 and 41 <= mm < 45) or (hh == 8 and 43 <= mm <= 45) else '?', 'C')

# 2019ZJA-77: Liu period 4 (3 on 1 off), Zhang period 5 (2 on 3 off); May 31 days; exactly 11 common days
def zja77():
    cases = []
    for a in range(4):
        for b in range(5):
            common = [d for d in range(1, 32) if (d - a) % 4 in (0, 1, 2) and (d - b) % 5 in (0, 1)]
            if len(common) == 11:
                cases.append(set(common))
    inter = set.intersection(*cases)
    return cases, inter
cases, inter = zja77()
print('   2019ZJA-77 cases:', [sorted(c) for c in cases], 'intersection', sorted(inter))
opts = {'A': 2, 'B': 4, 'C': 8, 'D': 11}
chk('2019ZJA-77', [k for k, x in opts.items() if x in inter], ['D'])

# ---------------- 星期日期（一） ----------------
# 2024GD-40: March has 5 Saturdays -> possible weekday of April 1
def gd40():
    poss = set()
    for w in range(7):  # weekday of March 1, 0=Mon
        sats = sum(1 for d in range(31) if (w + d) % 7 == 5)
        if sats == 5:
            poss.add((w + 31) % 7)
    return poss
names = ['一', '二', '三', '四', '五', '六', '日']
p = gd40(); print('   2024GD-40 April1 possible:', [names[x] for x in sorted(p)])
opts = {'A': 1, 'B': 2, 'C': 4, 'D': 5}
chk('2024GD-40', [k for k, x in opts.items() if x in p], ['A'])

# 2025GK-75: Mon-Fri 1, Sat/Sun 2; days 1-16 total 22 -> weekday of the 8th
def gk75():
    out = set()
    for w in range(7):
        tot = sum(2 if (w + d) % 7 in (5, 6) else 1 for d in range(16))
        if tot == 22:
            out.add((w + 7) % 7)
    return out
p = gk75(); print('   2025GK-75 8th:', [names[x] for x in p])
opts = {'A': 2, 'B': 3, 'C': 4, 'D': 5}
chk('2025GK-75', [k for k, x in opts.items() if x in p], ['D'])

# 2023SZ-59: work Tue-Sat; 31-day month; worked 22 days -> weekday of 4th
def sz59():
    out = set()
    for w in range(7):
        work = sum(1 for d in range(31) if (w + d) % 7 in (1, 2, 3, 4, 5))
        if work == 22:
            out.add((w + 3) % 7)
    return out
p = sz59(); print('   2023SZ-59 4th:', [names[x] for x in sorted(p)])
chk('2023SZ-59', sorted(p) == [0, 3], True)  # Mon or Thu -> option C

# 2025GKX-71: runs Mon-Thu; Feb 17, Mar 19 -> April count
def gkx71():
    outs = set()
    for w in range(7):  # weekday of Feb 1
        for feb in (28, 29):
            febc = sum(1 for d in range(feb) if (w + d) % 7 in (0, 1, 2, 3))
            m1 = (w + feb) % 7
            marc = sum(1 for d in range(31) if (m1 + d) % 7 in (0, 1, 2, 3))
            a1 = (m1 + 31) % 7
            aprc = sum(1 for d in range(30) if (a1 + d) % 7 in (0, 1, 2, 3))
            if febc == 17 and marc == 19:
                outs.add(aprc)
    return outs
chk('2025GKX-71', gkx71(), {16})

# ---------------- 星期日期（二） ----------------
# 2026GK-78: Monday meeting; visits on 10th and 20th; Aug+Sep exactly 2 coincidences -> Sep 1 weekday
def gk78():
    out = set()
    for w in range(7):  # weekday of Aug 1 (0=Mon)
        dates = []
        for d in (10, 20):
            dates.append((w + d - 1) % 7)
        s1 = (w + 31) % 7  # Sep 1
        for d in (10, 20):
            dates.append((s1 + d - 1) % 7)
        if sum(1 for x in dates if x == 0) == 2:
            out.add(s1)
    return out
p = gk78(); print('   2026GK-78 Sep1:', [names[x] for x in p])
opts = {'A': 2, 'B': 1, 'C': 5, 'D': 4}
chk('2026GK-78', [k for k, x in opts.items() if x in p], ['C'])

# 2020SZS-17: torn 10 pages (the 10 days before today) sum 244 -> today's date
def szs17():
    out = set()
    for prev_len in (28, 29, 30, 31):
        # today = date t in current month (1..31); the 10 previous days
        for t in range(1, 32):
            days = []
            for k in range(1, 11):
                x = t - k
                days.append(x if x >= 1 else prev_len + x)
            if sum(days) == 244:
                out.add((t, prev_len))
    return out
p = szs17(); print('   2020SZS-17 (today, prev month len):', p)
chk('2020SZS-17', sorted({t for t, _ in p}), [2])

# T161: Mon-Fri gym; every quarter same count -> National Day weekday
def t161():
    out = set()
    for year in range(1990, 2060):
        cnt = []
        for q in range(4):
            s = dt.date(year, 3 * q + 1, 1)
            e = dt.date(year + (q == 3), (3 * q + 4) % 12 or 12, 1) if q < 3 else dt.date(year + 1, 1, 1)
            c = 0; d = s
            while d < e:
                if d.weekday() < 5:
                    c += 1
                d += dt.timedelta(days=1)
            cnt.append(c)
        if len(set(cnt)) == 1:
            out.add(dt.date(year, 10, 1).weekday())
    return out
p = t161(); print('   T161 Oct1:', [names[x] for x in p])
chk('T161', p, {6})

# T162: July 1 Wed; reading Mon-Fri from plan day; 20/night -> done Jul 28, 30/night -> done Jul 20
def t162():
    out = []
    w1 = 2  # Jul 1 Wednesday (0=Mon)
    wd = lambda d: (w1 + d - 1) % 7
    for start in range(1, 21):
        n20 = sum(1 for d in range(start, 29) if wd(d) < 5)
        n30 = sum(1 for d in range(start, 21) if wd(d) < 5)
        if 20 * n20 == 30 * n30 and wd(28) < 5 and wd(20) < 5:
            out.append(start)
    return out
p = t162(); print('   T162 start days:', p)
chk('T162', p, [3])

# ---------------- 年龄 ----------------
def t013():
    for c in range(1, 100):
        a = 3 * c
        if F(a + 9) == F(12, 5) * (c + 9):
            b = F(a + c, 2)
            for t in range(0, 50):
                if F(c + t) / (b + t) == F(4, 7):
                    return t
chk('T013', t013(), 7)

def gk61():
    for k in range(1, 30):
        a, b, c = 3 * k, 4 * k, 5 * k
        if (a + 8) + (b + 8) == F(3, 2) * (c + 8):
            d8 = 43 * 4 - (a + 8) - (b + 8) - (c + 8)
            ages = [a + 23, b + 23, c + 23, d8 + 15]
            return sum(1 for x in ages if x > 60)
chk('2024GK-61', gk61(), 2)

def gk70():
    best = None
    for a in range(0, 100):
        for b in range(0, a):
            for c in range(0, b):
                if a + b + c == a + 10 and a - b > b - c:
                    best = a if best is None else min(best, a)
    return best
chk('2025GK-70', gk70(), 9)

def gd44():
    out = []
    for d in range(1, 20):  # Wang older by d
        for now_b in range(20, 80):  # brother's age now
            # brother started at 20; Wang started 2 years before brother started -> Wang age at start
            wang_start_age = 20 + d - 2
            if now_b != wang_start_age:
                continue
            now_w = now_b + d
            gl_b = now_b - 20
            gl_w = now_w - wang_start_age
            if gl_b >= 0 and now_b + now_w == 8 * (gl_b + gl_w):
                out.append(d)
    return out
chk('2025GD-44', gd44(), [4])

def zja70():
    out = []
    for x in range(1, 30):  # Li's work years in 2020
        li = 4 * x
        if li * 3 % 2: continue
        zh = F(li * 3, 2)
        if zh.denominator != 1: continue
        zh = int(zh)
        zgl2024 = F(zh + 4, 2)
        if zgl2024.denominator != 1: continue
        zgl2020 = int(zgl2024) - 4
        # Zhang started work zgl2020 years before 2020 -> Li's age then
        if li - zgl2020 == 10:
            out.append(li - x)
    return out
chk('2022ZJA-70', zja70(), [24])

# ---------------- 植树与方阵 ----------------
def gd36():
    return 4 + 2 * (10 // 3 - 1) + 2 * (8 // 3 - 1)
chk('2022GD-36', gd36(), 10)

def gd43():
    a = [x for x in range(4, 100, 4)]
    b = set(range(6, 100, 6))
    return len([x for x in a if x not in b])
chk('2024GD-43', gd43(), 16)

def szs22():
    old = set(range(0, 400, 16))
    best = 0
    for d in range(1, 16):
        if 400 % d: continue
        for off in range(0, d):
            new = set(range(off, 400 + off, d))
            new = {x % 400 for x in new}
            if len(old & new) == 5:
                best = max(best, d)
    return best
chk('2020SZS-22', szs22(), 10)

def sz59b():
    out = []
    for Y in range(9, 60):  # yellow side
        k2 = Y - 8
        if k2 <= 0 or k2 % 2: continue
        yellow = Y * Y - 64
        green = (Y - 4) ** 2
        if 64 + green == yellow:
            out.append(yellow)
    return out
chk('2024SZ-59', sz59b(), [260])

def gk75b():
    tri = {n * (n + 1) // 2 for n in range(1, 200)}
    for N in range(6, 2000):
        m = round((N - 4) ** 0.5)
        if m >= 2 and m * m == N - 4 and N + 5 in tri:
            per = min(2 * (a + N // a) - 4 for a in range(2, int(N ** 0.5) + 1) if N % a == 0)
            return N, per
print('   2019GK-75 N, min outer:', gk75b())
chk('2019GK-75', gk75b()[1], 22)

# ---------------- 钟表 ----------------
def ang(h, m):  # minutes past h o'clock (m may be fractional) -> smaller angle
    a = abs(30 * h + 0.5 * m - 6 * m) % 360
    return min(a, 360 - a)

def hb73():
    ts = [F(m) for m in []]
    sols = []
    # theta = minute - hour = 6m - (150 + 0.5m) = 5.5m - 150 ; angle 110 -> 5.5m-150 = +-110
    for target in (-110, 110):
        m = F(target + 150) / F(11, 2)
        if 0 <= m < 60:
            sols.append(m)
    return sols[1] - sols[0]
chk('2021HB-73', hb73(), 40)

def sc52():
    # start 8:xx with angle <= 30; end 10:xx overlap
    end = F(300) / F(11, 2)  # minutes past 10
    # theta(8:m) = 5.5m - 240 (mod 360); angle<=30 -> 5.5m-240 in [-30,30] (mod 360) -> m in [210/5.5, 270/5.5]
    lo, hi = F(210) / F(11, 2), F(270) / F(11, 2)
    dmin = 120 + end - hi
    dmax = 120 + end - lo
    opts = {'A': 125, 'B': 135, 'C': 145, 'D': 155}
    return [k for k, v in opts.items() if dmin <= v <= dmax], float(dmin), float(dmax)
r = sc52(); print('   2024SC-52 range(min):', r[1:])
chk('2024SC-52', r[0], ['B'])

def t065():
    # time t (min) such that hour hand moves from pos1 to pos2 and minute from pos2 to pos1 -> 0.5t + 6t = 360k
    return F(720, 13)
print('   T065 minutes:', float(t065()))
chk('T065', 'B' if abs(float(t065()) - 55) < 1 else '?', 'B')

def sz60():
    # leave 7:xx angle 90 (earliest), return 12:xx angle 90 (latest); count 180 deg in between
    def times(h, target):
        out = []
        for k in range(-3, 4):
            for s in (1, -1):
                m = (F(s * target) + 30 * h + 360 * k) / F(11, 2)
                if 0 <= m < 60:
                    out.append(m)
        return sorted(set(out))
    leave = min(times(7, 90)); back = max(times(0, 90))  # 12 o'clock -> h=0 in formula
    start = 7 * 60 + leave; end = 12 * 60 + back
    cnt = 0
    for h in range(7, 13):
        for m in times(h % 12, 180):
            t = h * 60 + m
            if start < t < end:
                cnt += 1
    return cnt
chk('2024SZ-60', sz60(), 5)

# ---------------- 杂题 ----------------
def zja74():
    # n students, ranks; Zhang rank z, Li rank l (1 = best)
    ok = set()
    for n in range(3, 60):
        for z in range(1, n + 1):
            for l in range(1, n + 1):
                if z == l: continue
                x = (z - 1) + (n - l)
                y = (n - z) + (l - 1)
                if x > 0 and 2 * y == 3 * x:
                    ok.add(F(n) - F(5, 4) * x)
    return ok
chk('2021ZJA-74', zja74(), {1})

def jsa66():
    from itertools import combinations
    teams = range(5)
    games = list(combinations(teams, 2))
    seconds = set()
    for res_ in product((0, 1, 2), repeat=len(games)):  # 0 i wins, 1 draw, 2 j wins
        pts = [0] * 5
        for (i, j), r in zip(games, res_):
            if r == 0: pts[i] += 3
            elif r == 2: pts[j] += 3
            else: pts[i] += 1; pts[j] += 1
        if sum(pts) == 25 and max(pts) == 12:
            s = sorted(pts, reverse=True)
            if s[0] > s[1]:
                seconds.add(s[1])
    return seconds
chk('2022JSA-66', jsa66(), {5})

def jsa64():
    out = []
    for n in range(1, 10):
        m = 10 * n
        tot = (11 * n) * (11 * n - 1)  # 2 points per game
        fem = F(tot, 11, ) / F(11, 2) if False else F(tot) / F(11, 2)
        fem_max = 2 * n * m + n * (n - 1)
        if fem.denominator == 1 and fem <= fem_max:
            out.append(m)
    return out
chk('2018JSA-64', jsa64(), [10])

print()
bad = [k for k, v in res.items() if not v[2]]
print('ALL OK' if not bad else f'MISMATCH: {bad}')
