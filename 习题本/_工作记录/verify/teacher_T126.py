# teacher T126 双胞胎随机着装，上衣、裙子、鞋子中至少两件相同的概率
from fractions import Fraction as F
from itertools import product

OPTS = {'A': F(3, 20), 'B': F(1, 6), 'C': F(1, 2), 'D': F(5, 6)}
TOP, SKIRT, SHOE = 5, 4, 3
outfits = list(product(range(TOP), range(SKIRT), range(SHOE)))
good = tot = 0
for a, b in product(outfits, repeat=2):
    tot += 1
    if sum(x == y for x, y in zip(a, b)) >= 2:
        good += 1
P = F(good, tot)
print('P =', P)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
