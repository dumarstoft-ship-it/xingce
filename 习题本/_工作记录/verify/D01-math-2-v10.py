# D01-math-2-v10 四人AA结算：甲应从其他三人处一共收回多少
from fractions import Fraction as Fr

opts = {'A': 440, 'B': 645, 'C': 810, 'D': 945}
paid = {'甲': 1260, '乙': 780, '丙': 420, '丁': 0}

total = sum(paid.values())
share = Fr(total, len(paid))
net = {k: v - share for k, v in paid.items()}       # 正数=应收回，负数=应补交
assert sum(net.values()) == 0

# 模拟一次结算：欠钱的人依次把钱付给多付的人，统计甲实际收到的钱
creditors = [[k, v] for k, v in net.items() if v > 0]
debtors = [[k, -v] for k, v in net.items() if v < 0]
received = {k: Fr(0) for k in paid}
i = j = 0
while i < len(debtors) and j < len(creditors):
    amt = min(debtors[i][1], creditors[j][1])
    received[creditors[j][0]] += amt
    debtors[i][1] -= amt
    creditors[j][1] -= amt
    if debtors[i][1] == 0:
        i += 1
    if creditors[j][1] == 0:
        j += 1
ans = received['甲']
assert ans == net['甲']

# 干扰项的错误路径
assert paid['甲'] - Fr(total, 3) == opts['A']                 # 漏了丁，按三人平均
assert -(net['丙'] + net['丁']) == opts['C']                  # 以为丙丁补交的全归甲
assert paid['甲'] * Fr(3, 4) == opts['D']                     # 只分摊甲垫付的钱

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('share =', share, 'net =', {k: str(v) for k, v in net.items()})
print(hits[0])
