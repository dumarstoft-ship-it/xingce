"""D05-math-1-v14 验算：5 人一排，甲乙丙中恰有两人相邻，且第三人与这两人都不相邻。穷举全排列。"""
from itertools import permutations

OPTIONS = {"A": 72, "B": 84, "C": 108, "D": 144}

cnt = 0
for p in permutations("甲乙丙丁戊"):
    adj = lambda a, b: abs(p.index(a) - p.index(b)) == 1
    ok = any(adj(x, y) and not adj(z, x) and not adj(z, y)
             for x, y, z in (("甲", "乙", "丙"), ("甲", "丙", "乙"), ("乙", "丙", "甲")))
    cnt += ok

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
