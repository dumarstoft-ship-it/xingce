# D02-math-2-v02：甲池底面积是乙池2倍，7:30 时水深 9 米、3 米，甲池水匀速抽入乙池，甲池每小时降 0.25 米。
# 求两池水深相同的时刻。解法：按体积守恒逐分钟模拟（精确分数）。
from fractions import Fraction as F

OPTIONS = {'A': '13:30', 'B': '15:30', 'C': '19:30', 'D': '23:30'}
S_yi = F(1)
S_jia = 2 * S_yi
h_jia, h_yi = F(9), F(3)
drop_per_hour = F(1, 4)
start = 7 * 60 + 30

t = 0                                   # 分钟
while h_jia > h_yi:
    dv = S_jia * drop_per_hour / 60      # 每分钟从甲池抽出的体积
    h_jia -= dv / S_jia
    h_yi += dv / S_yi
    t += 1
assert h_jia == h_yi, (h_jia, h_yi)     # 恰在整分钟相等
end = start + t
ans = f"{end // 60}:{end % 60:02d}"

hits = [k for k, v in OPTIONS.items() if v == ans]
assert len(hits) == 1, (ans, hits)


def clock(h):
    m = start + int(h * 60)
    return f"{m // 60}:{m % 60:02d}"


# 干扰项来源：忽略面积差(乙也升0.25)→12小时；面积比颠倒(乙升0.125)→16小时；误把末水深当平均数6米、按乙池算→6小时
assert clock(F(6) / F(1, 2)) == OPTIONS['C']
assert clock(F(6) / (F(1, 4) + F(1, 8))) == OPTIONS['D']
assert clock((F(6) - 3) / F(1, 2)) == OPTIONS['A']
print('相同时刻', ans, '此时水深', h_jia)
print(hits[0])
