# T213（2013山东）第k个人往所有编号为k的倍数的罐子倒1毫升水（k=1..100），第92号罐有多少毫升。
JARS, PEOPLE, TARGET = 100, 100, 92
OPTS = {'A': 2, 'B': 6, 'C': 46, 'D': 92}
water = [0] * (JARS + 1)
for k in range(1, PEOPLE + 1):
    for j in range(k, JARS + 1, k):
        water[j] += 1
hits = [kk for kk, v in OPTS.items() if v == water[TARGET]]
assert len(hits) == 1, (water[TARGET], hits)
print('jar 92 =', water[TARGET])
print(hits[0])
