"""D05-math-1-v16 验算：本周一至周日（不循环）选 3 天，任意两天不相邻，周日必选。枚举全部 3 天组合。"""
from itertools import combinations

OPTIONS = {"A": 3, "B": 6, "C": 10, "D": 15}
SUN = 6
cnt = sum(1 for s in combinations(range(7), 3)
          if SUN in s and all(b - a >= 2 for a, b in combinations(s, 2)))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
