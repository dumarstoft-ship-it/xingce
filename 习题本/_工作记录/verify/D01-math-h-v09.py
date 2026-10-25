# D01-math-h-v09  某海岛客运码头旅客发送量（修订版：两月合计加权）：
# 2025年9月比8月下降25%；2024年9月比8月下降40%；2025年8、9两月合计比2024年同期增长40%。
# 求2025年9月比2024年9月增长百分之几。
from fractions import Fraction as F

MOM_2025 = F(-25, 100)    # 2025年9月 vs 2025年8月
MOM_2024 = F(-40, 100)    # 2024年9月 vs 2024年8月
SUM_YOY = F(40, 100)      # 2025年8+9月 vs 2024年8+9月
OPTS = {'A': F(28, 100), 'B': F(40, 100), 'C': F(55, 100), 'D': F(60, 100)}

results = set()
for base in range(1, 501):                         # 2024年8月取任意基数，结果应与基数无关
    aug24 = F(base)
    sep24 = aug24 * (1 + MOM_2024)
    total25 = (aug24 + sep24) * (1 + SUM_YOY)
    # 2025年：sep25 = aug25 × (1 + MOM_2025)，且 aug25 + sep25 = total25
    aug25 = total25 / (2 + MOM_2025)
    sep25 = aug25 * (1 + MOM_2025)
    assert aug25 + sep25 == total25 and sep25 == aug25 * (1 + MOM_2025)
    results.add(sep25 / sep24 - 1)
assert len(results) == 1, results
g = results.pop()
hits = [k for k, v in OPTS.items() if v == g]
assert len(hits) == 1, (g, hits)

# 干扰项来源核对（以2024年8月=100）
aug24 = F(100); sep24 = aug24 * (1 + MOM_2024); total25 = (aug24 + sep24) * (1 + SUM_YOY)
aug25 = total25 / (2 + MOM_2025)
assert aug25 / aug24 - 1 == OPTS['A']                                # 算成8月同比
assert SUM_YOY == OPTS['B']                                          # 把两月合计增速当成9月增速
assert SUM_YOY + (MOM_2025 - MOM_2024) == OPTS['C']                  # 增长率直接加减
print('2025 Aug', aug25, 'Sep', aug25 * (1 + MOM_2025), 'Sep YoY', g)
print(hits[0])
