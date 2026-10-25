# teacher_T003  2024浙江A-70：每次最多拿3串，正好吃10串，共有多少种拿法
from itertools import product

N, STEPS = 10, (1, 2, 3)
OPTS = {'A': 44, 'B': 81, 'C': 149, 'D': 274}

f = [1] + [0] * N                      # f(0)=1 代表"还没拿"的状态
for n in range(1, N + 1):
    f[n] = sum(f[n - s] for s in STEPS if n - s >= 0)
brute = sum(1 for L in range(1, N + 1) for seq in product(STEPS, repeat=L) if sum(seq) == N)
assert brute == f[N], (brute, f[N])
ans = f[N]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert (OPTS['A'], OPTS['B'], OPTS['C']) == (f[7], f[8], f[9])   # 干扰项是递推前几项（下标错位）
print('f =', f)
print(hits[0])
