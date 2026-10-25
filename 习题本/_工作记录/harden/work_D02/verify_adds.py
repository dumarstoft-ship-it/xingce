from fractions import Fraction as F
# 2022GK-74: same efficiency, d = 甲-乙 constant. x+d=54 ; y-d=1.5x ; x-y=d
for x in range(1, 200):
    d = 54 - x; y = x - d
    if y - d == F(3,2)*x:
        print('2022GK-74 x,y,d =', x, y, d, '(d<0 => 乙 earlier)'); rate = F(y,3)
        t = (500 - x - y) / (2*rate); print('  500 at 12:00 +', float(t), 'h')
# 2021SD-42: second phase 王 doubled: (2w - z)/(2w + z) = 100/400 -> z:w
# 6w = 5z -> z:w = 6:5 ; first phase z-w = 50 -> 1 part=50 -> total 11 parts = 550 = x + 400
print('2021SD-42 small box =', 11*50 - 400)
# 2023JSA-61
def workdays(n, w, r):
    c = w + r; return (n//c)*w + min(n % c, w)
a1, b1 = workdays(23, 3, 1), workdays(21, 5, 2)
a2, b2 = workdays(15, 3, 1), workdays(27, 5, 2)
print('2023JSA-61 s1', a1, b1, 's2', a2, b2)
# a1*A + b1*B = a2*A + b2*B -> (a1-a2)A = (b2-b1)B
A, B = F(b2-b1), F(a1-a2)   # proportional
tot = a1*A + b1*B; need = tot / A
d = 0; done = 0
while done < need:
    d += 1
    if (d-1) % 4 < 3: done += 1
print('  甲 working days needed', need, '-> calendar days', d)
# 2025ZJA-59: (a+b)^2 = 4.5ab -> ratio roots
import math
r1 = (2.5 + math.sqrt(2.5**2 - 4))/2; print('2025ZJA-59 ratio roots', r1, 1/r1)
for ratio in (2, F(1,2)):   # 甲/乙 efficiency
    tot = 12*(ratio + 1) + 12*1; print('  甲/乙 =', ratio, '-> 甲 alone', tot/ratio)
# 2024JSA-54
T = F(259, F(1,6)+F(1,5)+F(1,4)); print('2024JSA-54 minutes', T, ' answer', T/5 + T/4 + T/2*F(4,5), ' trap399', T/5+T/4+T/2, ' trap469', 259 + T/2)
# 2025HB-75
for n in range(1, 10):
    if 150*(n-1) + 100*max(n-3,0) + 80*max(n-2,0) >= 1040: print('2025HB-75 n =', n); break
# 2024SC-48
for a in range(1, 100):
    if F(450, a) - F(450, a+5) == 1: print('2024SC-48 甲', a, '; after: 甲 behind', 450 - a*450//(a+5), 'catch 5/day ->', (450 - a*(450//(a+5)))//5, 'days ->', 40*((450 - a*(450//(a+5)))//5))
# 2020SC1206-46
jia, yi = F(10,12), F(15,12)
c = (75 - 30*jia - 30*yi*F(4,5)) / 30; print('2020SC1206-46 丙/甲 =', c/jia, ' trap(no 80%) =', (75 - 30*jia - 30*yi)/30/jia)
# T096
print('T096 工期', F(2) / (F(5)/F(9,2) - 1))
# T167
r = [F(1,96), F(1,90), F(1,80)]
cyc = 8*(r[0]+r[1]) + 8*(r[0]+r[2]) + 8*(r[1]+r[2]); rem = 1 - cyc
d4 = 8*(r[0]+r[1]); d5 = 8*(r[0]+r[2])
print('T167 cycle', cyc, 'rem', rem, 'after d4,d5', d4+d5, '< rem?', d4+d5 < rem, '-> 甲 hours', 16+16)
# T081 check: 6/n + 12/(n+5) = 1
for n in range(1, 40):
    if F(6,n) + F(12,n+5) == 1: print('T081 n =', n, '乙 =', n+5)
