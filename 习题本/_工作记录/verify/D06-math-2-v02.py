# D06-math-2-v02: theory first (pass 0.8 per attempt), then practical (0.6 per attempt);
# each subject allows 1 retake; certificate needs both subjects passed.
from fractions import Fraction as F
from itertools import product

pt = F(8, 10)   # theory, each attempt
pp = F(6, 10)   # practical, each attempt

total = F(0)
# pre-sample all potential attempts (unused attempts are marginalised out)
for t1, t2, p1, p2 in product([True, False], repeat=4):
    pr = (pt if t1 else 1 - pt) * (pt if t2 else 1 - pt) * (pp if p1 else 1 - pp) * (pp if p2 else 1 - pp)
    theory_ok = t1 or (not t1 and t2)          # retake only if first attempt fails
    if not theory_ok:
        continue                                # cannot sit the practical exam
    prac_ok = p1 or (not p1 and p2)
    if prac_ok:
        total += pr

opts = {'A': F(4800, 10000), 'B': F(5760, 10000), 'C': F(6720, 10000), 'D': F(8064, 10000)}
hit = [k for k, v in opts.items() if v == total]
assert len(hit) == 1, (total, hit)
print('P =', float(total))
print(hit[0])
