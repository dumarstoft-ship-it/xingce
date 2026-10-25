"""D05-math-1-v18 验算：4 男（含甲）3 女依次出场，男女交替，甲不第一个出场。穷举 7 人全排列。"""
from itertools import permutations

OPTIONS = {"A": 108, "B": 144, "C": 216, "D": 288}
people = ["男甲", "男2", "男3", "男4", "女1", "女2", "女3"]
cnt = sum(1 for p in permutations(people)
          if all(p[i][0] != p[i + 1][0] for i in range(6)) and p[0] != "男甲")

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
