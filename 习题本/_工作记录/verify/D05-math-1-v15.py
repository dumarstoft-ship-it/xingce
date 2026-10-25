"""D05-math-1-v15 验算：周一至周日选 3 天分别开展 3 项不同活动（每天至多 1 项），
任意两项之间至少间隔 1 天。枚举"活动→日期"的全部有序分配。"""
from itertools import permutations

OPTIONS = {"A": 10, "B": 18, "C": 24, "D": 60}
days = range(7)
cnt = 0
for d in permutations(days, 3):              # d[i] = 第 i 项活动的日期
    s = sorted(d)
    if all(s[i + 1] - s[i] - 1 >= 1 for i in range(2)):   # 两次之间至少空 1 天
        cnt += 1

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
