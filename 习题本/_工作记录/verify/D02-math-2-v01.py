# D02-math-2-v01：育苗池一进一排。进水管6小时注满空池，排水管8小时排空满池；
# 先单开进水管2小时，再两管同开，问从打开排水管起还需几小时注满。
# 解法：分段计算 + 逐分钟步进模拟交叉检验（精确分数），从题面数据求时间，再对照选项。
from fractions import Fraction as F

OPTIONS = {'A': 16, 'B': 18, 'C': 22, 'D': 24}
FULL = F(1)
r_in, r_out = FULL / 6, FULL / 8

level = r_in * 2                      # 前 2 小时只进不排
assert level < FULL
need = (FULL - level) / (r_in - r_out)

# 交叉检验：逐 1/60 小时步进模拟
lv, t, step = level, F(0), F(1, 60)
while lv < FULL:
    lv += (r_in - r_out) * step
    t += step
assert t == need and lv == FULL

hits = [k for k, v in OPTIONS.items() if v == need]
assert len(hits) == 1, (need, hits)
# 干扰项来源：全程 2+16=18；两管从空池同开 24；24-2=22
assert 2 + need == OPTIONS['B'] and FULL / (r_in - r_out) == OPTIONS['D'] and OPTIONS['D'] - 2 == OPTIONS['C']
print('还需小时数 =', need)
print(hits[0])
