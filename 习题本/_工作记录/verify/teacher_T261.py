# T261 A 在 B 正北 30；可疑船自 B 向西，巡逻艇速度快 1/3，直线追击在 C 相遇，求 BC
import math
AB = 30.0
k_speed = 1 + 1/3                     # AC:BC = 4:3
# AC² = AB² + BC², AC = k·BC  ->  BC = AB / sqrt(k²-1)
BC = AB / math.sqrt(k_speed**2 - 1)
options = {"A": 26, "B": 28, "C": 30, "D": 34}
best = min(options, key=lambda k: abs(options[k] - BC))
assert abs(options[best] - BC) < 1, BC
print(best)
