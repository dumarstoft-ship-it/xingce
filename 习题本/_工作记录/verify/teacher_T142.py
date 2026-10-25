# teacher T142（2015河南）7本书原价共100元，补钱换掉一本后7本价格成整数等差数列、最贵26元，求最便宜
OPTS = {'A': 2, 'B': 6, 'C': 8, 'D': 14}
N, OLD_TOTAL, MAXP = 7, 100, 26
ok = []
for key, low in OPTS.items():
    diff = MAXP - low
    if diff <= 0 or diff % (N - 1):
        print(key, low, '最贵-最便宜不是6的倍数')
        continue
    d = diff // (N - 1)
    prices = [low + i * d for i in range(N)]
    extra = sum(prices) - OLD_TOTAL          # 补的钱 = 新书价 - 旧书价
    # 必须真的补了钱，且存在某本新书p，使被换掉的旧书价 p-extra 为正整数
    feasible = extra >= 1 and any(p - extra >= 1 for p in prices)
    print(key, low, '新总价', sum(prices), '补', extra, '可行' if feasible else '不可行')
    if feasible:
        ok.append(key)
assert len(ok) == 1, ok
print(ok[0])
