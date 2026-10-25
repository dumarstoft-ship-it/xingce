"""D05-math-1-v10 验算：6 家企业排 6 个展位（从左到右），甲不在最左、乙不在最右。穷举全排列。"""
from itertools import permutations

OPTIONS = {"A": 384, "B": 480, "C": 500, "D": 504}
firms = ["甲", "乙", "丙", "丁", "戊", "己"]
cnt = sum(1 for p in permutations(firms) if p[0] != "甲" and p[-1] != "乙")

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
