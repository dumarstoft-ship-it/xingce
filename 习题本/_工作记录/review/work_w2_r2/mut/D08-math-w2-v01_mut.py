# D08-math-w2-v01: a volunteer team spends exactly 2700 points on rice (48 points/bag) and
# cooking oil (60 points/barrel). Both items must be taken, and the number of rice bags must be
# not less than the number of oil barrels. Question: how many different exchange plans are there?
# Method: brute-force every (rice, oil) pair straight from the stem data, count the plans that meet
# all conditions, cross-check with the "particular solution + step" description, and match options.
from math import gcd

TOTAL, RICE, OIL = 2640, 48, 60
opts = {'A': 6, 'B': 7, 'C': 11, 'D': 12}

# every non-negative pair that uses the points up exactly
pairs = [(x, y) for x in range(TOTAL // RICE + 1) for y in range(TOTAL // OIL + 1)
         if RICE * x + OIL * y == TOTAL]
both = [(x, y) for x, y in pairs if x >= 1 and y >= 1]          # both items taken
good = [(x, y) for x, y in both if x >= y]                       # rice bags >= oil barrels
count = len(good)

# cross-check with the step description: reduce by g, then x moves by OIL/g and y by RICE/g
g = gcd(RICE, OIL)
assert TOTAL % g == 0 and g == 12
step_x, step_y = OIL // g, RICE // g                             # 5 and 4
xs = sorted(x for x, _ in good)
assert all(b - a == step_x for a, b in zip(xs, xs[1:]))
assert all(y == (TOTAL // g - (RICE // g) * x) // (OIL // g) for x, y in good)

hit = [k for k, v in opts.items() if v == count]
assert len(hit) == 1, (count, hit)

# where the distractors come from (documentation only; the answer above does not use these)
ignore_order = len(both)                                         # forget "rice not less than oil"
ignore_order_and_zero = len(pairs)                               # ... and also count the all-oil plan (0, 45)
strict = sum(1 for x, y in both if x > y)                        # read "not less than" as "more than"
assert (strict, ignore_order, ignore_order_and_zero) == (opts['A'], opts['C'], opts['D']), \
    (strict, ignore_order, ignore_order_and_zero)
assert (25, 25) in good and (0, 45) in pairs                     # the equality plan and the zero plan exist

print('plans', good)
print('count', count, '| no order limit', ignore_order, '| with zero', ignore_order_and_zero, '| strict', strict)
print(hit[0])
