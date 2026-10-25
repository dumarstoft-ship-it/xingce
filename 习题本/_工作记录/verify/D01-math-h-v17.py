# D01-math-h-v17 甲、乙从单位上车，行驶18公里后丙上车，三人同乘一段后甲下车，乙、丙再乘12公里到终点。
# 全程车费150元、与里程成正比；每段车费由该段在车上的人平分，结算后丙比甲少付9元，求三人同乘的里程。
# 独立求解：对同乘里程 m 按0.5公里步长逐个尝试（0.5～1000公里），由全程车费定出每公里价格，
# 按三段的在车人员分摊，筛出"丙比甲少付9元"的 m，确认唯一；再按每公里逐段模拟复核，并复核干扰项。
from fractions import Fraction as Fr

OPTS = {'A': 20, 'B': 32, 'C': 50, 'D': 70}
LEG1, LEG3 = 18, 12          # 甲乙同乘、乙丙同乘的里程
FARE, DIFF = 150, 9          # 全程车费；丙比甲少付的钱


def pays(m):
    """同乘 m 公里时三人各付多少（每段车费由该段在车上的人平分）。"""
    total_km = LEG1 + m + LEG3
    per_km = Fr(FARE) / total_km
    segs = [(LEG1, ('甲', '乙')), (m, ('甲', '乙', '丙')), (LEG3, ('乙', '丙'))]
    pay = {'甲': Fr(0), '乙': Fr(0), '丙': Fr(0)}
    for km, riders in segs:
        for who in riders:
            pay[who] += km * per_km / len(riders)
    return pay


sols = []
for m2 in range(1, 2001):
    m = Fr(m2, 2)
    p = pays(m)
    assert sum(p.values()) == FARE
    if p['甲'] - p['丙'] == DIFF:
        sols.append(m)
assert len(sols) == 1, sols
m = sols[0]
assert m.denominator == 1
ans = int(m)

# 逐公里模拟复核（m 为整数时）
marks = (0, LEG1, LEG1 + ans, LEG1 + ans + LEG3)
ride = {'甲': (marks[0], marks[2]), '乙': (marks[0], marks[3]), '丙': (marks[1], marks[3])}
per_km = Fr(FARE, marks[3])
pay = {k: Fr(0) for k in ride}
for km in range(marks[3]):
    riders = [k for k, (s, e) in ride.items() if s <= km < e]
    for k in riders:
        pay[k] += per_km / len(riders)
assert pay['甲'] - pay['丙'] == DIFF and per_km == 3

# 干扰项的错误路径
wrong_rate = Fr(DIFF, LEG1 - LEG3)                    # 忘了前后两段都是两人平摊：6x＝9
assert FARE / wrong_rate - LEG1 - LEG3 == OPTS['D']
assert FARE / per_km == OPTS['C']                      # 求出全程50公里就停
assert ans + LEG3 == OPTS['B']                         # 把丙的乘车里程当成同乘里程

hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print('shared km =', ans, 'per km =', per_km, {k: str(v) for k, v in pay.items()})
print(hits[0])
