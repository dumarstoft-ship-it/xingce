# D05-math-2-v09：12 台相同的 AED 全部分给 3 个（不同的）社区，每个社区至少 2 台。
# 枚举 (社区1, 社区2, 社区3) 的台数。
from itertools import product

OPTIONS = {'A': 7, 'B': 10, 'C': 28, 'D': 55}

TOTAL, LOW = 12, 2
count = sum(1 for t in product(range(TOTAL + 1), repeat=3)
            if sum(t) == TOTAL and min(t) >= LOW)

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
