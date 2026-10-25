# D01-math-1-v04  冷库：荔枝存量是龙眼的2倍；第一周荔枝出库30%、龙眼出库一半；第二周各出库70箱后荔枝是龙眼的4倍。求原来共多少箱。
from fractions import Fraction as F

R, P_OUT, Q_OUT, M, K = 2, F(3, 10), F(1, 2), 70, 4
OPTS = {'A': 350, 'B': 450, 'C': 700, 'D': 1050}

def solve(lychee_keep):
    """lychee_keep: 第一周后荔枝保留的比例；穷举龙眼原有箱数b"""
    out = []
    for b in range(1, 50001):
        l = R * b
        l1, b1 = l * lychee_keep, b * (1 - Q_OUT)
        if F(l1).denominator != 1 or F(b1).denominator != 1:
            continue                      # 箱数须为整数
        l2, b2 = l1 - M, b1 - M
        if l2 <= 0 or b2 <= 0:
            continue
        if l2 == K * b2:
            out.append((b, l))
    return out

sols = solve(1 - P_OUT)
assert len(sols) == 1, sols
b, l = sols[0]
total = b + l
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits

# 干扰项来源核对
bad = solve(P_OUT)                        # 把“出库30%”读成“剩下30%”
assert len(bad) == 1 and sum(bad[0]) == OPTS['B']
assert b == OPTS['A'] and l == OPTS['C']  # 只答出龙眼或荔枝
print('longan', b, 'lychee', l, 'total', total)
print(hits[0])
