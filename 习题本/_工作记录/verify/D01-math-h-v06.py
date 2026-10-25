# D01-math-h-v06  每次花同样多的钱买荔枝：原价买300斤；第二次降价后买400斤；
# 第三次在第二次基础上又降2元/斤，买480斤。求原价（元/斤）。
from fractions import Fraction as F

OPTS = {'A': F(8), 'B': F(48, 5), 'C': F(15), 'D': F(16)}
Q1, Q2, Q3 = 300, 400, 480      # 三次采购的斤数
DROP2 = 2                       # 第三次比第二次每斤又低2元
N = 200000                      # 经费穷举上限（单位：角）

# 穷举每次的经费M（精确到角），单价＝经费÷斤数，须满足两次降价且第二次又降2元
sols = []
for m10 in range(1, N + 1):
    m = F(m10, 10)
    p1, p2, p3 = m / Q1, m / Q2, m / Q3
    if p1 > p2 > p3 and p2 - p3 == DROP2:
        sols.append((m, p1, p2, p3))
assert len(sols) == 1, sols
m, p1, p2, p3 = sols[0]
hits = [k for k, v in OPTS.items() if v == p1]
assert len(hits) == 1, hits

# 干扰项来源核对
k = F(DROP2, Q2 - Q1)                         # 误把单价比写成 480:400:300（顺序倒过来）
assert Q3 * k == OPTS['B']
# 误以为“数量多几分之几，单价就降几分之几”
r1, r2 = F(Q2 - Q1, Q1), F(Q3 - Q2, Q2)
p2_bad = DROP2 / r2                            # 第二次单价 × r2 ＝ 2元
assert p2_bad / (1 - r1) == OPTS['C']
# 误把2元当成第一次降价（原价→第二次），单价比仍按 1/300:1/400:1/480
unit = F(DROP2) / (F(1, Q1) - F(1, Q2))       # 对应的经费
assert unit / Q1 == OPTS['A']
print('money', m, 'prices', p1, p2, p3)
print(hits[0])
