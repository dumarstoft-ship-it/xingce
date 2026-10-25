# teacher T129（2014吉林）5个阄2个“去”，5人依次抓，第二人抓到“去”的概率
from fractions import Fraction as F
from itertools import permutations

OPTS = {'A': F(4, 10), 'B': F(25, 100), 'C': F(2, 10), 'D': F(1, 10)}
lots = ['去', '去', '空', '空', '空']
orders = list(permutations(range(len(lots))))   # 第k个人抓到第order[k]号阄
P = F(sum(lots[o[1]] == '去' for o in orders), len(orders))
print('P =', P)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
