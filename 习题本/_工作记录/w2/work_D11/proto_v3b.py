"""V3 redesign: 'no A' count equals 'exactly one item' count -> cancel only-B, only-C; ask only-A.
80 people, 85% at least one (none = 12); 'both B and C' 15 people of whom 6 do all three."""
from itertools import product
ans = set(); free = 0
n, abc = 12, 6
bc = 15 - abc
for a, b, c, ab in product(range(69), repeat=4):
    ac = 68 - (a + b + c + ab + bc + abc)
    if ac < 0: continue
    notA = b + c + bc + n
    one = a + b + c
    if notA == one:
        ans.add(a); free += 1
print('only-A values:', ans, ' (#consistent region fillings:', free, ')')
print('error paths: forget none ->', bc, '; use B∩C incl. triple ->', 15 + n, '; forget none and use 15 ->', 15)
