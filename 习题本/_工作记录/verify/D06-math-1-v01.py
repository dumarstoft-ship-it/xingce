# D06-math-1-v01: 6 个粽子，咸蛋黄(X)比豆沙(D)少；取 2 个恰 1 个 X 的概率为 8/15；求取 2 个都是 D 的概率
from fractions import Fraction as F
from itertools import combinations
TOTAL, GIVEN = 6, F(8, 15)
pairs = list(combinations(range(TOTAL), 2))
cands = []
for k in range(TOTAL + 1):
    if not k < TOTAL - k:          # 题设：咸蛋黄馅比豆沙馅少
        continue
    kind = ['X'] * k + ['D'] * (TOTAL - k)
    one = sum(1 for a, b in pairs if (kind[a] == 'X') + (kind[b] == 'X') == 1)
    if F(one, len(pairs)) == GIVEN:
        cands.append(k)
assert len(cands) == 1, cands
k = cands[0]
kind = ['X'] * k + ['D'] * (TOTAL - k)
ans = F(sum(1 for a, b in pairs if kind[a] == 'D' and kind[b] == 'D'), len(pairs))
opts = {'A': F(1, 15), 'B': F(2, 5), 'C': F(7, 15), 'D': F(3, 5)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('k =', k, 'P =', ans)
print(hit[0])
