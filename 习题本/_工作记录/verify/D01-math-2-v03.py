# D01-math-2-v03 盈盈型分配 + 改标准后新增人数
opts = {'A': 21, 'B': 24, 'C': 36, 'D': 57}
a, r1 = 7, 90     # 每人7盒，剩90盒
b, r2 = 9, 18     # 每人9盒，剩18盒
c = 6             # 加人后每人6盒，恰好发完

sols = []
for n in range(1, 5001):          # 原来的环卫工人数
    if a * n + r1 == b * n + r2:
        T = a * n + r1            # 凉茶总盒数
        if T % c == 0 and T // c > n:
            sols.append((n, T, T // c - n))
assert len(sols) == 1, sols
n, T, new = sols[0]

# 干扰项的错误路径
n_wrong = (r1 + r2) // (b - a)                      # 两次都剩却用"剩余之和"
assert (r1 + r2) % (b - a) == 0
assert (a * n_wrong + r1) // c - n_wrong == opts['B']
assert n == opts['C']                               # 答成原有人数
assert T // c == opts['D']                          # 答成现有总人数

hits = [k for k, v in opts.items() if v == new]
assert len(hits) == 1, hits
print('n =', n, 'total =', T, 'new =', new)
print(hits[0])
