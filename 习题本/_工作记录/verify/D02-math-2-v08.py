# D02-math-2-v08：全程用新型吊装设备效率提高25%可提前6天；实际先用原有设备若干天再换新设备，提前4天。
# 求用原有设备的天数。解法：先枚举原计划天数T满足第一个条件，再枚举原有设备天数x逐日推算（精确分数）。
from fractions import Fraction as F

OPTIONS = {'A': 6, 'B': 8, 'C': 10, 'D': 20}
UP, EARLY_ALL, EARLY_PART = F(5, 4), 6, 4


def days_needed(T, x):
    """原计划T天(每天完成1/T)，前x天原效率，之后效率×1.25，返回实际用时（可为分数）"""
    e = F(1, T)
    done = e * x
    if done >= 1:
        return F(T)
    return x + (1 - done) / (e * UP)


Ts = [T for T in range(1, 500) if T - days_needed(T, 0) == EARLY_ALL]
assert len(Ts) == 1, Ts
T = Ts[0]
xs = [x for x in range(0, T + 1) if T - days_needed(T, x) == EARLY_PART]
assert len(xs) == 1, xs
x = xs[0]
hits = [k for k, v in OPTIONS.items() if v == x]
assert len(hits) == 1
# 干扰项：比例用反(原有设备占4/6)→20；把"效率提高25%"当"时间缩短25%"→原计划24天、原有设备8天；实际26天减去新设备部分原计划的20天→6
assert T * F(EARLY_PART, EARLY_ALL) == OPTIONS['D']
T_wrong = F(EARLY_ALL) / F(1, 4)
assert T_wrong - F(EARLY_PART) / F(1, 4) == OPTIONS['B']
assert (T - EARLY_PART) - (T - x) == OPTIONS['A']
print('原计划', T, '天，原有设备', x, '天')
print(hits[0])
