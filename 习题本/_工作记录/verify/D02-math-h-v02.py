# D02-math-h-v02  科考队45人，补给恰好够全队用28天。出发若干天后5人沿原路以原速度返回（返程补给从现有补给中带走），
# 其余队员继续考察，补给用完的时间比原计划推迟了2天。求5人开始返回时已出发几天。
OPTS = {'A': 4, 'B': 5, 'C': 6, 'D': 12}
N, T, K, LATER = 45, 28, 5, 2


def runs_out_on(x, back_days=None, extend_people=None):
    """逐天模拟补给（单位：人·天），返回补给恰好用完的那一天；中途耗尽或有零头则返回 None。
    x：出发 x 天后返回；返程天数 = 去程天数 x（原路原速）。"""
    back = x if back_days is None else back_days(x)
    stock = N * T
    for day in range(1, x + 1):          # 前 x 天全队消耗
        stock -= N
        if stock < 0:
            return None
    stock -= K * back                    # 返回者带走返程补给
    if stock < 0:
        return None
    rest = N - K
    day = x
    while stock > 0:
        day += 1
        stock -= rest
    return day if stock == 0 else None


sols = [x for x in range(1, T) if runs_out_on(x) == T + LATER]
assert len(sols) == 1, sols
x = sols[0]
hits = [k for k, v in OPTS.items() if runs_out_on(v) == T + LATER]
assert len(hits) == 1 and OPTS[hits[0]] == x, hits

# ---- 干扰项来源核对（差量式：返回者每人省下的 = 留下者多用的）----
saved = lambda per_returnee: K * per_returnee
assert [y for y in range(1, T) if saved(T - y) == (N - K) * LATER] == [OPTS['D']]       # 忘了返程补给，返回者只用 y 天
assert [y for y in range(1, T) if saved(T - 3 * y) == (N - K) * LATER] == [OPTS['A']]   # 返程补给按往返 2y 天带
assert [y for y in range(1, T) if saved(T - 2 * y) == N * LATER] == [OPTS['B']]         # 多用的 2 天按全部 45 人算
assert 2 * x == OPTS['D']                                                                # 12 也是返回者回到出发地的天数

print('x', x)
print(hits[0])
