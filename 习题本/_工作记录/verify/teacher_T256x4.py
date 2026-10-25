# T256x4（2024河北）乐道（外圆）、福道（内圆=湖边），AB=50；李速=6×妈速，妈一圈时间=4×李一圈时间；π取3，求湖面积（万平方米）
from fractions import Fraction as F
v_ratio = F(6)                 # 李/妈 速度
t_ratio = F(1, 4)              # 李/妈 一圈时间
C_ratio = v_ratio * t_ratio    # 外圆周长/内圆周长 = 半径比
gap = F(50)
r = gap / (C_ratio - 1)        # 内圆半径
area = 3 * r * r
area_wan = area / 10000
options = {"A": 2, "B": 3, "C": 4, "D": 6}
hits = [k for k, v in options.items() if v == area_wan]
assert len(hits) == 1, (area_wan, hits)
print(hits[0])
