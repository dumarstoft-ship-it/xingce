# T095 2024国考副省级64：去年收入1200万、支出960万；今年上/下半年支出分别减20%、15%，收入不变，盈余增172万
from fractions import Fraction as F

INCOME, EXPENSE, D1, D2, GAIN = 1200, 960, F(20, 100), F(15, 100), 172
OPTS = {'A': -160, 'B': 160, 'C': -108, 'D': 108}   # 上半年-下半年（万元）

sols = []
for h1 in range(0, EXPENSE + 1):        # 去年上半年支出（万元，整数枚举）
    h2 = EXPENSE - h1
    new_exp = h1 * (1 - D1) + h2 * (1 - D2)
    if (INCOME - new_exp) - (INCOME - EXPENSE) == GAIN:
        sols.append((h1, h2, h1 * (1 - D1), h2 * (1 - D2)))
assert len(sols) == 1, sols
h1, h2, n1, n2 = sols[0]
diff = n1 - n2
hits = [k for k, v in OPTS.items() if v == diff]
assert len(hits) == 1, (diff, hits)
assert h1 - h2 == OPTS['B']            # 干扰项：算成去年的差额
print('last year', h1, h2, 'this year', n1, n2)
print(hits[0])
