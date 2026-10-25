# D03-math-1-v01: 1500米观光车道，快车到终点后原速折返，在距终点300米处与慢车相遇；问快车到终点时慢车距终点多远
from fractions import Fraction as F

L, MEET_LEFT = 1500, 300
OPTS = {'A': 300, 'B': 500, 'C': 600, 'D': 750}

def pos_fast(t, f):            # 快者位置：先到终点，再原速返回
    return f * t if f * t <= L else 2 * L - f * t

def meet_left(f, s=F(1)):      # 逐步求相遇时刻：慢者位置 = 快者位置（折返之后）
    t = F(L) / f               # 快者到终点时刻
    # 折返后两人相向：慢者在 s*t，快者在 2L - f*t，相等时 t = 2L/(s+f)
    tm = F(2 * L) / (s + f)
    assert tm >= t
    assert s * tm == pos_fast(tm, f)
    return L - s * tm

answers = set()
# 速度比 f:s 在 1.01~5 之间以 0.01 为步长穷举（慢者速度取 1）
for k in range(101, 501):
    f = F(k, 100)
    if meet_left(f) == MEET_LEFT:
        gap = L - F(L) / f * 1     # 快者到终点时慢者已走 L/f（慢者速度1）
        answers.add(gap)
assert len(answers) == 1, answers
ans = answers.pop()
hit = [k for k, v in OPTS.items() if v == ans]
assert len(hit) == 1, (ans, hit)
# 干扰项来源
assert OPTS['A'] == MEET_LEFT                 # 把相遇时距终点的300米当成差距
assert OPTS['C'] == 2 * MEET_LEFT             # 以为在差距的中点相遇
assert OPTS['D'] == MEET_LEFT * F(5, 2)       # 3:2 用反
print('gap =', ans)
print(hit[0])
