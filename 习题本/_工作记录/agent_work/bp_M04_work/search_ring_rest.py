from fractions import Fraction as F
# 环形：甲每跑一圈用 a 分钟、跑完一圈休息 r 分钟；乙每圈 b 分钟不休息。同点同向出发。
# 甲累计圈数 g(t)；乙 t/b。求最小 t>0 使 g(t) - t/b = 1，并要求发生在甲跑动阶段内部（非起止点）。
def g(t, a, r):
    k = t // (a + r); s = t - k * (a + r)
    return k + min(s, a) / F(a)
res = []
for a in range(2, 9):
    for r in range(1, 5):
        for b in range(a + 1, 16):
            if F(1, a + r) <= F(1, b):  # 甲平均速度必须大于乙
                continue
            # 逐个跑动段解方程
            for k in range(0, 200):
                t0 = (a + r) * k
                # g = k + (t - t0)/a ；k + (t-t0)/a - t/b = 1
                t = (1 - k + F(t0, a)) / (F(1, a) - F(1, b))
                if t0 <= t <= t0 + a:
                    # 检查此前休息段是否已有"接触"（休息段内甲不动，差值递减，不会达到 1 后再…）
                    inner = t0 < t < t0 + a
                    res.append((a, r, b, k + 1, t, inner, F(t, b)))
                    break
for x in res:
    a, r, b, k, t, inner, laps = x
    if inner and t.denominator <= 2 and laps.denominator <= 4:
        print('甲每圈%s分休%s分 乙每圈%s分 -> 甲第%s段跑动时追上，t=%s 分，乙跑了%s圈' % (a, r, b, k, t, laps))
