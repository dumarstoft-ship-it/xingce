# D01-math-h-v18 租金由参加者平均分摊：多2人则每人少摊30元，少2人则每人多摊50元，求租金。
# 独立求解：对原定人数 n 逐个尝试，由"多2人每人少30元"这一条件解出租金 T，再检验"少2人每人多50元"；
# 确认只有一组 (n, T)；再对每个选项反查，复核"只验一个条件"的错误路径。
from fractions import Fraction as Fr

OPTS = {'A': 600, 'B': 720, 'C': 1200, 'D': 1800}
MORE, LESS_EACH = 2, 30      # 多2人，每人少摊30元
FEWER, MORE_EACH = 2, 50     # 少2人，每人多摊50元


def cond_more(T, n):
    return T / n - T / (n + MORE) == LESS_EACH


def cond_fewer(T, n):
    return n > FEWER and T / (n - FEWER) - T / n == MORE_EACH


sols = []
for n in range(FEWER + 1, 1000):
    # 条件一对 T 是一次的：T·(1/n − 1/(n+2)) = 30
    k = Fr(1, n) - Fr(1, n + MORE)
    T = LESS_EACH / k
    if cond_fewer(T, n):
        sols.append((n, T))
assert len(sols) == 1, sols
n, T = sols[0]
assert T.denominator == 1 and (T / n).denominator == 1
ans = T

# 逐个选项反查：对每个选项，找出满足各条件的人数
for key, t in OPTS.items():
    t = Fr(t)
    n1 = [m for m in range(3, 500) if cond_more(t, m)]
    n2 = [m for m in range(3, 500) if cond_fewer(t, m)]
    both = set(n1) & set(n2)
    if t == ans:
        assert both == {n}
    else:
        assert not both
# 干扰项：只验一个条件
assert [m for m in range(3, 500) if cond_more(Fr(OPTS['B']), m)] == [6]       # 720：只满足多2人（6人）
assert [m for m in range(3, 500) if cond_more(Fr(OPTS['D']), m)] == [10]      # 1800：只满足多2人（10人）
assert [m for m in range(3, 500) if cond_fewer(Fr(OPTS['A']), m)] == [6]      # 600：只满足少2人（6人）

hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print('n =', n, 'per person =', T / n, 'rent =', T)
print(hits[0])
