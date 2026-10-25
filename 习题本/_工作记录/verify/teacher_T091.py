# T091 2019四川选调：定价降10%，单台利润升10%，总利润增21%，问销量变化
from fractions import Fraction as F

UNIT_PROFIT_CHG, TOTAL_PROFIT_CHG = F(10, 100), F(21, 100)
# 定价降10%与总利润无关（干扰信息），不参与计算

def classify(chg):
    if chg >= 0:
        return 'A' if chg < F(20, 100) else 'B'
    return 'C' if -chg < F(20, 100) else 'D'

qty_ratio = (1 + TOTAL_PROFIT_CHG) / (1 + UNIT_PROFIT_CHG)   # 总利润=单利×销量
chg = qty_ratio - 1
# 枚举验证：任取原单利、原销量，新销量由总利润反推
for u in range(1, 50):
    for q in range(1, 50):
        q2 = F(u * q) * (1 + TOTAL_PROFIT_CHG) / (F(u) * (1 + UNIT_PROFIT_CHG))
        assert q2 / q - 1 == chg
assert classify((1 + TOTAL_PROFIT_CHG) / F(9, 10) - 1) == 'B'   # 干扰：误用定价降幅
print('sales change =', chg)
print(classify(chg))
