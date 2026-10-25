"""D05-math-1-v12 验算：7 座一排，领导坐正中（第 4 座），2 名副职坐紧挨两侧（第 3、5 座），
其余 4 人（含甲乙）坐剩下 4 座，甲乙座位相邻。穷举 7 人全排列。"""
from itertools import permutations

OPTIONS = {"A": 8, "B": 12, "C": 16, "D": 24}
people = ["领导", "副1", "副2", "甲", "乙", "丙", "丁"]

cnt = 0
for seat in permutations(people):            # seat[i] = 第 i+1 个座位上的人
    if seat[3] != "领导" or {seat[2], seat[4]} != {"副1", "副2"}:
        continue
    if abs(seat.index("甲") - seat.index("乙")) != 1:
        continue
    cnt += 1

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
