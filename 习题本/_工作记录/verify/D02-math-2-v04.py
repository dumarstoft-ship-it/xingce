# D02-math-2-v04：甲乙原计划合作20天；合作4天后甲被抽调，乙单独又干4天，恰完成1/4；
# 丙加入（丙单独需40天），若干天后甲返回，三队干到完工，最终仍比原计划推迟2天。问甲队共离开多少天。
# 解法：由1/4节点枚举求出效率比；再对"丙加入后甲又离开的天数x"逐一枚举、逐日模拟，
# 找出恰在第22天末完工的x，甲离开天数=乙单独的4天+x。
from fractions import Fraction as F

OPTIONS = {'A': 6, 'B': 8, 'C': 10, 'D': 12}
N, a, b, p, delay, T_bing = 20, 4, 4, F(1, 4), 2, 40

# 设乙效率1、甲效率k：a(k+1)+b·1 = p·N·(k+1)，在分母≤12的正有理数中枚举
cands = {F(n, m) for m in range(1, 13) for n in range(1, 61)}
ks = sorted(k for k in cands if a * (k + 1) + b == p * N * (k + 1))
assert len(ks) == 1, ks
jia, yi = ks[0], F(1)
W = N * (jia + yi)
bing = W / T_bing


def finish_day(x):
    done, day = F(0), 0
    while done < W:
        day += 1
        if day <= a:
            rate = jia + yi
        elif day <= a + b:
            rate = yi
        elif day <= a + b + x:
            rate = yi + bing
        else:
            rate = jia + yi + bing
        done += rate
        if day > 300:
            return None
    return day if done == W else None


assert (jia + yi) * a + yi * b == p * W            # 1/4 节点
sols = [x for x in range(0, 60) if finish_day(x) == N + delay]
assert len(sols) == 1, sols
x = sols[0]
absent = b + x
hits = [k for k, v in OPTIONS.items() if v == absent]
assert len(hits) == 1, (absent, hits)
# 干扰项：只算丙加入后的天数x→8；三队合作天数→6；甲实际干活天数(前4天+三队天数)→10
trio = (N + delay - a - b) - x
assert x == OPTIONS['B'] and trio == OPTIONS['A'] and a + trio == OPTIONS['C']
# 把"推迟"误看成"提前"：只得x=0（与"若干天后甲队返回"矛盾），离开天数4不在选项中，不构成歧义
rem_early = N - delay - a - b
mis = [t for t in range(0, rem_early + 1) if (yi + bing) * t + (jia + yi + bing) * (rem_early - t) == W - p * W]
assert all(t == 0 and b + t not in OPTIONS.values() for t in mis), mis
print('甲/乙 =', jia, '总量', W, '丙效率', bing, 'x =', x, '甲共离开', absent, '天')
print(hits[0])
