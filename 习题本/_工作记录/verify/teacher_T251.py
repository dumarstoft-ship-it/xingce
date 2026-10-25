# T251 距离 100 米，仰角 30°→45° 用 11 秒，45°→60° 用 17 秒，前后平均上升速度比
import math
D = 100.0
hgt = lambda deg: D * math.tan(math.radians(deg))
v1 = (hgt(45) - hgt(30)) / 11
v2 = (hgt(60) - hgt(45)) / 17
ratio = v1 / v2
options = {"A": 0.89, "B": 0.91, "C": 1.12, "D": 1.10}
best = min(options, key=lambda k: abs(options[k] - ratio))
# 确认四舍五入到两位小数唯一对应
assert round(ratio, 2) == options[best], ratio
print(best)
