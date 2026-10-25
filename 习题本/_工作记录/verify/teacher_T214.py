# T214（T213变式）第k个人往所有编号为k的倍数的罐子倒k毫升水（k=1..100），第92号罐有多少毫升。
JARS, PEOPLE, TARGET = 100, 100, 92
OPTS = {'A': 76, 'B': 120, 'C': 167, 'D': 168}
water = [0] * (JARS + 1)
for k in range(1, PEOPLE + 1):
    for j in range(k, JARS + 1, k):
        water[j] += k
hits = [kk for kk, v in OPTS.items() if v == water[TARGET]]
assert len(hits) == 1, (water[TARGET], hits)
# 干扰项来源核对
divs = [d for d in range(1, TARGET + 1) if TARGET % d == 0]
assert sum(divs) - TARGET == OPTS['A']                # 漏掉92本身
assert sum(d for d in divs if d not in (2, 46)) == OPTS['B']   # 把4当质因数，只得1、4、23、92
assert sum(divs) - 1 == OPTS['C']                     # 漏掉第1个人
print('jar 92 =', water[TARGET], 'divisors =', divs)
print(hits[0])
