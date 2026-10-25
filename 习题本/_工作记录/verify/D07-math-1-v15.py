# D07-math-1-v15: 甲船 30 千米/时沿北偏东 40°，乙船 40 千米/时沿东偏南 40°，同时同地出发，几小时后相距 140 千米
import math

def heading(bearing_deg):
    t = math.radians(bearing_deg)
    return (math.sin(t), math.cos(t))

h_jia = heading(40)            # 北偏东 40°
h_yi = heading(90 + 40)        # 东偏南 40°：由正东向南转 40°
V_JIA, V_YI, TARGET = 30, 40, 140

def gap(t):
    pj = (V_JIA * t * h_jia[0], V_JIA * t * h_jia[1])
    py = (V_YI * t * h_yi[0], V_YI * t * h_yi[1])
    return math.dist(pj, py)

lo, hi = 0.0, 100.0
for _ in range(200):
    mid = (lo + hi) / 2
    if gap(mid) < TARGET:
        lo = mid
    else:
        hi = mid
t = (lo + hi) / 2
opts = {'A': 2, 'B': 2.8, 'C': 3.5, 'D': 14}
hit = [k for k, v in opts.items() if abs(v - t) < 1e-6]
assert len(hit) == 1, (t, hit)
print('t ≈', round(t, 6))
print(hit[0])
