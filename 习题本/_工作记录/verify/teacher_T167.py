# teacher T167（2014联考）甲96h、乙90h、丙80h，按甲乙、甲丙、乙丙轮班每天8小时，完工时甲工作了几小时
from fractions import Fraction as F

OPTS = {'A': 16, 'B': 24, 'C': 44, 'D': 32}
rate = {'甲': F(1, 96), '乙': F(1, 90), '丙': F(1, 80)}
order = [('甲', '乙'), ('甲', '丙'), ('乙', '丙')]
HOURS = 8
left, day = F(1), 0
worked = {k: F(0) for k in rate}
while left > 0:
    pair = order[day % 3]
    day += 1
    r = sum(rate[p] for p in pair)
    t = min(F(HOURS), left / r)
    for p in pair:
        worked[p] += t
    left -= r * t
print('第', day, '天完工，', {k: str(v) for k, v in worked.items()})
hits = [k for k, v in OPTS.items() if v == worked['甲']]
assert len(hits) == 1, hits
print(hits[0])
