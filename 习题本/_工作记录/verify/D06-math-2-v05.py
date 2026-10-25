# D06-math-2-v05: three lines, output ratio 5:3:2, defect rates 2%,3%,5%; P(defective) of a random item.
from fractions import Fraction as F

ratio = [5, 3, 2]
rate = [F(2, 100), F(3, 100), F(5, 100)]
tot = sum(ratio)
P = sum(F(r, tot) * d for r, d in zip(ratio, rate))

opts = {'A': F(26, 1000), 'B': F(29, 1000), 'C': F(33, 1000), 'D': F(38, 1000)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1, (P, hit)
print('P =', P)
print(hit[0])
