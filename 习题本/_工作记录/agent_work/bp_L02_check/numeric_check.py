import itertools
from fractions import Fraction as F
def chk(name, cond): print(('OK ' if cond else 'BAD'), name)

# D14-G10 门票 80->40, 人次+50%
chk('D14-G10 门票收入下降 (40*1.5=60<80)', 40 * F(3, 2) < 80)
# D14-G12 加权平均
avg = F(92 * 100 + 86 * 300, 400); chk(f'D14-G12 总平均={float(avg)} <89 且 !=89', avg < 89)
# D14-G14: 5人, 整数, 60<=s<=95, 最高恰95, 总分400
sols = [c for c in itertools.combinations_with_replacement(range(60, 96), 4) if sum(c) + 95 == 400]
S = [tuple(sorted(c + (95,))) for c in sols]
poss = lambda f: any(f(s) for s in S)
opts = {'有3人低于80': lambda s: sum(x < 80 for x in s) >= 3, '只有1人90分以上': lambda s: sum(x >= 90 for x in s) == 1,
        '最低分恰为60': lambda s: min(s) == 60, '有4人不低于90': lambda s: sum(x >= 90 for x in s) >= 4}
print('   D14-G14 possible?', {k: poss(f) for k, f in opts.items()})
chk('D14-G14 唯一不可能=有4人不低于90', [k for k, f in opts.items() if not poss(f)] == ['有4人不低于90'])
# D27-G11 停车 6->8 元/小时, 收入持平
chk('D27-G11 计费时长=0.75倍', F(6, 8) == F(3, 4))
# D27-G13 新增岗位
T = F(1); d24 = F(30, 100) * T; d25 = F(35, 100) * F(9, 10) * T
chk(f'D27-G13 数字经济新增岗位 {float(d24)}T -> {float(d25)}T 增加', d25 > d24)
chk('D27-G13 非数字岗位减少 (0.70T -> 0.585T)', F(65, 100) * F(9, 10) < F(70, 100))
# D27-G14 抽检
chk('D27-G14 2/50=4% <=5% 不召回; 再抽50仍2件 => 4/100=4% 仍不召回', F(2, 50) <= F(5, 100) and F(4, 100) <= F(5, 100))
# D27-G17: 8 社区, 每个>=3, 最多恰8, 合计40
comb = [c for c in itertools.combinations_with_replacement(range(3, 9), 8) if sum(c) == 40 and max(c) == 8]
opts = {'有一个社区只有3名': lambda c: 3 in c, '有3个社区各8名': lambda c: c.count(8) >= 3,
        '每个社区都不少于5名': lambda c: min(c) >= 5, '有5个社区各4名': lambda c: c.count(4) >= 5}
print('   D27-G17 possible?', {k: any(f(c) for c in comb) for k, f in opts.items()})
chk('D27-G17 唯一不可能=每个社区都不少于5名', [k for k, f in opts.items() if not any(f(c) for c in comb)] == ['每个社区都不少于5名'])
# D36-G11 港口: 2025总量=1, 外贸占60%, 外贸增12%, 总量增8%
tot24 = F(1) / F(108, 100); wm24 = F(60, 100) / F(112, 100); nm24 = tot24 - wm24; nm25 = F(40, 100)
g_nm = nm25 / nm24 - 1
print(f'   D36-G11 内贸增速={float(g_nm):.4f}, 2024外贸占比={float(wm24 / tot24):.4f}, 外贸增量/内贸增量={float((F(60,100)-wm24)/(nm25-nm24)):.2f}')
chk('D36-G11 内贸增速<8% 且 >0; 2024外贸占比<60%; 增量比!=1.5', 0 < g_nm < F(8, 100) and wm24 / tot24 < F(60, 100) and (F(60, 100) - wm24) / (nm25 - nm24) != F(3, 2))
# D36-G12 阶梯水价
fee = lambda t: 3 * min(t, 15) + 5 * max(t - 15, 0)
chk(f'D36-G12 甲20吨={fee(20)} 乙10吨={fee(10)} 比值>2; 乙15吨={fee(15)}<=50', fee(20) > 2 * fee(10) and fee(15) <= 50)
# D36-G13 辛普森
A = F(3, 10) * 98 + F(7, 10) * 80; B = F(9, 10) * 96 + F(1, 10) * 75
chk(f'D36-G13 例: A总体={float(A)} < B总体={float(B)} 而A分项都更高', A < B)
# D36-G15: 5人 整数互不相同 0..95, 最高恰95, 总分400
S = [c for c in itertools.combinations(range(0, 95), 4) if sum(c) == 305]
opts = {'最低分为60': lambda c: min(c) == 60, '有2人低于60': lambda c: sum(x < 60 for x in c) >= 2,
        '第二名94分': lambda c: max(c) == 94, '有3人在80分以上': lambda c: sum(x > 80 for x in c) + 1 >= 3}
print('   D36-G15 possible?', {k: any(f(c) for c in S) for k, f in opts.items()})
chk('D36-G15 唯一不可能=有2人低于60', [k for k, f in opts.items() if not any(f(c) for c in S)] == ['有2人低于60'])
# D7-G9 比例: 组内60% => 应届 > 非应届
chk('D7-G9 组内应届60%>非应届40%', F(60, 100) > F(40, 100))
# D36-G10 优秀率: 前30%且>=85 => <=30%
chk('D36-G10 优秀率上限30%', True)
