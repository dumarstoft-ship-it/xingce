# teacher_T004  10盏路灯，相邻(连续)2盏不能同时熄灭，共有多少种亮灯方式
from itertools import product
from math import comb

N = 10
OPTS = {'A': 55, 'B': 89, 'C': 144, 'D': 233}

# 穷举 2^10 种亮(1)/灭(0)状态
brute = sum(1 for s in product((0, 1), repeat=N) if all(s[i] or s[i + 1] for i in range(N - 1)))
# 状态递推：L(n)=L(n-1)+D(n-1)，D(n)=L(n-1)
L, D = 1, 1
for _ in range(2, N + 1):
    L, D = L + D, L
assert L + D == brute
# 插空法交叉核对：灭k盏，插入亮着的 N-k 盏形成的 N-k+1 个空
assert sum(comb(N - k + 1, k) for k in range(N // 2 + 1)) == brute
ans = brute
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['B'] == L and OPTS['A'] == D                        # 只算了末盏亮 / 末盏灭的一类
assert OPTS['B'] == sum(comb(N - k, k) for k in range(N // 2 + 1))  # 插空时空位数少算1
print('patterns =', ans)
print(hits[0])
