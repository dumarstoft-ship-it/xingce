# T240 长方体 12×4×3 表面从 A 爬到对角顶点 C' 的最短路程
import math, itertools
dims = (12, 4, 3)
cands = []
for i in range(3):
    single = dims[i]
    rest = sum(dims) - single
    cands.append(single**2 + rest**2)   # 展开后两直角边：一条棱、另两条棱之和
best_sq = min(cands)
options = {"A": 13**2, "B": 193, "C": 241, "D": 17**2}
hits = [k for k, v in options.items() if v == best_sq]
assert len(hits) == 1, (best_sq, hits)
print(hits[0])
