# D06-math-2-v07: suppliers A/B/C with purchase shares 4:3:3, defect rates 1%, 2%, 4%;
# given a randomly drawn meter is defective, P(it comes from supplier C).
from fractions import Fraction as F

share = [4, 3, 3]
rate = [F(1, 100), F(2, 100), F(4, 100)]
tot = sum(share)
joint = [F(s, tot) * d for s, d in zip(share, rate)]   # P(supplier i and defective)
P = joint[2] / sum(joint)                               # Bayes: P(C | defective)

opts = {'A': F(3, 11), 'B': F(3, 10), 'C': F(6, 11), 'D': F(4, 7)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('P =', P)
print(hit[0])
