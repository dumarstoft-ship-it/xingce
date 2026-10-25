# D02-math-1-v07  老周12天+小吴10天=完工；合干8天后小吴再干12天=完工；求老周单独天数
from fractions import Fraction as F
OPTS = {'A': 16, 'B': 24, 'C': 32, 'D': 40}
R = range(1, 60)

# 穷举两人日效率（正整数），找出两种方案工作量相等的情形，总量取方案一
sols = {F(12 * z + 10 * l, z) for z in R for l in R
        if 12 * z + 10 * l == 8 * (z + l) + 12 * l}
assert len(sols) == 1, sols
T = sols.pop()
hits = [k for k, v in OPTS.items() if v == T]
assert len(hits) == 1, hits


def alone(eq, who='z'):
    s = {F(12 * z + 10 * l, z if who == 'z' else l) for z in R for l in R if eq(z, l)}
    assert len(s) == 1, s
    return s.pop()


# 干扰项来源核对
assert alone(lambda z, l: 12 * z + 10 * l == 8 * l + 12 * l) == OPTS['B']   # 漏掉合干中老周的量
assert alone(lambda z, l: 12 * z + 10 * l == 8 * z + 12 * l) == OPTS['C']   # 漏掉合干中小吴的量
assert alone(lambda z, l: 12 * z + 10 * l == 8 * (z + l) + 12 * l, 'l') == OPTS['D']  # 小吴单独
print('Zhou alone', T)
print(hits[0])
