# D02-math-1-v12  口粮可供全队18天；吃6天后增援30人，提前3天吃完；求原有人数
OPTS = {'A': 90, 'B': 120, 'C': 150, 'D': 180}
D, FIRST, ADD, EARLY = 18, 6, 30, 3

# 穷举原有人数 n：总口粮（人·天）= 前6天 n 人 + 之后 (n+30) 人吃到第15天
sols = [n for n in range(1, 10000)
        if n * D == n * FIRST + (n + ADD) * (D - EARLY - FIRST)]
assert len(sols) == 1, sols
n = sols[0]
hits = [k for k, v in OPTS.items() if v == n]
assert len(hits) == 1, hits


def wrong(days):
    """增援队员吃的天数用错时，由 n*3 = 30*days 解出的人数。"""
    s = [m for m in range(1, 10000) if m * EARLY == ADD * days]
    return s[0]


# 干扰项来源核对
assert wrong(D - FIRST) == OPTS['B'] == n + ADD
assert wrong(D - EARLY) == OPTS['C']
assert wrong(D) == OPTS['D']
print('n', n)
print(hits[0])
