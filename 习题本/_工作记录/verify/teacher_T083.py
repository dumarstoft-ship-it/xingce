# T083 2012江苏B：浓度20%的溶液加水后变为15%，再加同样多的水，浓度变为？
from fractions import Fraction as F

C0, C1 = F(20, 100), F(15, 100)
OPTS = {'A': F(13, 100), 'B': F(125, 1000), 'C': F(12, 100), 'D': F(10, 100)}

results = set()
for S in range(1, 501):              # 原溶液质量任取，结果应与其无关
    S = F(S)
    salt = S * C0                     # 加水溶质不变
    w = salt / C1 - S                 # 第一次加的水量
    results.add(salt / (S + 2 * w))   # 再加同样多的水
assert len(results) == 1
c2 = results.pop()
hits = [k for k, v in OPTS.items() if v == c2]
assert len(hits) == 1, (c2, hits)
assert C1 - (C0 - C1) == OPTS['D']    # 干扰项：以为每次都降5个百分点
print('final concentration =', float(c2))
print(hits[0])
