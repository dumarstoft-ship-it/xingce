# D05-math-h-v03：11 套相同的少儿绘本配送给 3 个社区，每个社区至少 2 套，
# 绘本不必全部送出（没送出的留在馆内备用）。只看各社区分到几套，问有多少种配送方案。
# 暴力枚举：枚举 3 个社区各分到的套数，要求每个至少 2 套、送出总数不超过 11 套。
from itertools import product

OPTIONS = {'A': 20, 'B': 21, 'C': 35, 'D': 56}

TOTAL, LOW, COMMUNITIES = 11, 2, 3
count = sum(1 for t in product(range(TOTAL + 1), repeat=COMMUNITIES)
            if all(x >= LOW for x in t) and sum(t) <= TOTAL)

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
