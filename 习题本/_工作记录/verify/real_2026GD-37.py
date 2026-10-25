# real 2026GD-37  周六签约客户数是周日的1.5倍，签约总金额是周日的80%；两天共40家客户、720万元（无重复客户）。
# 求周日平均每家客户的签约金额。
from fractions import Fraction as F
OPTS = {'A': 15, 'B': 20, 'C': 25, 'D': 10}
CUST, AMT = 40, 720
sols = []
for sun in range(1, CUST):                      # 周日客户数
    sat = CUST - sun
    if sat != F(3, 2) * sun:
        continue
    for a10 in range(1, AMT * 10):              # 周日金额（0.1万元步长）
        a = F(a10, 10)
        if AMT - a == F(4, 5) * a:
            sols.append((sun, sat, a))
assert len(sols) == 1, sols
sun, sat, a = sols[0]
avg = a / sun
hits = [k for k, v in OPTS.items() if v == avg]
assert len(hits) == 1, hits
# 干扰项：金额比用反成5:4（周日320万元）
assert F(AMT * 4, 9) / sun == OPTS['B']
print('sunday customers', sun, 'amount', a, 'avg', avg)
print(hits[0])
