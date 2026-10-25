# teacher T143（2020地市）每箱48个，第k天做k个，X天后恰为整数箱，X最小值所在范围
OPTS = {'A': (41, 60), 'B': (61, 10 ** 9), 'C': (1, 19), 'D': (20, 40)}
BOX = 48
X = next(x for x in range(1, 10 ** 6) if (x * (x + 1) // 2) % BOX == 0)
wrong = next(x for x in range(1, 10 ** 6) if (x * (x + 1)) % BOX == 0)   # 忘了除以2的错误
print('X最小 =', X, '| 忘除以2会得', wrong)
hits = [k for k, (lo, hi) in OPTS.items() if lo <= X <= hi]
assert len(hits) == 1, hits
print(hits[0])
