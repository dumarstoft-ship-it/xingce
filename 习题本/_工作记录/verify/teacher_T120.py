# T120 2014广东：15份公文分给甲乙丙，每人不少于3份且不多于10份
DOCS, LO, HI = 15, 3, 10
OPTS = {'A': 15, 'B': 18, 'C': 21, 'D': 28}
cnt = 0
for x in range(LO, HI + 1):
    for y in range(LO, HI + 1):
        z = DOCS - x - y
        if LO <= z <= HI:
            cnt += 1
# 上限是否起作用：去掉上限后计数不变
cnt_no_hi = sum(1 for x in range(LO, DOCS + 1) for y in range(LO, DOCS + 1) if DOCS - x - y >= LO)
assert cnt_no_hi == cnt
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('ways =', cnt)
print(hits[0])
