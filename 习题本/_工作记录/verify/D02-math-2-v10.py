# D02-math-2-v10：甲班组单独12小时、乙班组单独18小时，按"甲2小时、乙1小时"轮流（甲先），求总用时。
# 解法：按班次逐段模拟（精确分数），换算成"x小时y分"再对照选项。
from fractions import Fraction as F

OPTIONS = {'A': '13小时20分', 'B': '13小时30分', 'C': '14小时', 'D': '15小时'}
rate = {'甲': F(1, 12), '乙': F(1, 18)}
blocks = [('甲', 2), ('乙', 1)]


def finish():
    done, t, i = F(0), F(0), 0
    while True:
        who, length = blocks[i % 2]
        if done + rate[who] * length >= 1:
            return t + (1 - done) / rate[who]
        done += rate[who] * length
        t += length
        i += 1


def fmt(h):
    m = h * 60
    assert m.denominator == 1
    m = int(m)
    return f"{m // 60}小时" + (f"{m % 60}分" if m % 60 else '')


ans = fmt(finish())
hits = [k for k, v in OPTIONS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
# 干扰项：按平均效率算→13小时30分；尾巴按乙效率→14小时；凑整周期→15小时
avg = (rate['甲'] * 2 + rate['乙'] * 1) / 3
assert fmt(1 / avg) == OPTIONS['B']
print('总用时', ans)
print(hits[0])
