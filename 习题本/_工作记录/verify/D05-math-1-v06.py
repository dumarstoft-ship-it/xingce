"""D05-math-1-v06 验算：6 男 3 女医生选 3 人，男医生不超过 2 名。枚举全部 3 人组合。"""
from itertools import combinations

OPTIONS = {"A": 45, "B": 63, "C": 64, "D": 83}
doctors = ["男"] * 6 + ["女"] * 3
cnt = sum(1 for s in combinations(range(9), 3) if sum(doctors[i] == "男" for i in s) <= 2)

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
