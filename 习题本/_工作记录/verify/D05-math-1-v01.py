"""D05-math-1-v01 验算：两荤两素套餐，荤菜比素菜多 2 种，共 210 种套餐，求荤菜种数。
对每个选项给出的荤菜数，实际构造菜品并逐一枚举所有套餐（2 荤 2 素）计数。"""
from itertools import combinations

OPTIONS = {"A": 4, "B": 5, "C": 6, "D": 7}
TARGET = 210

def meals(meat):
    veg = meat - 2
    meats = [f"荤{i}" for i in range(meat)]
    vegs = [f"素{i}" for i in range(max(veg, 0))]
    return sum(1 for m in combinations(meats, 2) for v in combinations(vegs, 2))

hits = [k for k, h in OPTIONS.items() if meals(h) == TARGET]
# 更大范围内也只有一个解
assert [h for h in range(2, 40) if meals(h) == TARGET] == [OPTIONS[k] for k in hits]
assert len(hits) == 1, hits
print({k: meals(h) for k, h in OPTIONS.items()})
print(hits[0])
