# D02-math-2-v03：景观水池半高处有排水口，水面高于排水口时匀速流出。
# 堵住排水口时进水管4小时注满空池；满池停止进水、打开排水口，6小时后水面降到排水口处。
# 排水口不堵，从空池注水，求注满时间。解法：先由"6小时降到排水口处"求流速，再逐步模拟注水过程。
from fractions import Fraction as F

OPTIONS = {'A': 5, 'B': 6, 'C': 8, 'D': 12}
FULL, HOLE = F(1), F(1, 2)
r_in = FULL / 4

# 排水实验：从满池开始只排不进，模拟到水面降到排水口处恰好用 6 小时，反求流速
leak = None
for k in range(1, 200):
    cand = F(k, 240)                      # 候选流速（满池的 k/240 每小时）
    if FULL - cand * 6 == HOLE:
        leak = cand
assert leak is not None


def fill_time():
    level, t, step = F(0), F(0), F(1, 120)   # 每半分钟一步
    while level < FULL:
        rate = r_in - (leak if level >= HOLE else 0)
        level += rate * step
        t += step
    return t, level


t, level = fill_time()
assert level == FULL
hits = [k for k, v in OPTIONS.items() if v == t]
assert len(hits) == 1, (t, hits)
# 干扰项：全程扣漏水→6；把流速当成6小时漏完整池(1/6)→2+6=8；两错叠加→12
assert FULL / (r_in - leak) == OPTIONS['B']
assert HOLE / r_in + (FULL - HOLE) / (r_in - FULL / 6) == OPTIONS['C']
assert FULL / (r_in - FULL / 6) == OPTIONS['D']
print('排水口流速', leak, '注满用时', t, '小时')
print(hits[0])
