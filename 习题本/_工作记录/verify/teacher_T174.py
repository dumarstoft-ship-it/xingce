# teacher T174（2019辽宁）羊单独吃16天；牛先交替整数天吃完；羊先交替多吃半天；牛单独吃几天
# 注：按题给数据，“牛先交替恰好整数天”与其他条件不能同时成立（见issues），这里以
#     “羊先比牛先多用半天”这一可检验条件逐项检验选项，并打印牛先方式的实际天数。
from fractions import Fraction as F

OPTS = {'A': 8, 'B': 7, 'C': 6, 'D': 5}
SHEEP_DAYS = 16

def finish(cycle, total):
    eaten, t = F(0), 0
    while True:
        r = cycle[t % 2]
        if eaten + r >= total:
            return t + (total - eaten) / r
        eaten += r
        t += 1

ok = []
for key, cow_days in OPTS.items():
    s = F(1)
    total = SHEEP_DAYS * s
    c = total / cow_days
    t_cow_first = finish((c, s), total)
    t_sheep_first = finish((s, c), total)
    print(key, '牛单独', cow_days, '天 | 牛先', t_cow_first, '| 羊先', t_sheep_first, '| 差', t_sheep_first - t_cow_first)
    if t_sheep_first - t_cow_first == F(1, 2):
        ok.append(key)
assert len(ok) == 1, ok
print(ok[0])
