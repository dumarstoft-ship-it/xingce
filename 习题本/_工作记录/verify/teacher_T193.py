# T193 50个单元，两人轮流每次划1~5个，划最后一次者胜，甲先划，第一次划几个才能保证获胜。
TOTAL, LO, HI = 50, 1, 5
OPTS = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
win = [False] * (TOTAL + 1)          # win[r]: 剩r个、轮到自己时是否必胜（r=0时对手刚划完最后一次，自己已输）
for r in range(1, TOTAL + 1):
    win[r] = any(not win[r - k] for k in range(LO, HI + 1) if k <= r)
good = [k for k in range(LO, HI + 1) if k <= TOTAL and not win[TOTAL - k]]
hits = [kk for kk, v in OPTS.items() if v in good]
assert len(hits) == 1, (good, hits)
print('winning first moves =', good)
print(hits[0])
