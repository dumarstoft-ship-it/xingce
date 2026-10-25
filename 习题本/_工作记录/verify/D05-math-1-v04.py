"""D05-math-1-v04 验算：3 男 3 女选 4 人，女生不少于 2 名，并从入选男生中指定 1 名队长。
枚举所有 4 人组合及队长人选。"""
from itertools import combinations

OPTIONS = {"A": 12, "B": 18, "C": 21, "D": 36}
people = [("男", i) for i in range(3)] + [("女", i) for i in range(3)]

cnt = 0
for team in combinations(people, 4):
    if sum(p[0] == "女" for p in team) < 2:
        continue
    for leader in team:
        if leader[0] == "男":
            cnt += 1

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
