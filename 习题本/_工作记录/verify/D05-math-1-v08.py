"""D05-math-1-v08 验算：若干男网格员 + 4 名女网格员中选 3 人且男女都有，共 70 种，求男网格员人数。
对每个选项实际构造人员并枚举所有 3 人组合计数。"""
from itertools import combinations

OPTIONS = {"A": 5, "B": 6, "C": 7, "D": 8}
WOMEN, TARGET = 4, 70

def mixed(men):
    staff = ["男"] * men + ["女"] * WOMEN
    return sum(1 for s in combinations(range(len(staff)), 3)
               if len({staff[i] for i in s}) == 2)

hits = [k for k, x in OPTIONS.items() if mixed(x) == TARGET]
assert [x for x in range(1, 40) if mixed(x) == TARGET] == [OPTIONS[k] for k in hits]
assert len(hits) == 1, hits
print({k: mixed(x) for k, x in OPTIONS.items()})
print(hits[0])
