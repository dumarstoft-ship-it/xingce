# D03-math-1-v14: 村委会的车平时8:00到镇汽车站接人；某天他7:25到站后步行迎车，步行27分钟遇车，上车返回；求比平时早到多少分钟
from fractions import Fraction as F

USUAL = 8 * 60                 # 平时车到车站的时刻（分钟）
ARRIVE, WALK = 7 * 60 + 25, 27
OPTS = {'A': 4, 'B': 8, 'C': 16, 'D': 35}

def one_day(c, w, D):
    """车速 c、步速 w（米/分），村委会到车站 D 米；返回 (步行分钟数, 比平时早到的分钟数)"""
    depart = USUAL - F(D, c)                 # 车每天的出发时刻
    # 坐标：村委会为 0，车站为 D。人从 ARRIVE 起由 D 向 0 走；车从 depart 起由 0 向 D 开
    # 相遇时刻 t：D - w(t-ARRIVE) = c(t-depart)（需 t >= depart 且 t >= ARRIVE）
    t = (D + w * ARRIVE + c * depart) / F(w + c)
    if t < depart or t < ARRIVE:
        return None
    meet = c * (t - depart)
    if not (0 < meet < D):
        return None
    arrive_unit = t + meet / F(c)
    return t - ARRIVE, USUAL + F(D, c) - arrive_unit

results, n = set(), 0
# 穷举步速 40~120、车速 100~1500（米/分，整数）和若干路程，只保留“步行恰好27分钟”的情形
for w in range(40, 121):
    for c in range(100, 1501):
        for D in (4000, 6000, 9000, 15000):
            r = one_day(c, w, D)
            if r and r[0] == WALK:
                results.add(r[1]); n += 1
assert n > 1
assert len(results) == 1, results
ans = results.pop()
hit = [k for k, v in OPTS.items() if v == ans]
assert len(hit) == 1, (ans, hit)
# 干扰项来源
one_way = USUAL - (ARRIVE + WALK)
assert one_way == OPTS['B']                   # 只算单程
assert F(one_way, 2) == OPTS['A']             # 把“往返省时÷2”用反
assert USUAL - ARRIVE == OPTS['D']            # 提前到站的35分钟
print('情形数', n, '早到', ans, '分钟')
print(hit[0])
