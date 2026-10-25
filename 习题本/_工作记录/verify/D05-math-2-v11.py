# D05-math-2-v11：10 个相同的岗位名额全部分给 4 个乡镇，每镇至少 1 个、至多 4 个。
# 枚举 4 个乡镇各自的名额数。
from itertools import product

OPTIONS = {'A': 44, 'B': 68, 'C': 74, 'D': 84}

TOTAL, LOW, HIGH = 10, 1, 4
count = sum(1 for t in product(range(TOTAL + 1), repeat=4)
            if sum(t) == TOTAL and all(LOW <= x <= HIGH for x in t))

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
