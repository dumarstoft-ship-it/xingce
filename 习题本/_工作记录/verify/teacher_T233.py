# T233 正四棱锥伞：伞骨 PC 长度不变，∠CPQ 由 30° 变为 60°，求正方形面积倍数
import math
L = 1.0                                   # 伞骨长（不变量）
def square_area(angle_deg):
    half_diag = L * math.sin(math.radians(angle_deg))   # CQ = PC·sin∠CPQ，Q 为底面中心
    diag = 2 * half_diag
    return diag**2 / 2
ratio = square_area(60) / square_area(30)
options = {"A": 3*math.sqrt(2), "B": math.sqrt(3), "C": 2.0, "D": 3.0}
hits = [k for k, v in options.items() if abs(v - ratio) < 1e-9]
assert len(hits) == 1, (ratio, hits)
print(hits[0])
