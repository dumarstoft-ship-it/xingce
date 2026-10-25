"""D05-math-1-v09 验算：粤 4、港 3、澳 2 家企业中选 4 家，三地都有。枚举全部 4 家组合。"""
from itertools import combinations

OPTIONS = {"A": 36, "B": 71, "C": 72, "D": 144}
region = ["粤"] * 4 + ["港"] * 3 + ["澳"] * 2
cnt = sum(1 for s in combinations(range(9), 4) if {region[i] for i in s} == {"粤", "港", "澳"})

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
