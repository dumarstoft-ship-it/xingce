# D05-math-2-v06：6 名公务员分到 3 个不同街道，每个街道 2 人；甲、乙必须在同一街道。
# 枚举每人的去向（3^6 种），筛选"每街道恰 2 人且甲乙同街道"。
from itertools import product

OPTIONS = {'A': 3, 'B': 6, 'C': 9, 'D': 18}

JIA, YI = 0, 1                                  # 0 号=甲，1 号=乙，其余 4 人编号 2–5
count = 0
for f in product(range(3), repeat=6):
    if all(f.count(t) == 2 for t in range(3)) and f[JIA] == f[YI]:
        count += 1

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
