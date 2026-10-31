"""配速专练 10 题：逐题验算答案唯一、干扰项各对应一种错法（全部用分数精确计算，能穷举的穷举）"""
from fractions import Fraction as F
res = {}

# 1 骑车：15 km/h 迟到 4，18 km/h 早到 6；先慢后快准时，问快骑多少千米
p_slow, p_fast = F(60, 15), F(60, 18)                   # 分钟/千米
D = F(4 + 6) / (p_slow - p_fast); T = D * p_slow - 4
x = [x for x in [F(k, 4) for k in range(0, 4 * int(D) + 1)] if (D - x) * p_slow + x * p_fast == T]
assert D == 15 and T == 56 and x == [6]
res[1] = ('A', 6, {'C': D - 6, 'B': D / 2, 'D': D})       # 9 慢骑那段 / 7.5 各一半 / 15 全程

# 2 赛跑 1500 米：甲到终点时乙差 100、丙差 300；让乙先跑 20 秒同时到 → 丙要先跑几秒
sols = set()
for k in range(1, 400):                                 # 乙每米用时 b 按 0.001 秒一档穷举
    b = F(k, 1000); T = 1400 * b                         # 甲的全程用时 = 乙跑 1400 米的时间
    a = T / 1500
    if 1500 * b - 1500 * a == 20:
        c = T / 1200; sols.add(1500 * c - T)
assert sols == {70}
b = F(1, 5); T = 1400 * b; a = T / 1500; c = T / 1200
res[2] = ('C', 70, {'B': 20 * 3, 'A': 300 * a, 'D': 300 * (T + 20) / 1200})

# 3 施工降速 60%：多 6 千米多晚 4 分钟 → 平时速度
e = F(24 - 20, 6)                                       # 每千米多用的分钟
p = e / (1 / F(6, 10) - 1)                              # 平时配速
assert 60 / p == 60 and 20 / e == 30                    # 施工段 30 千米
res[3] = ('C', 60 / p, {'D': 60 / e, 'A': 60 / (e / F(4, 10)), 'B': 60 / (e / F(6, 10))})

# 4 上坡 12、平路 15、下坡 20；去比回多 16 分钟，往返 192 分钟
up, flat, down = F(60, 12), F(60, 15), F(60, 20)
slope = F(16) / (up - down); y = (192 - slope * (up + down)) / (2 * flat)
assert (slope, y) == (8, 16)
# 穷举 0.5 千米一档也只有这一组
sols = [(s, f) for s in [F(k, 2) for k in range(1, 100)] for f in [F(k, 2) for k in range(1, 100)]
        if s * up + f * flat - (s * down + f * flat) == 16 and s * (up + down) + 2 * f * flat == 192]
assert sols == [(8, 16)]
res[4] = ('A', slope + y, {'C': slope + (192 - slope * (up + down)) / flat, 'B': 2 * y, 'D': 2 * (slope + y)})

# 5 顺风 40 分钟、逆风 60 分钟，风速增减相同 → 无风往返
d = F(1); v_down, v_up = d / 40, d / 60; v0 = (v_down + v_up) / 2
assert 2 * d / v0 == 96
res[5] = ('B', 2 * d / v0, {'C': 40 + 60, 'A': 80, 'D': 120})

# 6 15 千米：甲配速 5、每跑完 2 千米歇 2 分钟；乙配速 6 不歇
rests = len([k for k in range(1, 15) if k % 2 == 0])     # 跑完第 2、4、…、14 千米后（终点不算）
ja, yi = 15 * 5 + 2 * rests, 15 * 6
assert (rests, ja, yi) == (7, 89, 90)
res[6] = ('D', yi - ja, {'A': 0, 'B': yi - (75 + 16), 'C': yi - (75 + 12)})

# 7 甲先出发 20 分钟，乙开 1 小时在 C 追上；乙停车 15 分钟后同时到 B；CB = 48 → 甲速
AC = 48 * F(20, 15)                                     # 少用的时间与路程成正比
v_jia = AC / F(80, 60); v_yi = AC / 1
assert (AC, v_jia, v_yi) == (64, 48, 64) and 48 / v_jia * 60 == 48 / v_yi * 60 + 15
res[7] = ('C', v_jia, {'D': v_yi, 'B': 48 / F(80, 60), 'A': 48 * F(15, 20) / F(80, 60)})

# 8 三车：乙晚 10 分钟在 30 千米追上甲；丙再晚 10 分钟在 40 千米追上甲 → 丙追上乙
d_jy, d_jb = F(10, 30), F(20, 40)                       # 甲比乙、甲比丙每千米多用的分钟
catch = 10 / (d_jb - d_jy)
for vj in [F(k) for k in range(20, 80)]:                 # 任取甲速，模拟验证与甲速无关
    pj = 60 / vj; py, pb = pj - d_jy, pj - d_jb
    assert py > pb > 0 and 10 + 30 * py == 30 * pj and 20 + 40 * pb == 40 * pj
    assert 20 + catch * pb == 10 + catch * py            # 丙、乙同时到 catch 处
assert catch == 60
res[8] = ('B', catch, {'A': 50, 'C': 30 + 40, 'D': 20 / (d_jb - d_jy)})

# 9 乙晚 20 分钟，在 30 千米处 C 地停车 10 分钟，90 千米处追上甲，最终早 20 分钟 → AB
diff = F(20 + 10, 90); AB = 90 + 20 / diff
for vj in [F(k) for k in range(30, 90)]:
    pj = 60 / vj; py = pj - diff
    assert py > 0 and 20 + 30 * py > 30 * pj           # 乙晚于甲到 C 地：此前没追上
    assert 20 + 90 * py + 10 == 90 * pj and 90 * pj + (AB - 90) * pj - (90 * pj + (AB - 90) * py) == 20
assert AB == 150
res[9] = ('B', AB, {'A': AB - 90, 'C': 90 + 20 / F(20, 90), 'D': 90 + 90 * F(30, 20)})

# 10 甲每千米比乙少用 30 秒；甲 1 小时到 B 后原速返回，在距 B 12 千米处遇乙 → AB
sols = []
for k in range(13, 400):                                # AB 按 0.5 千米一档穷举
    ab = F(k, 2); pj = 60 / ab; py = pj + F(1, 2)
    if (ab + 12) * pj == (ab - 12) * py: sols.append(ab)
assert sols == [60]
res[10] = ('C', 60, {'A': 60 - 12, 'D': 60 + 12})

ORDER = [5, 6, 3, 1, 7, 2, 9, 4, 10, 8]
for n, k in enumerate(ORDER, 1):
    a, v, traps = res[k]
    print(n, a, v, {t: (float(x) if isinstance(x, F) else x) for t, x in traps.items()})
