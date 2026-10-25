# D03-math-1-v02: 路程之和为全长1/3时甲距A端800米；为全长5/6时乙距B端3000米；求线路全长
from fractions import Fraction as F

R1, D1 = F(1, 3), 800      # 第一个时刻：两人路程和 = 全长×R1，甲已走 D1
R2, D2 = F(5, 6), 3000     # 第二个时刻：两人路程和 = 全长×R2，乙已走 D2
OPTS = {'A': 4560, 'B': 4800, 'C': 5400, 'D': 6000}

sols, only1 = set(), set()
# 穷举全长 S（1米步长，至 30000 米）；甲的速度占比 a = v甲/(v甲+v乙) 由第一个条件确定，再检验第二个条件
for S in range(1, 30001):
    t1, t2 = S * R1, S * R2          # 以“两人合计速度=1”为时间单位，路程和即时间
    a = F(D1) / t1                   # 第一个时刻甲走了 D1
    if not (0 < a < 1):
        continue
    only1.add(S)
    if (1 - a) * t2 == D2:           # 第二个时刻乙走了 D2
        assert t2 < S                # 此时两人尚未相遇
        sols.add((S, a))
assert len(only1) > 1                # 只用第一个条件，全长不唯一
assert len(sols) == 1, sols          # 两个条件合用，全长唯一
S, a = sols.pop()
# 逐步模拟复核：两人以 a:(1-a) 的速度比相向而行，按 1 米合计路程推进
pa = pb = F(0)
while pa + pb < S:
    pa += a; pb += 1 - a
    if pa + pb == S * R1: assert pa == D1
    if pa + pb == S * R2: assert pb == D2
assert pa + pb == S
hit = [k for k, v in OPTS.items() if v == S]
assert len(hit) == 1, (S, hit)
# 干扰项来源
assert F(D1 + D2) / R2 == OPTS['A']                  # 两个时刻路程直接相加再除以5/6
assert 2 * (D1 / R1) == OPTS['B']                    # 以为在中点相遇：2400×2
assert D1 / R1 + D2 == OPTS['C']                     # 只放大甲，乙的3000米没放大
print('S =', S, 'a =', a, '甲相遇时走', a * S, '乙相遇时走', (1 - a) * S)
print(hit[0])
