# D06-math-h-v02：甲、乙、丙三校各自从 5 个研学基地中随机选定 2 个（三校互不影响），
# 求任意两校选定的基地都至少有一个相同的概率。
# 暴力枚举：每校 C(5,2)=10 种选法等可能，三校共 10^3=1000 种组合，数"两两都有公共基地"的组合。
from fractions import Fraction as F
from itertools import combinations, product

OPTIONS = {'A': '63%', 'B': '10%', 'C': '34.3%', 'D': '37%'}


def matches(p, s):
    """选项按其显示精度比较：34.3% 表示 [34.25%, 34.35%)。"""
    txt = s.rstrip('%')
    d = len(txt.split('.')[1]) if '.' in txt else 0
    return abs(p * 100 - F(txt)) < F(1, 2 * 10 ** d)


BASES, PICK = 5, 2
choices = [frozenset(c) for c in combinations(range(BASES), PICK)]
triples = list(product(choices, repeat=3))
good = sum(1 for a, b, c in triples if a & b and a & c and b & c)
ans = F(good, len(triples))

hits = [k for k, v in OPTIONS.items() if matches(ans, v)]
assert len(hits) == 1, (ans, hits)

# 自检：容斥各项与干扰项对应的错误路径（都由枚举得到）
p1 = F(sum(1 for a, b, c in triples if not a & b), len(triples))                         # 某一对错开 0.3
p2 = F(sum(1 for a, b, c in triples if not a & b and not a & c), len(triples))           # 共用甲的两对同时错开 0.09
p3 = F(sum(1 for a, b, c in triples if not a & b and not a & c and not b & c), len(triples))  # 三对都错开
assert p3 == 0                                                   # 需要 6 个基地，不可能
assert 1 - (3 * p1 - 3 * p2 + p3) == ans                         # 反面容斥与枚举一致
assert matches(1 - 3 * p1, OPTIONS['B'])                         # 只减不加回
assert matches((1 - p1) ** 3, OPTIONS['C'])                      # 把三对当作相互独立
assert matches(1 - ans, OPTIONS['A'])                            # 忘了取反
print('triples', len(triples), 'all pairs overlap', good, 'P =', ans, ' p1 =', p1, 'p2 =', p2, 'p3 =', p3)
print(hits[0])
