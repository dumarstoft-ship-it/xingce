# D01-math-h-v14 甲、乙、丙研学套票单价60、40、80元，共售300张、收入18400元，甲、乙销售额相同，求丙的张数。
# 独立求解：枚举全部非负整数张数组合，用三个条件筛选，确认唯一；再复核打包法与干扰项的错误路径。
from fractions import Fraction as Fr

OPTS = {'A': 25, 'B': 70, 'C': 100, 'D': 125}
PRICE = {'甲': 60, '乙': 40, '丙': 80}
N, R = 300, 18400

sols = []
for a in range(N + 1):
    for b in range(N + 1 - a):
        c = N - a - b
        if PRICE['甲'] * a != PRICE['乙'] * b:          # 甲、乙销售额相同
            continue
        if PRICE['甲'] * a + PRICE['乙'] * b + PRICE['丙'] * c == R:
            sols.append((a, b, c))
assert len(sols) == 1, sols
a, b, c = sols[0]
assert a > 0 and b > 0 and c > 0
ans = c

# 打包法复核：甲∶乙＝40∶60＝2∶3，5张一包
pack_ab = 2 * PRICE['甲'] + 3 * PRICE['乙']             # 240 元
pack_c = 5 * PRICE['丙']                                 # 400 元
packs = N // 5
c_packs = Fr(R - packs * pack_ab, pack_c - pack_ab)
assert c_packs.denominator == 1 and 5 * c_packs == ans

# 干扰项的错误路径
# ① 按单价正比取甲∶乙＝3∶2（最典型）
wrong = [(3 * s, 2 * s, N - 5 * s) for s in range(N // 5 + 1)
         if 3 * s * PRICE['甲'] + 2 * s * PRICE['乙'] + (N - 5 * s) * PRICE['丙'] == R]
assert len(wrong) == 1 and wrong[0][2] == OPTS['C']
# ② 求出丙的包数后忘了乘5
assert c_packs == OPTS['A']
# ③ 答成甲票的张数
assert a == OPTS['B']

hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print('甲,乙,丙 =', sols[0])
print(hits[0])
