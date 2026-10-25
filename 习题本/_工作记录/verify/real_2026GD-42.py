"""2026GD-42 自解验算：周一至周日选 3 天开展活动，每次活动之间至少间隔 1 天。枚举全部 3 天组合。"""
from itertools import combinations

OPTIONS = {"A": 3, "B": 5, "C": 10, "D": 15}
cnt = sum(1 for s in combinations(range(7), 3)
          if all(s[i + 1] - s[i] - 1 >= 1 for i in range(2)))
exact = sum(1 for s in combinations(range(7), 3)            # 误读"恰好间隔 1 天"
            if all(s[i + 1] - s[i] - 1 == 1 for i in range(2)))
assert exact == OPTIONS["A"]

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt, "| 恰好间隔1天的误读 =", exact)
print(hits[0])
