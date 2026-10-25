# D06-math-h-v04：回访电话每次接通的概率 0.6，各次独立；累计接通 2 位即完成本轮回访。
# 求恰好拨打 4 次完成的概率。
# 按过程逐次模拟（精确分布）：状态 = 已接通人数，接通满 2 人即停止，记录停止时已拨打的次数。
from fractions import Fraction as F
from itertools import product

OPTIONS = {'A': '17.28%', 'B': '28.80%', 'C': '34.56%', 'D': '82.08%'}
P, NEED, TARGET = F(6, 10), 2, 4


def matches(p, s):
    txt = s.rstrip('%')
    d = len(txt.split('.')[1]) if '.' in txt else 0
    return abs(p * 100 - F(txt)) < F(1, 2 * 10 ** d)


stop_at = {}                      # 拨打次数 -> 恰在这一次完成的概率
alive = {0: F(1)}                 # 尚未完成时：已接通人数 -> 概率
for call in range(1, 60):
    nxt = {}
    for got, pr in alive.items():
        for ok, w in ((1, P), (0, 1 - P)):
            g = got + ok
            if g == NEED:
                stop_at[call] = stop_at.get(call, F(0)) + pr * w
            else:
                nxt[g] = nxt.get(g, F(0)) + pr * w
    alive = nxt
assert 1 - sum(stop_at.values()) < F(1, 10 ** 9)
ans = stop_at[TARGET]

# 交叉核对：枚举前 4 次的全部结果，找出"第 4 次恰好是第 2 次接通"的序列
brute = F(0)
for seq in product((0, 1), repeat=TARGET):
    first_done = next((i + 1 for i in range(TARGET) if sum(seq[:i + 1]) == NEED), None)
    if first_done == TARGET:
        w = F(1)
        for ok in seq:
            w *= P if ok else 1 - P
        brute += w
assert brute == ans

hits = [k for k, v in OPTIONS.items() if matches(ans, v)]
assert len(hits) == 1, (ans, hits)

# 自检：干扰项对应的错误路径
q = 1 - P
assert matches(6 * P ** 2 * q ** 2, OPTIONS['C'])               # 套"4 次中恰 2 次"C(4,2)
assert matches(3 * P * q ** 2, OPTIONS['B'])                    # 只算前 3 次恰中 1 次，漏乘第 4 次
assert matches(sum(stop_at.get(k, F(0)) for k in range(1, TARGET + 1)), OPTIONS['D'])   # 4 次以内完成
print('P(恰第4次完成) =', ans, float(ans))
print(hits[0])
