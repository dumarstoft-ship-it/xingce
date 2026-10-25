"""D05-math-1-v11 验算：3 个科室 2、3、3 名选手，同科室连续出场，第 1 个出场的是 2 人科室的选手。
穷举 8 人全排列。"""
from itertools import permutations

OPTIONS = {"A": 72, "B": 144, "C": 288, "D": 432}
players = ["A1", "A2", "B1", "B2", "B3", "C1", "C2", "C3"]   # A 科室 2 人

def contiguous(p, dept):
    idx = [i for i, x in enumerate(p) if x[0] == dept]
    return idx[-1] - idx[0] == len(idx) - 1

cnt = sum(1 for p in permutations(players)
          if p[0][0] == "A" and all(contiguous(p, d) for d in "ABC"))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
