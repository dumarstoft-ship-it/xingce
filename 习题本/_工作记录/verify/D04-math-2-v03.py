# D04-math-2-v03 总利润率不低于30%，求剩余部分最低折扣
from fractions import Fraction as F
c, p, a, r = 6, 10, F(6, 10), F(3, 10)
def rate(d):  # 总利润率（按每斤总量为1计）
    rev = a * p + (1 - a) * p * d
    return (rev - c) / c
# 二分/精确：rate(d) 关于 d 单调增，求最小 d 使 rate>=r
d_min = ((1 + r) * c - a * p) / ((1 - a) * p)
assert rate(d_min) == r and rate(d_min - F(1, 1000)) < r
options = {'A': F(45, 100), 'B': F(6, 10), 'C': F(75, 100), 'D': F(78, 100)}
feas = {k: rate(v) >= r for k, v in options.items()}
err = {'只看剩余部分': (1 + r) * c / p, '剩余保本': F(c, p), '基数用定价': (c + r * p - a * p) / ((1 - a) * p)}
print('d_min =', d_min, feas, {k: float(v) for k, v in err.items()})
hits = [k for k, v in options.items() if v == d_min]
assert len(hits) == 1, hits
# “最低”= 可行选项中的最小者，且等于 d_min
assert min((v for k, v in options.items() if feas[k])) == d_min
print(hits[0])
