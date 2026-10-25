# T258 AB=2km, DB=1km, DB⊥AB；D 站半径 DB，A 站半径 AE（E 为 AD 与 D 圆交点）
# 小林从 B 沿 BA 以 4km/h 行进，多久后重新收到信号（√5≈2.23）
import math
AB, DB, v = 2.0, 1.0, 4.0
sqrt5 = 2.23                               # 题给近似值
AD = sqrt5                                 # √(AB²+DB²)
AE = AD - DB                               # A 站信号半径
# 从 B 出发：到 D 的距离 √(DB²+s²) ≥ DB，立即离开 D 站范围；到 A 的距离 AB-s ≤ AE 时进入 A 站范围
assert abs(math.hypot(AB, DB) - AD) < 0.01
s_needed = AB - AE                         # 盲区 BC
minutes = s_needed / v * 60
options = {"A": 8, "B": 10, "C": 12, "D": 14}
best = min(options, key=lambda k: abs(options[k] - minutes))
assert abs(options[best] - minutes) < 1, minutes
print(best)
