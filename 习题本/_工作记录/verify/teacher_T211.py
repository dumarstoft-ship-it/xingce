# T211（2015河南）1~50号选手爬60层楼：第1层人人得号牌，之后经过第k层（k=2..60）时编号是k的倍数再得一个。
# 恰好持有3个号牌的选手有多少人。
PLAYERS, FLOORS, TARGET = range(1, 51), 60, 3
OPTS = {'A': 1, 'B': 4, 'C': 7, 'D': 10}
cnt = {n: 1 + sum(1 for k in range(2, FLOORS + 1) if n % k == 0) for n in PLAYERS}
who = [n for n in PLAYERS if cnt[n] == TARGET]
hits = [k for k, v in OPTS.items() if v == len(who)]
assert len(hits) == 1, (who, hits)
print('players =', who)
print(hits[0])
