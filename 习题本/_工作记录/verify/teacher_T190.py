# T190 5道题正确率95%、85%、75%、65%、50%，做对>=4道为优秀，求优秀率至少多少。
# 设100人：非优秀者每人至少错2题 => 非优秀 <= 错题总人次//2；再构造出达到上界的具体分配并核验。
N, RATES = 100, [95, 85, 75, 65, 50]
OPTS = {'A': 35, 'B': 40, 'C': 48, 'D': 50}
wrong = [N * (100 - r) // 100 for r in RATES]
upper = min(N, sum(wrong) // 2)
# 构造：反复让当前剩余错题最多的两道题配成一个"恰错2题"的人
rem = wrong[:]
people = []
while True:
    order = sorted(range(len(rem)), key=lambda i: -rem[i])
    i, j = order[0], order[1]
    if rem[i] == 0 or rem[j] == 0:
        break
    rem[i] -= 1
    rem[j] -= 1
    people.append({i, j})
# 剩余错题（若有）分给优秀者，每人至多错1题
leftover = sum(rem)
k = len(people)
assert all(len(p) == 2 for p in people)
assert k + leftover <= N
for q in range(len(RATES)):
    assert sum(1 for p in people if q in p) + rem[q] == wrong[q]
assert k == upper
excellent_rate = (N - k) * 100 // N
hits = [kk for kk, v in OPTS.items() if v == excellent_rate]
assert len(hits) == 1, (excellent_rate, hits)
print('max non-excellent =', k, 'min excellent % =', excellent_rate)
print(hits[0])
