"""D05-math-1-v19 验算：10 月 1 日至 15 日选 4 天巡查，相邻两次巡查之间至少空出 2 天。枚举全部 4 天组合。"""
from itertools import combinations

OPTIONS = {"A": 35, "B": 126, "C": 210, "D": 495}
cnt = sum(1 for s in combinations(range(1, 16), 4)
          if all(s[i + 1] - s[i] - 1 >= 2 for i in range(3)))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
