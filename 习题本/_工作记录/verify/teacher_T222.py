# T222 从1~10号球中不放回取3个，号码和为3的倍数即中奖，求中奖概率。
from fractions import Fraction as F
from itertools import combinations

BALLS = range(1, 11)
OPTS = {'A': F(3, 10), 'B': F(1, 3), 'C': F(41, 120), 'D': F(7, 20)}
allc = list(combinations(BALLS, 3))
p = F(sum(1 for c in allc if sum(c) % 3 == 0), len(allc))
hits = [k for k, v in OPTS.items() if v == p]
assert len(hits) == 1, (p, hits)
# 干扰项来源核对
assert F(sum(1 for c in allc if len({x % 3 for x in c}) == 3), len(allc)) == OPTS['A']   # 只算三组各取一个
print('P =', p)
print(hits[0])
