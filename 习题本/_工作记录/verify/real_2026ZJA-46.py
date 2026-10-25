# real_2026ZJA-46：甲、乙两池水深8米、5米，8:30起甲池水匀速注入乙池；甲池每小时降0.2米，乙池每小时升0.3米。
# 问何时水深相同。解法：逐分钟模拟水深（精确分数），并用方程 8-0.2t=5+0.3t 交叉检验。
from fractions import Fraction as F

OPTIONS = {'A': '14:30', 'B': '15:00', 'C': '15:30', 'D': '16:00'}
h_jia, h_yi = F(8), F(5)
d_jia, u_yi = F(2, 10), F(3, 10)
start = 8 * 60 + 30

t = 0
while h_jia > h_yi:
    h_jia -= d_jia / 60
    h_yi += u_yi / 60
    t += 1
assert h_jia == h_yi
t_eq = (F(8) - 5) / (d_jia + u_yi)          # 方程解（小时）
assert t_eq * 60 == t
end = start + t
ans = f"{end // 60}:{end % 60:02d}"
hits = [k for k, v in OPTIONS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('经过', t_eq, '小时，', ans, '水深均为', h_jia, '米')
print(hits[0])
