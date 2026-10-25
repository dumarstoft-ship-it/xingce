from fractions import Fraction as F

# V1 牛吃草中途卖牛: 30头10天, 25头15天 -> x, S; then N cows 5 days, sell 6, 10 more days
x = F(30*10 - 25*15, 10 - 15)          # (30-x)*10 = (25-x)*15
S = (30 - x) * 10
print('V1 growth x =', x, 'stock S =', S)
# (N-x)*5 + (N-6-x)*10 = S
N = (S + x*5 + (6 + x)*10) / 15
print('V1 N =', N, ' check:', (N-x)*5 + (N-6-x)*10 == S)
# err1: ignore growth: 5N + 10(N-6) = S
print('V1 err ignore growth:', (S + 60) / 15)
# err3: growth only in 2nd phase: 5N + (N-6-x)*10 = S
print('V1 err growth only phase2:', (S + (6 + x)*10) / 15)
print('V1 err answer after selling:', N - 6)

# V2 依次加入: 1 machine 50 days, +1 machine every 3 days
total, day, cum = 50, 0, 0
while cum < total:
    day += 1
    machines = (day - 1)//3 + 1
    cum += machines
print('V2 finish on day', day, 'cum', cum)
# naive whole segments: smallest n with 3*n(n+1)/2 >= 50
n = 1
while 3*n*(n+1)//2 < total: n += 1
print('V2 naive whole segments ->', 3*n, 'days')

# V-asym: half work +25%, half -25%, delay 2 days
fac = (F(4,5) + F(4,3)) / 2
print('V-asym factor', fac, 'T =', 2 / (fac - 1))
e2 = F(1,2)*F(4,5) + F(1,2)*F(5,4)      # 降效25%误当时间+25%
e3 = F(1,2)*F(3,4) + F(1,2)*F(4,3)      # 提效25%误当时间-25%
print('V-asym err2 T =', 2/(e2-1), ' err3 T =', 2/(e3-1))

# V-科考: 20 days food, after 5 days 4 return (return trip 5 days, food taken), rest eat 17 days
N = F(17*4 - 4*5, 17 - 15)              # 15N - 20 = 17(N-4)
print('V-kk N =', N, ' check:', 15*N - 20 == 17*(N-4))
print('V-kk err forget return food:', F(17*4, 2), ' err round trip 10d:', F(17*4 - 40, 2))

# V4 按效率分配: each 150 parts; after 2h A left 70, B left 30, C finished 30 min early
a, b, c = F(80,2), F(120,2), F(150, F(3,2))
print('V4 rates', a, b, c)
T = (500 + c) / (a + b + c)            # a T + b T + c (T-1) = 500
print('V4 T =', T, ' C gets', c*(T-1), ' A', a*T, ' B', b*T)
print('V4 err ratio split C =', 500 * c / (a + b + c))
