# D01-math-2-v09 两所高校志愿者：总数120，男66；甲男比乙女多9，求乙校人数
opts = {'A': 57, 'B': 63, 'C': 66, 'D': 75}
N, male, d = 120, 66, 9

yi_totals = set()
count = 0
for jm in range(N + 1):              # 甲男
    for ym in range(N + 1):          # 乙男
        if jm + ym != male:
            continue
        yf = jm - d                  # 乙女
        if yf < 0:
            continue
        jf = N - jm - ym - yf        # 甲女
        if jf < 0:
            continue
        yi_totals.add(ym + yf)
        count += 1
assert count > 1                     # 单个量不唯一（设而不求）
assert len(yi_totals) == 1, yi_totals
ans = yi_totals.pop()

# 干扰项的错误路径
female = N - male
assert female + d == opts['B']       # 求成甲校（甲=女总数+9）就停下
assert male == opts['C']             # 漏减9
assert male + d == opts['D']         # 方向弄反

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('yi total =', ans, 'feasible splits =', count)
print(hits[0])
