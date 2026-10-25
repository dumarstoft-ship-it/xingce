# D02-math-2-v05：两组原计划合作15天完成；合作3天后乙组被抽调（期间甲组单独），乙组返回后又合作9天完工，
# 总用时比原计划多5天。求甲组单独完成天数。解法：枚举甲单独天数T，按时间轴逐日模拟验证。
from fractions import Fraction as F

OPTIONS = {'A': 20, 'B': 25, 'C': 40, 'D': 55}
N, a, J, extra = 15, 3, 9, 5
total = N + extra
absent = total - a - J                 # 乙组缺席天数，由时间轴得出


def works(T):
    jia = F(1, T)
    yi = F(1, N) - jia
    if yi <= 0:
        return False
    done = F(0)
    for day in range(1, total + 1):
        if day <= a or day > a + absent:
            done += jia + yi
        else:
            done += jia
    return done == 1


sols = [T for T in range(N + 1, 1000) if works(T)]
assert len(sols) == 1, sols
T = sols[0]
hits = [k for k, v in OPTIONS.items() if v == T]
assert len(hits) == 1
# 干扰项：把多用的5天当缺席天数→25；合作只算后9天→20；缺席天数漏减前3天(20-9=11)→55
left = 1 - F(a + J, N)
assert extra / left == OPTIONS['B']
assert absent / (1 - F(J, N)) == OPTIONS['A']
assert (total - J) / left == OPTIONS['D']
print('乙组缺席', absent, '天，甲组单独需', T, '天')
print(hits[0])
