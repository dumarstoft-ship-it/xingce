# T225（2023福建）计价器残留两位数ab；匀速行驶1小时显示ba，2小时显示a0b；车费按里程计，求应付车费。
OPTS = {'A': 82, 'B': 86, 'C': 90, 'D': 95}
fares = set()
for a in range(1, 10):
    for b in range(1, 10):            # ba 也是两位数，b≠0
        s0, s1, s2 = 10 * a + b, 10 * b + a, 100 * a + b
        if s1 - s0 == s2 - s1 > 0:    # 匀速：两段车费相等
            fares.add(s2 - s0)
assert len(fares) == 1, fares
ans = fares.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('fare =', ans)
print(hits[0])
