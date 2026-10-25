# D06-math-2-v11: typhoon prob 0.2, loss 50 (10k yuan); insurance premium 6, pays 80% of loss.
# Compare expected loss (premium included) and evaluate the four statements.
from fractions import Fraction as F

p, loss, prem, cover = F(2, 10), F(50), F(6), F(8, 10)
no_ins = p * loss
ins = prem + p * loss * (1 - cover)

if ins < no_ins:
    better, diff = '投保', no_ins - ins
elif ins > no_ins:
    better, diff = '不投保', ins - no_ins
else:
    better, diff = '相同', F(0)

opts = {'A': ('不投保', F(4)), 'B': ('投保', F(8)), 'C': ('投保', F(4)), 'D': ('投保', F(2))}
hit = [k for k, (b, d) in opts.items() if b == better and d == diff]
assert len(hit) == 1, (better, diff, hit)
print('no insurance', no_ins, 'insurance', ins)
print(hit[0])
