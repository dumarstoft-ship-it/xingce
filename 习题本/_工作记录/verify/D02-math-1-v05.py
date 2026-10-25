# D02-math-1-v05  甲乙10天、乙丙12天、甲丙15天；三组合作4天后甲撤出，乙丙还需几天
from fractions import Fraction as F
OPTS = {'A': 4, 'B': 5, 'C': 6, 'D': 8}
ab, bc, ac = F(1, 10), F(1, 12), F(1, 15)
# 逐个解出三组效率，再按时间顺序模拟
s = (ab + bc + ac) / 2
a, b, c = s - bc, s - ac, s - ab
assert min(a, b, c) > 0 and a + b == ab and b + c == bc and a + c == ac
left = 1 - 4 * (a + b + c)
t = left / (b + c)
hits = [k for k, v in OPTS.items() if v == t]
assert len(hits) == 1, (t, hits)

# 干扰项来源核对
assert left / (a + b + c) == OPTS['A']                 # 余量误除以三组效率和
assert left / ab == OPTS['B']                          # 误除以甲乙效率和
avg = (ab + bc + ac) / 3                               # 三组效率和误取平均数
assert (1 - 4 * avg) / bc == OPTS['D']
print('a b c', a, b, c, 't', t)
print(hits[0])
