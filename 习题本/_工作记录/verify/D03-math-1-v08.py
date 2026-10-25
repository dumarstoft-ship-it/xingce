# D03-math-1-v08: 甲前一半时间10、后一半时间6；乙前一半路程10、后一半路程6；甲早到6分钟；求路程
from fractions import Fraction as F

V1, V2, EARLY = 10, 6, F(6, 60)
OPTS = {'A': F(6), 'B': F(45, 4), 'C': F(12), 'D': F(20)}

def time_jia(S):
    # 甲：总用时 T，前 T/2 以 V1、后 T/2 以 V2，走完 S：V1·T/2 + V2·T/2 = S
    return F(2) * S / (V1 + V2)

def time_yi(S):
    # 乙：前 S/2 以 V1、后 S/2 以 V2
    return (S / 2) / V1 + (S / 2) / V2

sols = set()
for k in range(1, 20001):           # 路程 0.01~200 千米，步长 0.01
    S = F(k, 100)
    if time_yi(S) - time_jia(S) == EARLY:
        sols.add(S)
assert len(sols) == 1, sols
S = sols.pop()

# 逐分钟模拟复核（时间单位：分钟，速度换算成千米/分钟）
def simulate_jia(T_min):
    pos = F(0)
    for m in range(T_min):
        pos += F(V1 if m < T_min // 2 else V2, 60)
    return pos
Tj = time_jia(S) * 60
assert Tj.denominator == 1 and Tj % 2 == 0 and simulate_jia(int(Tj)) == S
pos, m = F(0), 0
while pos < S:
    pos += F(V1 if pos < S / 2 else V2, 60); m += 1
assert pos == S and m - Tj == 6     # 乙晚 6 分钟

hit = [k for k, x in OPTS.items() if x == S]
assert len(hit) == 1, (S, hit)
# 干扰项来源
Tj_h, Ty_h = time_jia(S), time_yi(S)
avg_yi, avg_jia = S / Ty_h, S / Tj_h
assert Tj_h * avg_yi == OPTS['B']                           # 甲的用时 × 乙的平均速度
assert F(1, 6) / (1 / avg_yi - 1 / avg_jia) == OPTS['D']    # 6分钟误作1/6小时
assert EARLY / (F(1) / (avg_jia * avg_yi)) == OPTS['A']     # 倒数差漏掉分子0.5（误作1/60）
print('S =', S, '甲用时', Tj, '分', '乙用时', m, '分')
print(hit[0])
