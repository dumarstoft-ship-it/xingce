# D07-math-1-v12: B 在 A 北偏东 20° 8 千米，C 在 A 南偏东 40° 8 千米，求 BC
import math

def pos(bearing_deg, dist):               # 方位角：从正北顺时针量
    t = math.radians(bearing_deg)
    return (dist * math.sin(t), dist * math.cos(t))

B = pos(20, 8)            # 北偏东 20°
C = pos(180 - 40, 8)      # 南偏东 40°
d = math.dist(B, C)
opts = {'A': 4 * math.sqrt(3), 'B': 8, 'C': 8 * math.sqrt(2), 'D': 8 * math.sqrt(3)}
hit = [k for k, v in opts.items() if abs(v - d) < 1e-9]
assert len(hit) == 1, (d, hit)
print('BC ≈', round(d, 6))
print(hit[0])
