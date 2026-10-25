"""D05-math-1-v13 验算：6 节不同车厢（动力 2、餐车 1、客车 3）从前到后排列；
2 节动力车厢相连且位于整列车的一端；餐车不与任一动力车厢相邻。穷举全排列。"""
from itertools import permutations

OPTIONS = {"A": 24, "B": 36, "C": 48, "D": 72}
cars = ["动1", "动2", "餐", "客1", "客2", "客3"]

cnt = 0
for p in permutations(cars):
    d1, d2, c = p.index("动1"), p.index("动2"), p.index("餐")
    if abs(d1 - d2) != 1:
        continue
    if {d1, d2} not in ({0, 1}, {4, 5}):
        continue
    if abs(c - d1) == 1 or abs(c - d2) == 1:
        continue
    cnt += 1

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
