# D04-math-1-v01  同价一盈一亏，已知合计亏损反求售价
# 题面：两件以相同价格卖出，按各自买入价一件盈利20%、一件亏损20%，合计亏损30元，求每件卖出价。
from fractions import Fraction as F

UP, DOWN, LOSS = F(20, 100), F(20, 100), F(30)
OPTS = {'A': F(360), 'B': F(375), 'C': F(450), 'D': F(750)}


def total_loss(P):
    """以卖出价 P 计算两件合计亏损额（总成本-总收入）。"""
    cost = P / (1 + UP) + P / (1 - DOWN)
    return cost - 2 * P


# 1) 在0.01元精度上穷举卖出价（0~2000元，已覆盖全部选项）
sols = [F(c, 100) for c in range(1, 200001) if total_loss(F(c, 100)) == LOSS]
assert len(sols) == 1
P = sols[0]
# 2) 逐项检验选项
hits = [L for L, v in OPTS.items() if total_loss(v) == LOSS]
assert len(hits) == 1 and OPTS[hits[0]] == P, (hits, P)

# 结论核对：总亏损恰为总成本的 r^2
cost_total = P / (1 + UP) + P / (1 - DOWN)
assert total_loss(P) == cost_total * UP * UP

# 干扰项来源核对
assert LOSS / (2 * UP * UP) == OPTS['B']          # 误用 2P*r^2=30
assert P / (1 - DOWN) == OPTS['C']                # 亏损那件的买入价
assert cost_total == OPTS['D']                    # 总成本（亦即 P*r^2=30 的错解）
assert LOSS / (UP * UP) == OPTS['D']

print('P =', P, 'costs =', P / (1 + UP), P / (1 - DOWN))
print(hits[0])
