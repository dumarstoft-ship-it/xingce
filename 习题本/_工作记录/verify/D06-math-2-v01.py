# D06-math-2-v01: two experts review independently (pass prob 0.5 each);
# both pass -> selected; both fail -> out; exactly one pass -> committee review with pass rate x.
# Find x so that P(selected) = 0.4.
from fractions import Fraction as F
from itertools import product

p_expert = F(1, 2)
target = F(2, 5)

# P(selected) = a + b*x, enumerate the 4 outcomes of the two experts
a = F(0)
b = F(0)
for e1, e2 in product([True, False], repeat=2):
    pr = (p_expert if e1 else 1 - p_expert) * (p_expert if e2 else 1 - p_expert)
    if e1 and e2:
        a += pr          # selected directly
    elif e1 != e2:
        b += pr          # goes to committee, selected with prob x
x = (target - a) / b
assert 0 <= x <= 1

opts = {'A': F(15, 100), 'B': F(3, 10), 'C': F(6, 10), 'D': F(8, 10)}
hit = [k for k, v in opts.items() if v == x]
assert len(hit) == 1, (x, hit)
print('x =', x)
print(hit[0])
