# Recompute each distractor from its claimed error path (sanity check of the jiexi claims).
import math
from fractions import Fraction as F
print('--- v08 EOQ: D=3000, K=250, h=6')
cost = lambda x: F(250*3000, x) + F(6*x, 2)
print('forgot half -> x =', math.sqrt(3000*250/6))
wrong = lambda x: F(250*3000, x) + 6*x
print('forgot-half costs 250/500:', wrong(250), wrong(500))
print('costs', {x: cost(x) for x in (250, 375, 500, 750, 1000)})
print('--- v09 parking')
print('24/3 =', 24/3, ' 24/5 =', 24/5)
print('--- v10 subway')
print('full-amount reading: n=21 -> S=105 ->', 0.8*105/21)
print('premium 60 (0.2 slip): n>=', 60/1.5, ' premium 65:', 65/1.5, ' forgot 8折 tier (75):', 75/1.5)
print('--- v11 tax')
def tax(x):
    t=0
    for lo,hi,r in [(0,3000,.03),(3000,12000,.10),(12000,25000,.20)]:
        if x>lo: t+=(min(x,hi)-lo)*r
    return t
for a in (8400, 9600, 12000, 14400):
    print(a, 'diff with +6000:', round(tax(a+6000)-tax(a),2))
print('--- v12 margin p=60 v=40 F=120000 r=20%')
print('target profit = 20% of fixed:', (120000*1.2)/20)
print('denominator only variable:', 120000/(20-0.2*40))
print('profit/revenue:', 120000/(20-0.2*60))
print('breakeven:', 120000/20)
print('--- v13 make-or-buy')
print('critical point', 90000/12, ' naive self-make', (90000+18*8000)/1e4, ' cap-aware', (90000+18*6000+30*2000)/1e4,
      ' forgot remaining', (90000+18*6000)/1e4, ' all buy', 30*8000/1e4)
