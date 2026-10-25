# T212（2020北京区级）不到100人平均分成N组（N>1，每组人数>1），每组人数恰有6种可能，求人数最小值与最大值之差。
LIMIT, WAYS = 100, 6
OPTS = {'A': 32, 'B': 48, 'C': 56, 'D': 64}
ok = [n for n in range(1, LIMIT) if sum(1 for d in range(2, n) if n % d == 0) == WAYS]
ans = max(ok) - min(ok)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('possible headcounts =', ok)
print(hits[0])
