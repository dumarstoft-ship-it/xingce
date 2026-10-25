"""D05-math-1-v02 验算：5 男 4 女志愿者；田径 2 男分别检录、计时；篮球男女各 1；跳水 2 女（同分工）。
把 9 人每人分到 {检录, 计时, 篮球, 跳水, 不去} 之一，穷举全部 5^9 种分派，按题面条件计数。"""
from itertools import product

OPTIONS = {"A": 360, "B": 720, "C": 1200, "D": 1440}
MALE = [True] * 5 + [False] * 4          # 0-4 男，5-8 女
JL, JS, LQ, TS, NO = range(5)            # 检录 计时 篮球 跳水 不去

cnt = 0
for f in product(range(5), repeat=9):
    if f.count(JL) != 1 or f.count(JS) != 1 or f.count(LQ) != 2 or f.count(TS) != 2:
        continue
    if not MALE[f.index(JL)] or not MALE[f.index(JS)]:
        continue
    lq = [i for i in range(9) if f[i] == LQ]
    if sum(MALE[i] for i in lq) != 1:
        continue
    ts = [i for i in range(9) if f[i] == TS]
    if any(MALE[i] for i in ts):
        continue
    cnt += 1

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
