# D06-math-2-v04: P(warning day) = p; congestion 75% on warning days, 25% otherwise;
# overall average congestion 40%. Solve p.
from fractions import Fraction as F

hi, lo, avg = F(75, 100), F(25, 100), F(40, 100)

def overall(p):
    return p * hi + (1 - p) * lo

# overall(p) is linear in p: solve overall(p) = avg
p = (avg - overall(F(0))) / (overall(F(1)) - overall(F(0)))
assert 0 <= p <= 1 and overall(p) == avg

opts = {'A': F(15, 100), 'B': F(20, 100), 'C': F(30, 100), 'D': F(70, 100)}
hit = [k for k, v in opts.items() if v == p]
# cross-check: exactly one option reproduces the 40% average
assert [k for k, v in opts.items() if overall(v) == avg] == hit
assert len(hit) == 1, (p, hit)
print('p =', p)
print(hit[0])
