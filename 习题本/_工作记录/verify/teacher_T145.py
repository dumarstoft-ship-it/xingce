# teacher T145（2013江苏A）公比2的等比数列，第n项与前n-1项和之差为5，求前4项和
from fractions import Fraction as F

OPTS = {'A': 70, 'B': 85, 'C': 80, 'D': 75}
Q, DIFF = 2, 5
cands = set()
for num in range(-400, 401):
    a1 = F(num, 4)
    seq = [a1 * Q ** i for i in range(12)]
    # 对任意n（2..12）都检验：a_n - (a_1+...+a_{n-1}) == 5
    if all(seq[n - 1] - sum(seq[:n - 1]) == DIFF for n in range(2, 13)):
        cands.add(a1)
assert len(cands) == 1, cands
a1 = cands.pop()
s4 = sum(a1 * Q ** i for i in range(4))
print('a1 =', a1, 'S4 =', s4)
hits = [k for k, v in OPTS.items() if v == s4]
assert len(hits) == 1, hits
print(hits[0])
