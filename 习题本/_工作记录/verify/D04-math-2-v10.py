# D04-math-2-v10 会员卡临界消费额（按标价总额计）
from fractions import Fraction as F
fee, disc = 190, F(95, 100)
member = lambda x: fee + disc * x
non = lambda x: F(x)
# 临界点：member(x) = non(x)
x0 = F(fee) / (1 - disc)
assert member(x0) == non(x0) and member(x0 + 1) < non(x0 + 1) and member(x0 - 1) > non(x0 - 1)
options = {'A': 1900, 'B': 3610, 'C': 3800, 'D': 4000}
print('threshold =', x0, {k: (member(v) < non(v)) for k, v in options.items()})
hits = [k for k, v in options.items() if v == x0]
assert len(hits) == 1, hits
print(hits[0])
