# T207（2015河南）1~10号球，两人各取3个（同一人所取号码互不相同），号码之积都是144，小张的和更大，求小张的和。
from itertools import combinations
from math import prod

BALLS, PRODUCT = range(1, 11), 144
OPTS = {'A': 19, 'B': 17, 'C': 16, 'D': 14}
sums = sorted({sum(c) for c in combinations(BALLS, 3) if prod(c) == PRODUCT})
assert len(sums) == 2                 # 恰有两种不同的和，较大者为小张
ans = max(sums)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('triples =', [c for c in combinations(BALLS, 3) if prod(c) == PRODUCT], 'sums =', sums)
print(hits[0])
