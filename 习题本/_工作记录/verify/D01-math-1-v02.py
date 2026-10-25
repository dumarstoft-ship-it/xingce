# D01-math-1-v02  时间银行：每服务1小时记10分，法定节假日按1.5倍记分；每月记分超过300分的部分只按一半存入账户。
# 小林5月节假日服务10小时，当月账户存入340分。求非节假日服务小时数。
from fractions import Fraction as F

PER_H, HOLI_MUL, CAP = 10, F(3, 2), 300
HOLI_H, CREDITED = 10, 340
OPTS = {'A': 19, 'B': 23, 'C': 24, 'D': 28}

def credited(raw):
    """原始记分 -> 实际存入个人账户的分数"""
    return raw if raw <= CAP else CAP + F(raw - CAP, 2)

# 穷举非节假日服务小时数（一个月最多744小时）
sols = [x for x in range(0, 745)
        if credited(PER_H * HOLI_MUL * HOLI_H + PER_H * x) == CREDITED]
assert len(sols) == 1, sols
x = sols[0]
hits = [k for k, v in OPTS.items() if v == x]
assert len(hits) == 1, hits

# 干扰项来源核对
assert (CREDITED - PER_H * HOLI_MUL * HOLI_H) / PER_H == OPTS['A']      # 忽略减半规则，直接用340分
raw = CAP + (CREDITED - CAP) * 2                                        # 正确还原的原始记分380
assert (raw - PER_H * HOLI_H) / PER_H == OPTS['D']                      # 节假日没乘1.5
assert (CREDITED - PER_H * HOLI_H) / PER_H == OPTS['C']                 # 两处都错
print('raw points', raw, 'non-holiday hours', x)
print(hits[0])
