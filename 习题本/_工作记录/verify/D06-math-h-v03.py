# D06-math-h-v03：甲、乙各罚球 2 次，甲每次罚中 0.6，乙每次 0.5，各次独立；
# 求甲罚中次数比乙多的概率。
# 暴力枚举：4 次罚球的全部 16 种结果逐一乘出概率，累加"甲中的次数 > 乙中的次数"的结果。
from fractions import Fraction as F
from itertools import product

OPTIONS = {'A': '27%', 'B': '33%', 'C': '39%', 'D': '76%'}
P_JIA, P_YI, N = F(6, 10), F(5, 10), 2


def matches(p, s):
    txt = s.rstrip('%')
    d = len(txt.split('.')[1]) if '.' in txt else 0
    return abs(p * 100 - F(txt)) < F(1, 2 * 10 ** d)


def prob(shots, p):
    out = F(1)
    for hit in shots:
        out *= p if hit else 1 - p
    return out


gt = ge = F(0)
for jia in product((0, 1), repeat=N):
    for yi in product((0, 1), repeat=N):
        w = prob(jia, P_JIA) * prob(yi, P_YI)
        if sum(jia) > sum(yi):
            gt += w
        if sum(jia) >= sum(yi):
            ge += w
ans = gt

hits = [k for k, v in OPTIONS.items() if matches(ans, v)]
assert len(hits) == 1, (ans, hits)

# 自检：干扰项对应的错误路径
q = 1 - P_JIA
assert matches(P_JIA * q * (1 - P_YI) ** 2 + P_JIA ** 2 * (1 - P_YI ** 2), OPTIONS['B'])  # 甲中 1 次漏乘 C(2,1)
assert matches(P_JIA ** 2 * (1 - P_YI ** 2), OPTIONS['A'])                                # 只算甲中 2 次
assert matches(ge, OPTIONS['D'])                                                          # "多于"算成"不少于"
print('P(甲>乙) =', gt, float(gt), ' P(甲>=乙) =', ge)
print(hits[0])
