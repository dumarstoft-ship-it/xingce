# D01-math-1-v07  工程款三期：首期付合同总额的1/3少20万元；第二期付首期后余款的3/5多6万元；
# 第二期付款额恰好是合同总额的一半；其余为尾款。求合同总额（万元）。
from fractions import Fraction as F

OPTS = {'A': 90, 'B': 120, 'C': 180, 'D': 260}
FIRST_FRAC, FIRST_LESS = F(1, 3), 20
SECOND_FRAC, SECOND_MORE = F(3, 5), 6
SECOND_SHARE = F(1, 2)

def pays(T):
    first = T * FIRST_FRAC - FIRST_LESS
    rest = T - first                                  # 首期付款后的余款
    second = rest * SECOND_FRAC + SECOND_MORE
    return first, second, T - first - second

# 以0.1万元为步长穷举合同总额：三期付款都为正，且第二期恰好是总额的一半
sols = []
for t10 in range(1, 100001):
    T = F(t10, 10)
    first, second, tail = pays(T)
    if first > 0 and second > 0 and tail > 0 and second == T * SECOND_SHARE:
        sols.append(T)
assert len(sols) == 1, sols
T = sols[0]
hits = [k for k, v in OPTS.items() if v == T]
assert len(hits) == 1, hits

# 干扰项来源核对（各错误路径都是一次方程，逐一按错误的式子穷举求解）
def solve_wrong(second_fn):
    return [F(t10, 10) for t10 in range(1, 100001)
            if second_fn(F(t10, 10)) == F(t10, 10) * SECOND_SHARE]
# 余款里的20万元忘了乘3/5：第二期写成总额的2/5多(20＋6)
assert solve_wrong(lambda t: t * (1 - FIRST_FRAC) * SECOND_FRAC + FIRST_LESS + SECOND_MORE) == [OPTS['D']]
# 漏加6万元
assert solve_wrong(lambda t: (t - (t * FIRST_FRAC - FIRST_LESS)) * SECOND_FRAC) == [OPTS['B']]
# 设第二期为x、总额为2x，解出x后忘了乘2（答成第二期付款额）
assert pays(T)[1] == OPTS['A'] and T * SECOND_SHARE == OPTS['A']
print('payments', [str(v) for v in pays(T)], 'total', T)
print(hits[0])
