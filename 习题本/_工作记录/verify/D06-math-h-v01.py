# D06-math-h-v01：5 双款式各不相同的手套拆散混放（共 10 只），随机取出 4 只，
# 求"恰好有 2 只能配成一双、另外 2 只配不成双"的概率。
# 暴力枚举：10 只手套各不相同（款式 × 左右），枚举全部 C(10,4) 种取法，数其中恰含 1 个完整双的取法。
from fractions import Fraction as F
from itertools import combinations
from math import comb

OPTIONS = {'A': F(1, 7), 'B': F(4, 7), 'C': F(13, 21), 'D': F(2, 3)}

STYLES = 5
gloves = [(s, side) for s in range(STYLES) for side in ('左', '右')]


def full_pairs(pick):
    styles = [s for s, _ in pick]
    return sum(1 for s in set(styles) if styles.count(s) == 2)


picks = list(combinations(gloves, 4))
dist = {k: sum(1 for p in picks if full_pairs(p) == k) for k in range(3)}
ans = F(dist[1], len(picks))

hits = [k for k, v in OPTIONS.items() if v == ans]
assert len(hits) == 1, (ans, hits)

# 自检：干扰项对应的错误路径
assert F(STYLES * comb(2 * STYLES - 2, 2), len(picks)) == OPTIONS['D']        # 成双后从剩下 8 只任取 2 只
assert F(STYLES * comb(STYLES - 1, 2), len(picks)) == OPTIONS['A']            # 选了另 2 双却漏乘 2×2
assert F(dist[1] + dist[2], len(picks)) == OPTIONS['C']                       # 至少一双
print('total', len(picks), 'by number of pairs', dist, 'P =', ans)
print(hits[0])
