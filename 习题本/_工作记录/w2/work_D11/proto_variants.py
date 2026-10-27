"""Feasibility prototypes for the D11 variant requests (sample data only; generator will make its own)."""
from itertools import product
from math import lcm

# V1 2x2 table: among A-participants 1/4 also B; among non-A 1/3 do B; B = A - 10; neither = 40 -> total?
sols = set()
for N in range(1, 400):
    for A in range(0, N + 1, 4):
        nA = N - A
        if nA % 3: continue
        both, onlyB, nei = A // 4, nA // 3, nA - nA // 3
        if nei == 40 and both + onlyB == A - 10: sols.add(N)
print('V1 total', sols)

# V2 standard-type data -> exactly two: N 60, A30 B28 C26, AB12 AC10 BC9 (incl. triple), none 4
for t in range(0, 10):
    ab, ac, bc = 12 - t, 10 - t, 9 - t
    a, b, c = 30 - ab - ac - t, 28 - ab - bc - t, 26 - ac - bc - t
    if min(a, b, c, ab, ac, bc) < 0: continue
    if a + b + c + ab + ac + bc + t + 4 == 60:
        print('V2 t', t, 'exactly two', ab + ac + bc, 'at least two', ab + ac + bc + t, 'only one', a + b + c)

# V3 mark-and-cancel: 80 households, 70 >=1; (no B) - (has C) = 6; only A 9; all three 5 -> only B&C ?
ans = set()
a, abc, n = 9, 5, 10
for b, c, ab in product(range(57), repeat=3):
    for ac in range(0, 57 - b - c - ab):
        bc = 70 - (a + b + c + ab + ac + abc)
        if bc < 0: continue
        if (a + c + ac + n) - (c + ac + bc + abc) == 6: ans.add(bc)
print('V3 only B&C', ans)

# V4 containment via contrapositive: no-B => no-C (C ⊂ B); abc = C/2; C = 3/8 B; only A 20, none 10, only A&B 6, total 78 -> only B ?
ans = set()
a, n, ab = 20, 10, 6
for bc, abc in product(range(80), repeat=2):
    b = 78 - (a + ab + bc + abc + n)
    if b < 0: continue
    C = bc + abc; B = b + ab + bc + abc
    if 2 * abc == C and 8 * C == 3 * B: ans.add(b)
print('V4 only B', ans)

# V5 two-set: 120, A75, B68, none <= 15 -> min exactly-one
vals = []
for both in range(0, 69):
    nei = 120 - (75 + 68 - both)
    if 0 <= nei <= 15 and both <= 68: vals.append(75 + 68 - 2 * both)
print('V5 exactly-one range', min(vals), max(vals), ' naive(both=68):', 75 + 68 - 136)

# V6 three-set: 50 all >=1, A40 B38 C8 -> min at-least-two (brute force over regions)
best = None; arg = None
for ab, ac, bc, abc in product(range(41), range(9), range(9), range(9)):
    a, b, c = 40 - ab - ac - abc, 38 - ab - bc - abc, 8 - ac - bc - abc
    if min(a, b, c) < 0: continue
    if a + b + c + ab + ac + bc + abc != 50: continue
    v = ab + ac + bc + abc
    if best is None or v < best: best, arg = v, (a, b, c, ab, ac, bc, abc)
print('V6 min at-least-two', best, arg, ' naive ceil((S-P)/2)=', -(-(86 - 50) // 2))

# V7 periodic, non-coprime periods 4,6,10 from day 1, days 1..61 -> exactly one
P = (4, 6, 10)
cnt = [sum(1 for d in range(1, 62) if (d - 1) % p == 0) for p in P]
ex1 = sum(1 for d in range(1, 62) if sum((d - 1) % p == 0 for p in P) == 1)
un = sum(1 for d in range(1, 62) if any((d - 1) % p == 0 for p in P))
pair = [sum(1 for d in range(1, 62) if (d - 1) % lcm(p, q) == 0) for p, q in ((4, 6), (4, 10), (6, 10))]
trip = sum(1 for d in range(1, 62) if (d - 1) % 60 == 0)
print('V7 singles', cnt, 'pairs', pair, 'triple', trip, 'exactly one', ex1, 'union', un,
      'formula', sum(cnt) - 2 * sum(pair) + 3 * trip)
# product-instead-of-lcm error path
pair_bad = [sum(1 for d in range(1, 62) if (d - 1) % (p * q) == 0) for p, q in ((4, 6), (4, 10), (6, 10))]
print('   with products instead of lcm:', sum(cnt) - 2 * sum(pair_bad) + 3 * sum(1 for d in range(1, 62) if (d - 1) % 240 == 0))
