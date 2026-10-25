# D05-math-2-v07：5 名志愿者分到 3 个不同的地铁站，每人只去 1 站，每站至少 1 人。
# 枚举每人的去向（3^5 种），筛选 3 个站都有人的情况。
from itertools import product

OPTIONS = {'A': 90, 'B': 150, 'C': 300, 'D': 540}

count = 0
for f in product(range(3), repeat=5):
    if len(set(f)) == 3:
        count += 1

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
