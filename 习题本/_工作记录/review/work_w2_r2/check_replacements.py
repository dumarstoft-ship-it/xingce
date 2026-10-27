# Check the replacement distractors proposed in the review (all derived from stem data).

# ---- D11-v02: replace 32 with 4 (forgot the 6 "none" firms: union taken as 74) ----
A, B, C, AB, AC, BC, N, NONE = 38, 34, 28, 17, 12, 8, 74, 6
P = AB + AC + BC
T = (N - NONE) - (A + B + C - P)            # correct triple
T_forgot_none = N - (A + B + C - P)         # union mistaken as 74
correct = P - 3 * T
wrong4 = P - 3 * T_forgot_none
print('v02 triple', T, 'exactly-two', correct, '| forgot none: triple', T_forgot_none, '-> exactly-two', wrong4,
      '| at-least-two (subtract twice)', P - 2 * T, '| not subtracted', P)
new_opts = sorted([wrong4, correct, P - 2 * T, P])
diffs = [b - a for a, b in zip(new_opts, new_opts[1:])]
print('   new option set', new_opts, 'gaps', diffs, '(AP?' , len(set(diffs)) == 1, ')')

# ---- D11-v05: replace 110 with 69 ----
TOT, S, F, NMAX = 126, 88, 79, 16
both = S + F - (TOT - NMAX)                  # 57 at the optimum
exact1 = S + F - 2 * both                    # 53
slip_a = TOT - both                          # "exactly one = total - both" (forgot the 16 non-participants)
slip_b = (TOT - NMAX) - (S + F - TOT)        # union with neither=16 minus "both" computed with neither=0
print('v05 both', both, 'exactly-one', exact1, '| 126-57 =', slip_a, '| 110-41 =', slip_b,
      '| parity of exactly-one (167-2x) is odd; 110 even ->', 110 % 2 == 0)
feasible = sorted({(S - x) + (F - x) for x in range(0, min(S, F) + 1)
                   if 0 <= TOT - (S + F - x) <= NMAX})
print('   feasible exactly-one values:', feasible[:3], '...', feasible[-3:], '| 69 feasible but not minimal:', 69 in feasible)

# ---- D11-v07: replace 15 with 8 ----
def counts(periods, lo=0, hi=60):
    out = {0: 0, 1: 0, 2: 0, 3: 0}
    for d in range(lo, hi + 1):
        out[sum(d % p == 0 for p in periods)] += 1
    return out

c = counts([8, 10, 12])
union = c[1] + c[2] + c[3]
pairs_sum = sum(1 for d in range(61) for (p, q) in ((8, 10), (8, 12), (10, 12)) if d % p == 0 and d % q == 0)
print('v07 exactly-one', c[1], '| union', union, '| sum of pairwise coincidences', pairs_sum,
      '| days with >=2 lines', c[2] + c[3], '| union - pairs_sum =', union - pairs_sum)
print('   formula slip (singles - 2*pairs, no +3*triple):', 21 - 2 * pairs_sum)
# Robustness of the correct value to window-boundary readings
for lo, hi in ((0, 60), (1, 60), (0, 59), (1, 59)):
    print('   window', (lo, hi), 'exactly-one', counts([8, 10, 12], lo, hi)[1], '| period-n reading', counts([7, 9, 11], lo, hi)[1])
old = [10, 15, 18, 19]
new = [8, 10, 18, 19]
for name, opts in (('old', old), ('new', new)):
    survivors = [o for o in opts if o < union]       # exactly-one must be < union (June 1 is a triple day)
    print('   %s options %s -> survive union bound (<%d): %s' % (name, opts, union, survivors))
