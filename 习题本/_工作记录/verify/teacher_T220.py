# T220（2008湖北）小于100的整数，与5的差是4的倍数，与5的和是7的倍数，这个数最大是多少。
OPTS = {'A': 65, 'B': 89, 'C': 93, 'D': 97}
ok = [x for x in range(-1000, 100) if (x - 5) % 4 == 0 and (x + 5) % 7 == 0]
ans = max(ok)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
# 干扰项来源核对
assert OPTS['A'] in ok and OPTS['A'] < ans                          # 少取一个周期
assert OPTS['B'] % 4 == 1 and OPTS['B'] % 7 == 5                    # 把x+5≡0(mod 7)错成x≡5(mod 7)
assert (OPTS['D'] - 5) % 4 == 0 and (OPTS['D'] + 5) % 7 != 0        # 只满足第一个条件
print('solutions below 100 (top) =', ok[-4:])
print(hits[0])
