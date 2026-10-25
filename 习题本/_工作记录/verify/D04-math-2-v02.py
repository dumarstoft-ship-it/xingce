# D04-math-2-v02 分批销售：已知折扣与总利润比例，求按定价售出占比（逐个枚举售出盆数）
from fractions import Fraction as F
total_cost, n = 3600, 150
c = F(total_cost, n)
p = c * (1 + F(1, 2))        # 按50%利润率定价
disc = p * F(8, 10)          # 打八折
full = (p - c) * n
sols = [k for k in range(n + 1) if (p - c) * k + (disc - c) * (n - k) == full * F(88, 100)]
assert len(sols) == 1, sols
share = F(sols[0], n) * 100
loss = full * F(12, 100)
err = {
    '利润打八折': 100 - loss / ((p - c) * F(2, 10)) / n * 100,
    '12个百分点': 100 - (total_cost * F(12, 100)) / (p * F(2, 10)) / n * 100,
    '少赚额按成本算': 100 - loss / (c * F(2, 10)) / n * 100,
}
print('k =', sols[0], 'share =', share, {k: float(v) for k, v in err.items()})
options = {'A': 40, 'B': 60, 'C': 70, 'D': 80}
hits = [k for k, v in options.items() if v == share]
assert len(hits) == 1, hits
print(hits[0])
