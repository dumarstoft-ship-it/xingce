# teacher_T002  爬10级楼梯，每次爬1级或2级，有多少种方法
from itertools import product

N, STEPS = 10, (1, 2)
OPTS = {'A': 6, 'B': 55, 'C': 89, 'D': 144}

# 递推：f(n) = f(n-1) + f(n-2)，f(0) = 1
f = [1] + [0] * N
for n in range(1, N + 1):
    f[n] = sum(f[n - s] for s in STEPS if n - s >= 0)
# 穷举所有步长序列独立核对
brute = sum(1 for L in range(1, N + 1) for seq in product(STEPS, repeat=L) if sum(seq) == N)
assert brute == f[N], (brute, f[N])
ans = f[N]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
# 干扰项来源
assert OPTS['A'] == len({seq.count(2) for L in range(1, N + 1) for seq in product(STEPS, repeat=L) if sum(seq) == N})  # 只数"用几次2级"
assert OPTS['B'] == f[N - 1] and OPTS['D'] == f[N] + f[N - 1]   # 递推错一位
print('ways =', ans)
print(hits[0])
