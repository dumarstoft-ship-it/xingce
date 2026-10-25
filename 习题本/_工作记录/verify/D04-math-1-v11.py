# D04-math-1-v11  进货价降低8%，售价不变，利润率提高10个百分点，求原利润率
from fractions import Fraction as F

A_DROP, K = F(8, 100), F(10, 100)


def gain(r, c0=F(100)):
    """原利润率为 r 时，进价降 8% 后利润率提高了多少（以小数计）。"""
    price = c0 * (1 + r)
    c1 = c0 * (1 - A_DROP)
    return (price - c1) / c1 - r


# 在万分之一精度上穷举原利润率（0~200%）
sols = [F(t, 10000) for t in range(0, 20001) if gain(F(t, 10000)) == K]
assert len(sols) == 1
r = sols[0]
assert gain(r, F(37)) == K       # 与进价赋值无关

OPTS = {'A': F(15), 'B': F(18), 'C': F(25), 'D': F(35)}   # 百分数
hits = [L for L, v in OPTS.items() if v == r * 100]
assert len(hits) == 1, hits
# 选项代入：只有正确项使利润率恰好提高10个百分点
assert [L for L, v in OPTS.items() if gain(v / 100) == K] == hits

# 干扰项来源核对
assert (A_DROP + K) * 100 == OPTS['B']                    # 8%+10% 直接相加
new_rate = (100 * (1 + r) - 92) / 92
assert new_rate * 100 == OPTS['C']                        # 新利润率（答非所问）
assert (K / A_DROP - 1) * 100 == OPTS['C']                # 结论式漏乘(1-a)
w = [F(t, 10000) for t in range(0, 20001) if 100 * (1 + F(t, 10000)) - 92 == 92 * F(t, 10000) + 10]
assert w and w[0] * 100 == OPTS['C']                      # 10个百分点按原进价100算成10元
assert ((1 + A_DROP) * K / A_DROP - 1) * 100 == OPTS['D']  # 结论式把(1-a)记成(1+a)
assert (1 - A_DROP) * K / A_DROP == 1 + r                 # 结论式 1+r=(1-a)k/a
# 说明：若把"提高10个百分点"误作"提高10%"，解得 r=8/1.2≈666.7%，明显荒谬，故不设为选项
assert F(8) / F(12, 10) > 6

print('r', r, 'new rate', new_rate)
print(hits[0])
