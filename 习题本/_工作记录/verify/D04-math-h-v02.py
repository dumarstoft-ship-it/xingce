# D04-math-h-v02: a food company has only two businesses. In 2024 the frozen-food business made a profit a,
# the prepared-dish business made a loss b. In 2025 the frozen-food profit grew 10%, the prepared-dish loss
# shrank by 40%, and the company's total profit grew 50%. Find b as a percentage of a (2024 figures).
# Method: (1) brute force over integer pairs (a, b) with 1 <= a, b <= 300, keeping every pair that satisfies
# the 2025 condition exactly (losses entered as negative profit); all must share one ratio b/a.
# (2) check the 2024 total profit is positive, so "grew 50%" is meaningful. (3) match the ratio, in percent,
# against the options (two of them are given to one decimal place as "约").
from fractions import Fraction as F
import re

OPTIONS = {'A': '约44.4%', 'B': '约55.6%', 'C': '80%', 'D': '400%'}

G_FROZEN = F(10, 100)      # frozen-food profit +10%
LOSS_CUT = F(40, 100)      # prepared-dish loss -40%
G_TOTAL = F(50, 100)       # total profit +50%


def totals(a, b):
    t2024 = a + (-b)
    t2025 = a * (1 + G_FROZEN) + (-b * (1 - LOSS_CUT))
    return t2024, t2025


ratios = set()
for a in range(1, 301):
    for b in range(1, 301):
        t24, t25 = totals(F(a), F(b))
        if t25 == t24 * (1 + G_TOTAL):
            ratios.add(F(b, a))
assert len(ratios) == 1, ratios
r = ratios.pop()
assert totals(F(1), r)[0] > 0          # the 2024 total profit is positive
pct = r * 100
print('b/a =', r, '=', float(pct), '%')


def opt_value(s):
    return F(re.sub(r'[^0-9.]', '', s))


hits = []
for k, s in OPTIONS.items():
    v = opt_value(s)
    if s.startswith('约'):
        good = abs(pct - v) < F(5, 100)    # rounded to 0.1 percentage point
    else:
        good = pct == v
    if good:
        hits.append(k)
assert len(hits) == 1, hits

# distractors reproduce the error paths named in the 解析
# loss cut treated as a negative contribution: 0.1a - 0.4b = 0.5(a - b)  ->  b = 4a
wrong_sign = (G_TOTAL - G_FROZEN) / (G_TOTAL - LOSS_CUT)
assert wrong_sign * 100 == opt_value(OPTIONS['D'])
# loss compared with the 2024 total profit instead of the frozen-food profit
assert r / (1 - r) * 100 == opt_value(OPTIONS['C'])
# lever rule with weights proportional (not inversely proportional) to the distances: frozen = total + loss,
# distances 50% - 10% = 40 (total) and 10% - (-40%) = 50 (loss); swapped weights total : loss = 40 : 50
d_total, d_loss = G_TOTAL - G_FROZEN, G_FROZEN + LOSS_CUT
assert d_loss / d_total == (1 - r) / r                         # the correct weights are inversely proportional
swapped = d_loss / (d_total + d_loss) * 100                    # loss / frozen with the weights swapped
assert abs(swapped - opt_value(OPTIONS['B'])) < F(5, 100)
print(hits[0])
