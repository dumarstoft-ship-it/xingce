# D08-math-w2-v02: four grid workers (jia, yi, bing, ding) visited different numbers of households,
# ordered from most to fewest as jia > yi > bing > ding (all distinct, positive integers).
# jia = 2 * bing, jia + yi = 57, bing + ding = 34. Question: how many households did ding visit?
# Options: 16 / 17 / 18 / "cannot be determined".
# Method: brute-force every positive 4-tuple satisfying the three equations, keep those that respect
# the full strict order, and decide which option is the (only) true statement.
from itertools import product

S_AB, S_CD, MULT = 57, 32, 2
opts = {'A': 16, 'B': 17, 'C': 18, 'D': 'undetermined'}


def tuples():
    lim = S_AB + S_CD
    for a, c in product(range(1, lim), repeat=2):
        b, d = S_AB - a, S_CD - c
        if a == MULT * c and min(a, b, c, d) >= 1:
            yield a, b, c, d


full = [t for t in tuples() if t[0] > t[1] > t[2] > t[3]]
ding = sorted({t[3] for t in full})
assert ding, 'no solution'


def true_option(key):
    v = opts[key]
    if v == 'undetermined':
        return len(ding) > 1
    return ding == [v]


hit = [k for k in opts if true_option(k)]
assert len(hit) == 1, (ding, hit)

# where the traps come from (documentation only; the answer above does not use these)
first_two = [t for t in tuples() if t[0] > t[1] > t[2]]                    # only jia>yi and yi>bing
assert len(first_two) == 4 and sorted(t[3] for t in first_two) == [16, 17, 18, 19]
non_strict = [t for t in tuples() if t[0] >= t[1] >= t[2] >= t[3]]        # read every ">" as ">="
assert sorted(t[2] for t in non_strict) == [17, 18, 19]                    # bing=17 (bing=ding) or 19 (yi=bing)
for wrong in (17, 18):                                                     # each numeric distractor breaks bing>ding
    t = next(t for t in first_two if t[3] == wrong)
    assert t[0] > t[1] > t[2] and not t[2] > t[3], t
assert full[0][2] == opts['C']                                             # 18 is bing's own count

print('full order:', full, '| first two only:', first_two)
print(hit[0])
