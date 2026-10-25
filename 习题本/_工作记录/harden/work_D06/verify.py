"""Brute-force / exact checks for D06 harden decision (real adds, teacher adds, new-variant ideas)."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, factorial, sqrt

def show(name, val, expect=None):
    ok = '' if expect is None else ('OK' if val == expect else f'MISMATCH (expect {expect})')
    print(f'{name:<28} {val} ~ {float(val):.4f} {ok}')

# ---------- real additions ----------
# 2025GD-45: 3 people each draw 2 of 6 questions; exactly one question undrawn
pairs = list(combinations(range(6), 2))
fav = sum(1 for a, b, c in product(pairs, repeat=3) if len(set(a) | set(b) | set(c)) == 5)
show('2025GD-45', F(fav, len(pairs) ** 3), F(1080, 3375))

# 2025HB-71: white = 8 triangles (leg 1), total = (2+sqrt2)^2
print('2025HB-71 white share', 4 / (2 + sqrt(2)) ** 2, '6-4*sqrt2 =', 6 - 4 * sqrt(2))

# 2024ZJA-62: Zhang order random with Jia@2, Ding@4; Wang random with Yi@3
qs = '甲乙丙丁戊'
Z = [p for p in permutations(qs) if p[1] == '甲' and p[3] == '丁']
W = [p for p in permutations(qs) if p[2] == '乙']
show('2024ZJA-62', F(sum(1 for z in Z for w in W if z == w), len(Z) * len(W)), F(1, 72))

# 2023GK-71: 甲乙 not first/last, 丙 3rd or 4th; P(丁戊 adjacent)
names = '甲乙丙丁戊己'
ok = [p for p in permutations(names) if p.index('甲') not in (0, 5) and p.index('乙') not in (0, 5) and p.index('丙') in (2, 3)]
show('2023GK-71', F(sum(1 for p in ok if abs(p.index('丁') - p.index('戊')) == 1), len(ok)), F(2, 9))

# 2025GK-79: 7 days, two distinct 2-day blocks, 3 free days pairwise non-adjacent
arr = set()
for s1 in range(6):
    for s2 in range(6):
        d1, d2 = {s1, s1 + 1}, {s2, s2 + 1}
        if d1 & d2:
            continue
        arr.add((s1, s2))
def free_ok(s1, s2):
    free = sorted(set(range(7)) - {s1, s1 + 1, s2, s2 + 1})
    return all(b - a > 1 for a, b in zip(free, free[1:]))
show('2025GK-79', F(sum(free_ok(*a) for a in arr), len(arr)), F(1, 10))

# 2021SC2-49: 5 counties to 2 groups, each >=2; P(甲乙 same group)
tot = same = 0
for assign in product((0, 1), repeat=5):
    if min(assign.count(0), assign.count(1)) >= 2:
        tot += 1
        same += assign[0] == assign[1]
show('2021SC2-49', F(same, tot), F(2, 5))

# 2021JSA-56: round table 8 seats, 4 depts x2 adjacent; 小李/小王 different depts adjacent
people = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2']  # 小王=A1, 小李=B1
tot = adj = 0
for rest in permutations(people[1:]):
    seat = ('A1',) + rest  # fix A1 at seat 0 (rotation)
    good = all(abs(seat.index(d + '1') - seat.index(d + '2')) in (1, 7) for d in 'ABCD')
    if good:
        tot += 1
        adj += abs(seat.index('A1') - seat.index('B1')) in (1, 7)
show('2021JSA-56', F(adj, tot), F(1, 6))

# 2020SZ1-55: choose 3 of 1..7, average in (3,5)
c3 = list(combinations(range(1, 8), 3))
show('2020SZ1-55', F(sum(1 for c in c3 if 9 < sum(c) < 15), len(c3)), F(3, 5))
print('   sums<=9:', sum(1 for c in c3 if sum(c) <= 9), ' sums>=15:', sum(1 for c in c3 if sum(c) >= 15))

# 2025ZJA-67: 300a+500b+700c <= 1600, not all zero; P(>=1000)
combos = [(a, b, c) for a in range(6) for b in range(4) for c in range(3) if 0 < 300 * a + 500 * b + 700 * c <= 1600]
show('2025ZJA-67', F(sum(1 for a, b, c in combos if 300 * a + 500 * b + 700 * c >= 1000), len(combos)), F(7, 10))
print('   total combos', len(combos), ' cheap(<1000):', [300 * a + 500 * b + 700 * c for a, b, c in combos if 300 * a + 500 * b + 700 * c < 1000])

# 2024GK-74: group sizes then P(甲 or 乙 in 2nd largest)
sols = [s for s in combinations(range(3, 37), 6) if sum(s) == 36 and max(s) <= 3 * min(s)]
print('2024GK-74 size sets', sols)
k = sorted(sols[0])[-2]
show('2024GK-74', 1 - F(comb(34, k), comb(36, k)), F(2, 5))

# 2022SC2-47: 乙 16, 甲 24; P(at least 1 of 3 from 甲)
p = 1 - F(comb(16, 3), comb(40, 3))
show('2022SC2-47', p)
print('   swapped counts ->', float(1 - F(comb(24, 3), comb(40, 3))))

# 2021ZJA-58: 3 odd digits with exactly two equal; P(success within 2 tries)
codes = [c for c in product('13579', repeat=3) if len(set(c)) == 2]
show('2021ZJA-58', F(2, len(codes)), F(1, 30))

# 2022SD-44
x = F(comb(9, 2), comb(10, 3)); y = 1 - F(9, 10) ** 4
show('2022SD-44 z=x-y (%)', (x - y) * 100)

# 2025ZJA-64: 8 people 2 dorms x4; no person two consecutive weeks; all 3 weeks same dorm
dorm = lambda i: i // 4
tot = fav = 0
for w1, w2, w3 in product(range(8), repeat=3):
    if w1 == w2 or w2 == w3:
        continue
    tot += 1
    fav += dorm(w1) == dorm(w2) == dorm(w3)
show('2025ZJA-64', F(fav, tot), F(9, 49))

# 2020SC0725-53: bracket champion probabilities
P = {('甲', '乙'): F(7, 10), ('甲', '丙'): F(3, 10), ('甲', '丁'): F(1, 2), ('乙', '丙'): F(1, 5), ('乙', '丁'): F(3, 10), ('丙', '丁'): F(2, 3)}
def win(a, b):
    return P[(a, b)] if (a, b) in P else 1 - P[(b, a)]
def champ(semis):
    (a, b), (c, d) = semis
    res = {}
    for x, y, others in ((a, b, (c, d)), (b, a, (c, d)), (c, d, (a, b)), (d, c, (a, b))):
        o1, o2 = others
        res[x] = win(x, y) * (win(o1, o2) * win(x, o1) + win(o2, o1) * win(x, o2))
    return res
for semis in ((('甲', '乙'), ('丙', '丁')), (('甲', '丙'), ('乙', '丁')), (('甲', '丁'), ('乙', '丙'))):
    r = champ(semis)
    print('2020SC0725-53', semis, {k: round(float(v), 4) for k, v in r.items()})

# ---------- teacher additions ----------
D = {0: 1, 1: 0}
for n in range(2, 9):
    D[n] = (n - 1) * (D[n - 1] + D[n - 2])
show('T123', F(comb(8, 3) * D[5], factorial(8)), F(11, 180))
show('T125', (F(5, 6) * F(4, 5)) ** 3, F(8, 27))
a, b, c = F(1, 5), F(1, 4), F(1, 3)
show('T126', a * b * c + a * b * (1 - c) + a * (1 - b) * c + (1 - a) * b * c, F(1, 6))
show('T127', F(6, 10) + F(5, 10) - F(25, 100), F(85, 100))
show('T133', sum(F(comb(4, k), 16) for k in (2, 3, 4)), F(11, 16))
q = F(3, 5)
show('T134', sum(comb(3, k) * q ** k * (1 - q) ** (3 - k) for k in (2, 3)), F(81, 125))
c10 = list(combinations(range(1, 11), 3))
show('T222', F(sum(1 for t in c10 if sum(t) % 3 == 0), len(c10)), F(7, 20))
trip = [(bb, cc) for bb in range(1, 200) for cc in range(1, 200) if cc * cc - bb * bb == 49]
print('T252 triples', trip, 'P =', F(25, 7 + 24 + 25), float(F(25, 56)))

# ---------- new-variant ideas ----------
# NV1: 5 pairs of gloves, draw 4, exactly one pair
gl = [(i, s) for i in range(5) for s in (0, 1)]
draws = list(combinations(gl, 4))
def npairs(d):
    ids = [i for i, _ in d]
    return sum(1 for i in range(5) if ids.count(i) == 2)
show('NV1 exactly one pair', F(sum(1 for d in draws if npairs(d) == 1), len(draws)), F(4, 7))
show('NV1 trap 5*C(8,2)', F(5 * comb(8, 2), comb(10, 4)), F(2, 3))
show('NV1 at least one pair', F(sum(1 for d in draws if npairs(d) >= 1), len(draws)), F(13, 21))
show('NV1 no pair', F(sum(1 for d in draws if npairs(d) == 0), len(draws)), F(8, 21))

# NV2: two people each pick 2 of 5 days; at least one common day
d2 = list(combinations(range(5), 2))
show('NV2 at least one common', F(sum(1 for u in d2 for v in d2 if set(u) & set(v)), len(d2) ** 2), F(7, 10))
print('   trap day-independent', 1 - (1 - (2 / 5) ** 2) ** 5, ' trap with-replacement', 1 - (3 / 5) ** 2)

# NV3: 甲 0.6 x2, 乙 0.5 x2; P(甲 hits > 乙 hits)
def binom(n, p):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
A, B = binom(2, F(3, 5)), binom(2, F(1, 2))
gt = sum(A[i] * B[j] for i in range(3) for j in range(3) if i > j)
ge = sum(A[i] * B[j] for i in range(3) for j in range(3) if i >= j)
show('NV3 甲>乙', gt, F(39, 100))
show('NV3 trap no C(2,1)', F(24, 100) * B[0] + A[2] * (B[0] + B[1]), F(33, 100))
show('NV3 trap 甲>=乙', ge, F(76, 100))

# NV4: stop after 2nd success; p=0.6; stop exactly at shot 4
p = F(3, 5); qq = 1 - p
show('NV4 exactly 4th', comb(3, 1) * p * qq ** 2 * p, F(1728, 10000))
show('NV4 trap C(4,2)', comb(4, 2) * p ** 2 * qq ** 2, F(3456, 10000))
show('NV4 within 4', 1 - qq ** 4 - 4 * p * qq ** 3, F(8208, 10000))
# brute force
tot = F(0)
for seq in product((0, 1), repeat=4):
    pr = F(1)
    for s in seq:
        pr *= p if s else qq
    if sum(seq) == 2 and seq[3] == 1:
        tot += pr
show('NV4 brute', tot, F(1728, 10000))

# NV5: written 0.4; retake 0.3; interview 0.5; P(retake | hired)
hired_direct = F(4, 10) * F(1, 2); hired_retake = F(6, 10) * F(3, 10) * F(1, 2)
show('NV5', hired_retake / (hired_direct + hired_retake), F(9, 29))
show('NV5 trap 0.09/0.2', hired_retake / hired_direct, F(9, 20))

# NV6: deuce from 10:10, p=0.6
p = F(3, 5)
show('NV6 deuce', p * p / (p * p + (1 - p) * (1 - p)), F(9, 13))
show('NV6 trap two rounds', p * p + 2 * p * (1 - p) * p * p)
# simulate by value iteration of the walk (lead -2..2)
v = {-2: F(0), 2: F(1)}
x = F(0)
for _ in range(60):
    x = p * p + 2 * p * (1 - p) * x
print('   iteration ->', float(x))

# NV7: passenger-weighted punctuality
A_pax, B_pax = 40 * 30, 20 * 90
show('NV7 by passenger', F(A_pax * 95 + B_pax * 80, (A_pax + B_pax) * 100), F(86, 100))
show('NV7 by trip', F(40 * 95 + 20 * 80, 60 * 100), F(90, 100))
show('NV7 swapped', F(A_pax * 80 + B_pax * 95, (A_pax + B_pax) * 100), F(89, 100))

# NV8: box A 3R2W, move 2 to box B (2R3W), draw 1 from B
balls = ['R'] * 3 + ['W'] * 2
tot = F(0); cnt = 0
for mv in combinations(range(5), 2):
    reds = sum(balls[i] == 'R' for i in mv)
    tot += F(2 + reds, 7); cnt += 1
show('NV8', tot / cnt, F(16, 35))
show('NV8 expectation shortcut', (2 + 2 * F(3, 5)) / 7, F(16, 35))

# NV9: choose 2 of 5 incl 王,李; given at least one of them chosen, P(王 chosen)
ch = list(combinations('王李abc', 2))
cond = [c for c in ch if '王' in c or '李' in c]
show('NV9', F(sum('王' in c for c in cond), len(cond)), F(4, 7))

# NV10: Q1 0.8 -> 100; continue Q2 0.3 -> 400 else 0
cont = F(3, 10) * 400
print('NV10 E(continue)=', cont, ' stop=100 ->', 'continue' if cont > 100 else 'stop', ' overall E =', F(8, 10) * max(cont, 100))
print('   misread keep-100 overall =', F(8, 10) * (F(3, 10) * 400 + F(7, 10) * 100))
