# D05-math-2-v05：6 名专家全部派往甲、乙、丙 3 个镇，每人只去 1 个镇；每镇至少 1 人，且 3 镇人数互不相同。
# 枚举每名专家的去向（3^6 种），筛选条件。
from itertools import product

OPTIONS = {'A': 60, 'B': 180, 'C': 360, 'D': 540}

count = 0
for f in product(range(3), repeat=6):          # f[i] = 第 i 名专家去的镇
    sizes = [f.count(t) for t in range(3)]
    if min(sizes) >= 1 and len(set(sizes)) == 3:
        count += 1

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
