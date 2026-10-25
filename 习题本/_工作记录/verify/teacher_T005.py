# teacher_T005  8户金额 2,9,6,1,4,3,3,8，相邻两户不能同晚被偷，求最高金额
from itertools import combinations

AMT = [2, 9, 6, 1, 4, 3, 3, 8]
OPTS = {'A': 15, 'B': 20, 'C': 21, 'D': 23}
n = len(AMT)

best = 0
for r in range(n + 1):
    for idx in combinations(range(n), r):
        if all(idx[i + 1] - idx[i] >= 2 for i in range(len(idx) - 1)):
            best = max(best, sum(AMT[i] for i in idx))
# 递推 f(i)=max(f(i-1), f(i-2)+a_i) 交叉核对
f = []
for i, a in enumerate(AMT):
    f.append(max(f[i - 1] if i >= 1 else 0, (f[i - 2] if i >= 2 else 0) + a))
assert f[-1] == best, (f, best)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
assert OPTS['A'] == sum(AMT[0::2])            # 只偷单号户
assert OPTS['D'] == 9 + 6 + 8                 # 贪心挑最大，忽略第2、3户相邻
print('dp table =', f)
print(hits[0])
