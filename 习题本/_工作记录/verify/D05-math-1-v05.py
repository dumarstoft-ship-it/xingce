"""D05-math-1-v05 验算：8 名选手按半决赛名次分道（前四 3-6 道、五六 7-8 道、七八 1-2 道），
前四名中的甲、乙不能相邻道次。穷举 8 人到 8 条道的全部排列。"""
from itertools import permutations

OPTIONS = {"A": 24, "B": 48, "C": 72, "D": 96}
JIA, YI = 0, 1                       # 半决赛前四名为选手 0-3，甲乙是其中两人
cnt = 0
for lane in permutations(range(1, 9)):  # lane[i] = 选手 i 的道次
    if set(lane[0:4]) != {3, 4, 5, 6}:
        continue
    if set(lane[4:6]) != {7, 8} or set(lane[6:8]) != {1, 2}:
        continue
    if abs(lane[JIA] - lane[YI]) == 1:
        continue
    cnt += 1

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
