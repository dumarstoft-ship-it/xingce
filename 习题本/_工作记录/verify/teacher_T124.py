# teacher T124（2021浙江）A试验田连续3年中至少2年种同一作物的概率
from fractions import Fraction as F
from itertools import permutations, product
from collections import Counter

OPTS = {'A': F(36, 100), 'B': F(48, 100), 'C': F(52, 100), 'D': F(64, 100)}
CROPS, YEARS = 5, 3
# 每年在“5种作物分到5块田”的全部安排中等可能地挑一种
arrangements = list(permutations(range(CROPS)))
dist = Counter(p[0] for p in arrangements)          # A田（第0块）的作物分布
good = tot = 0
for crops in product(dist, repeat=YEARS):
    w = 1
    for c in crops:
        w *= dist[c]
    tot += w
    if len(set(crops)) < YEARS:                       # 至少两年相同
        good += w
P = F(good, tot)
print('P =', P, '| 恰两年相同 =', P - F(1, 25), '(只算这一类会得48%)')
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
