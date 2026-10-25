# real 2026GK-70: 甲胜乙 0.4；乙胜丙 = 2 x 丙胜丁；乙对甲、丙均取胜的概率 0.18（各场独立、无平局），求丙胜丁
from fractions import Fraction as F
p_jia_beats_yi = F(4, 10)
p_yi_beats_jia = 1 - p_jia_beats_yi          # 乒乓球无平局
target = F(18, 100)
# 乙胜甲 × 乙胜丙 = 0.18，乙胜丙 = 2x  =>  x = 0.18 / (乙胜甲 × 2)
x = target / (p_yi_beats_jia * 2)
assert 0 <= 2 * x <= 1
opts = {'A': F(1, 10), 'B': F(12, 100), 'C': F(15, 100), 'D': F(3, 10)}
# 逐项代回题设核对，确认恰好一个选项满足
ok = [L for L, v in opts.items() if 2 * v <= 1 and p_yi_beats_jia * 2 * v == target]
hit = [L for L, v in opts.items() if v == x]
assert len(hit) == 1 and ok == hit, (x, hit, ok)
print('x =', x)
print(hit[0])
