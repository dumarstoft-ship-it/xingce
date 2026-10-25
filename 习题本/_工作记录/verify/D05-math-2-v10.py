# D05-math-2-v10：月季、三角梅、茉莉共 10 盆，每种至少 1 盆，月季盆数为偶数。
# 枚举 (月季, 三角梅, 茉莉) 的盆数。
from itertools import product

OPTIONS = {'A': 16, 'B': 18, 'C': 20, 'D': 36}

TOTAL = 10
count = sum(1 for (rose, bougain, jasmine) in product(range(TOTAL + 1), repeat=3)
            if rose + bougain + jasmine == TOTAL
            and min(rose, bougain, jasmine) >= 1
            and rose % 2 == 0)

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
