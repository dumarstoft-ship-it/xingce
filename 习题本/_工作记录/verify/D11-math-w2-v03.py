# D11-math-w2-v03: 140 elderly households; services: meals (M), bathing (B), medical visits (D)
#   85% applied for at least one service
#   (households that did NOT apply for D) == (households that applied for exactly one service)
#   applied for both M and B: 20 households, 5 of whom applied for all three
# Question: households that applied for D only.
# Method: enumerate every non-negative filling of the eight regions consistent with the stem and
# collect the "D only" value; it must be the same in all fillings. Then match the options.
from fractions import Fraction as Fr

N, AT_LEAST_ONE_SHARE = 140, Fr(85, 100)
MB_INCL, ALL3 = 20, 5

at_least_one = AT_LEAST_ONE_SHARE * N
assert at_least_one.denominator == 1
at_least_one = int(at_least_one)

answers, fillings = set(), 0
for none in range(0, N + 1):
    if N - none != at_least_one:
        continue
    for abc in range(0, N + 1):
        if abc != ALL3:
            continue
        mb = MB_INCL - abc                               # M and B but not D
        if mb < 0:
            continue
        rest = at_least_one - mb - abc                   # m + b + d + md + bd
        for m in range(rest + 1):
            for b in range(rest - m + 1):
                for md in range(rest - m - b + 1):
                    for bd in range(rest - m - b - md + 1):
                        d = rest - m - b - md - bd
                        not_d = m + b + mb + none
                        exactly_one = m + b + d
                        if not_d == exactly_one:
                            answers.add(d)
                            fillings += 1
assert fillings > 0 and len(answers) == 1, (fillings, answers)
d_only = answers.pop()

opts = {'A': 15, 'B': 20, 'C': 36, 'D': 41}
hit = [k for k, v in opts.items() if v == d_only]
assert len(hit) == 1, (d_only, hit)

# distractors (documentation only)
none = N - at_least_one
forget_none = MB_INCL - ALL3                 # "not D" without the 21 households that applied for nothing
use_20 = MB_INCL + none                      # take 20 as "M and B only"
both_wrong = MB_INCL
assert [forget_none, both_wrong, use_20] == [opts['A'], opts['B'], opts['D']]

print('consistent fillings', fillings, 'D only always', d_only)
print(hit[0])
