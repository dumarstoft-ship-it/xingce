"""D05-math-1-v17 验算：一排 10 盏灯关 3 盏，首尾两盏不关，不关相邻两盏。枚举全部 3 盏组合。"""
from itertools import combinations

OPTIONS = {"A": 20, "B": 35, "C": 56, "D": 120}
N = 10
cnt = sum(1 for s in combinations(range(N), 3)
          if 0 not in s and N - 1 not in s and all(b - a >= 2 for a, b in combinations(s, 2)))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
