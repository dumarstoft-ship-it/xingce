# Proposed replacement data for D06-math-2-v07 (independent of 2-v05's data)
# 甲乙丙三家供应商 采购量 4:3:3，不合格率 1%、2%、4%；抽到不合格品，来自丙的概率
from fractions import Fraction as F
ratio = [4, 3, 3]
rate = [F(1, 100), F(2, 100), F(4, 100)]
tot = sum(ratio)
joint = [F(r, tot) * d for r, d in zip(ratio, rate)]
P = joint[2] / sum(joint)
traps = {'只看采购占比': F(3, 10), '乙供应商': joint[1] / sum(joint), '只看不合格率占比': F(4, 1 + 2 + 4)}
opts = {'A': F(3, 10), 'B': F(3, 11), 'C': F(6, 11), 'D': F(4, 7)}
hit = [k for k, v in opts.items() if v == P]
assert len(hit) == 1
print('P =', P, float(P), 'traps', {k: (str(v), round(float(v), 4)) for k, v in traps.items()})
print(hit[0])
