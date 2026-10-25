# teacher T173（2019新疆）甲乙交替检测，两种顺序同天数后差56个，效率比9:5，求甲每天检测量
OPTS = {'A': 72, 'B': 99, 'C': 112, 'D': 126}
RA, RB, LEFT = 9, 5, 56
ok = []
for key, a in OPTS.items():
    if a * RB % RA:
        print(key, a, '乙的效率不是整数')
        continue
    b = a * RB // RA
    for n in range(1, 500):                       # 方式一（甲先）恰好n天完工，总量=w1
        w1 = sum(a if d % 2 == 0 else b for d in range(n))
        w2 = sum(b if d % 2 == 0 else a for d in range(n))   # 方式二（乙先）同样n天
        if w1 - w2 == LEFT:
            ok.append(key)
            print(key, a, '乙', b, '方式一天数可为', n, '(奇数)')
            break
assert len(ok) == 1, ok
print(ok[0])
