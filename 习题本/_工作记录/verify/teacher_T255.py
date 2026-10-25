# T255 航天器在北极正上方 S，切线恰好切在北纬 45° 线上，求 S 到北极点距离（R=1）
import math
R = 1.0
lat = math.radians(45)
# 切点 C 与地心连线和地轴夹角 = 90° - 纬度；切线 ⊥ 半径 → OS = R / cos(夹角)
ang = math.pi / 2 - lat
OS = R / math.cos(ang)
SA = OS - R
s2 = math.sqrt(2)
options = {"A": (s2 - 1) / 2, "B": (2 - s2) / 2, "C": s2 - 1, "D": 2 - s2}
hits = [k for k, v in options.items() if abs(v - SA) < 1e-9]
assert len(hits) == 1, (SA, hits)
print(hits[0])
