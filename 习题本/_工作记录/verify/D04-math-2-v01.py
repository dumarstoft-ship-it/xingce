# D04-math-2-v01 团购价下限：从题面数据独立求解
from fractions import Fraction as F
cost, price, N = 30, 50, 600
unit = price - cost
retail_new = N * (1 - F(1, 3))          # 零售量减少1/3
group = 2 * retail_new                   # 团购量为新零售量的2倍
orig = unit * N
def profit(g):
    return unit * retail_new + (g - cost) * group
g_min = cost + (orig - unit * retail_new) / group
assert profit(g_min) >= orig and profit(g_min - F(1, 100)) < orig
options = {'A': 35, 'B': 40, 'C': 45, 'D': 50}
# 干扰项路径核对（仅打印）
err = {
    '团购量误为减少量的2倍': cost + (orig - unit * retail_new) / (2 * (N - retail_new)),
    '原利润全压团购': cost + F(orig) / group,
    '减少1/3误读为减少到1/3': cost + (orig - unit * N * F(1, 3)) / (2 * N * F(1, 3)),
}
print('g_min =', g_min, {k: float(v) for k, v in err.items()})
hits = [k for k, v in options.items() if v == g_min]
assert len(hits) == 1, hits
# 其余选项都不是“至少”的值
print(hits[0])
