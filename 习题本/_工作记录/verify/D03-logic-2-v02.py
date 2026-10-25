"""D03-logic-2-v02 数据验算（政务服务中心“一窗通办”）。

从题面数据出发：日均办件量 600 → 720，区里据此认为窗口工作效率提高了 20%。
效率 = 办件量 ÷ 对外服务时间。逐项读取各选项给出的、与效率分母（服务时间、人手）
有关的量化信息，计算效率实际变化，找出能推翻“效率提高 20%”的选项，并确认恰好一项。
"""
from fractions import Fraction as F

vol_before, vol_after = 600, 720          # 题面：日均办件量
claimed_gain = F(20, 100)                  # 题面：区里认为效率提高 20%

# 题面论证：把办件量增幅直接当成效率增幅
vol_gain = F(vol_after, vol_before) - 1
assert vol_gain == claimed_gain, vol_gain

# 各选项中与效率分母有关的量化信息：(改革前小时数, 改革后小时数)；
# None 表示该项没有给出服务时间或人手的变化，无法改变“效率”的计算。
option_hours = {
    'A': (6, 8),   # 对外服务时间由 6 小时延长到 8 小时
    'B': None,     # 群众办一件事要跑的窗口 3→1：群众端指标，不是窗口办件效率的分母
    'C': None,     # 新增业务的类别构成，无时间、人手信息
    'D': None,     # 另一中心办件量不变：对照信息，不涉及本中心的服务时间
}

refuters = []
for letter, hrs in option_hours.items():
    if hrs is None:
        continue
    h0, h1 = hrs
    per_hour_before = F(vol_before, h0)
    per_hour_after = F(vol_after, h1)
    eff_gain = per_hour_after / per_hour_before - 1
    print(letter, 'per-hour', per_hour_before, '->', per_hour_after, 'efficiency change', eff_gain)
    if eff_gain < claimed_gain:          # 实际效率增幅达不到所称的 20%（此处为负）
        refuters.append((letter, eff_gain))

assert len(refuters) == 1, refuters
letter, gain = refuters[0]
assert gain == F(-1, 10), gain             # 每小时办件 100 → 90，反降 10%（与解析一致）
print(letter)
