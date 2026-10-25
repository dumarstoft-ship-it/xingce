# D02-math-2-v11：中转仓库只进货6天装满空仓，只出货9天运空满仓；"进货1天、出货1天"交替，从空仓先进货。
# 求第几天第一次装满。解法：逐天模拟库存（精确分数），进货日若当天达到满仓即停止。
from fractions import Fraction as F

OPTIONS = {'A': 30, 'B': 31, 'C': 35, 'D': 36}
FULL = F(1)
r_in, r_out = FULL / 6, FULL / 9

stock, day = F(0), 0
while True:
    day += 1
    if day % 2 == 1:                     # 进货日
        if stock + r_in >= FULL:
            break
        stock += r_in
    else:                                # 出货日
        assert stock - r_out >= 0
        stock -= r_out
hits = [k for k, v in OPTIONS.items() if v == day]
assert len(hits) == 1, (day, hits)
# 干扰项：按每2天净增量直接除→36；36-1=35；停在"差一次进货"的那天→30
net2 = r_in - r_out
assert FULL / net2 * 2 == OPTIONS['D'] and OPTIONS['D'] - 1 == OPTIONS['C'] and day - 1 == OPTIONS['A']
print('第一次装满在第', day, '天')
print(hits[0])
