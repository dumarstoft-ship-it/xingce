# D06-math-1-v10: 8 人随机两两分成 4 组，小林(0)和小周(1)同组的概率
from fractions import Fraction as F
def pairings(lst):
    if not lst:
        yield []
        return
    a = lst[0]
    for i in range(1, len(lst)):
        for rest in pairings(lst[1:i] + lst[i + 1:]):
            yield [(a, lst[i])] + rest
allp = list(pairings(list(range(8))))
ans = F(sum(1 for p in allp if (0, 1) in p), len(allp))
opts = {'A': F(1, 7), 'B': F(1, 4), 'C': F(2, 7), 'D': F(1, 28)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('pairings =', len(allp), 'P =', ans)
print(hit[0])
