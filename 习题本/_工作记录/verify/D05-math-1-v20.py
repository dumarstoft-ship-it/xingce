"""D05-math-1-v20 验算：1-12 号厂房，3 家不同企业各租 1 间，任意两家编号至少相差 3。
枚举"企业→编号"的全部有序分配。"""
from itertools import permutations, combinations

OPTIONS = {"A": 20, "B": 56, "C": 120, "D": 336}
cnt = sum(1 for p in permutations(range(1, 13), 3)
          if all(abs(a - b) >= 3 for a, b in combinations(p, 2)))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
