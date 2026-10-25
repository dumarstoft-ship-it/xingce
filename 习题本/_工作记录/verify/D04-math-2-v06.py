# D04-math-2-v06 降价只能是2元整数倍：枚举降价次数
cost, p0, q0, step, inc = 60, 100, 80, 2, 15
def profit(n):
    return (p0 - step * n - cost) * (q0 + inc * n)
ns = range(0, (p0 - cost) // step + 1)
vals = sorted(((profit(n), n) for n in ns), reverse=True)
assert vals[0][0] > vals[1][0]
best = vals[0][1]
price = p0 - step * best
# 误读“每降1元多卖15台”（仍取偶数降价额）
mis = max(range(0, 41, 2), key=lambda x: (p0 - x - cost) * (q0 + inc * x))
mis_any = max(range(0, 41), key=lambda x: (p0 - x - cost) * (q0 + inc * x))   # 误读且不按2元整数倍
assert p0 - mis == 82 and p0 - mis_any == 83
print('best n =', best, 'price =', price, 'top3 =', vals[:3], 'misread ->', p0 - mis, 'misread any-int ->', p0 - mis_any)
options = {'A': 82, 'B': 84, 'C': 85, 'D': 86}
valid = {k: (p0 - v) % step == 0 for k, v in options.items()}
hits = [k for k, v in options.items() if v == price and valid[k]]
assert len(hits) == 1, hits
print(hits[0])
