# T249x5（2023湖北）CD=24，A 处仰角：B 为 45°，C 为 31°（tan31°≈0.60），求石像 BC
import math
CD, tan31 = 24.0, 0.60
AD = CD / tan31
BD = AD * math.tan(math.radians(45))
BC = BD - CD
options = {"A": 20, "B": 18, "C": 16, "D": 14}
best = min(options, key=lambda k: abs(options[k] - BC))
assert abs(options[best] - BC) < 0.5, BC
print(best)
