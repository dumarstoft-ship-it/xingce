# Check numeric examples proposed in review suggestions (not part of the key)
from fractions import Fraction as F

# v04 deepening: 15% dispatch; first 10 converted to regular staff (total unchanged), then 20 returned; ratio becomes 10%
sols = []
for T in range(1, 5000):
    d = F(15, 100) * T
    if d.denominator != 1: continue
    if d - 30 > 0 and F(d - 30, T - 20) == F(1, 10):
        sols.append(T)
print('v04 deep: original total', sols)
# trap: blindly keep "others unchanged" -> 0.85T = 0.9(T-20)
print('   trap others-unchanged ->', [T for T in range(1, 5000) if F(85, 100) * T == F(9, 10) * (T - 20)])
# trap: treat conversion like removal (total -30)
print('   trap total-30 ->', [T for T in range(1, 5000) if F(15, 100) * T - 30 == F(1, 10) * (T - 30)])

# v09 deepening: 2024 Sep = Aug*0.8; 2025 Sep = 2025 Aug*0.75; Aug+Sep 2025 vs 2024 +40%; ask 2025 Sep YoY
aug24 = F(100); sep24 = aug24 * F(8, 10)
tot25 = (aug24 + sep24) * F(14, 10)
# aug25 + 0.75 aug25 = tot25
aug25 = tot25 / F(175, 100); sep25 = aug25 * F(75, 100)
print('v09 deep: Sep25 YoY', (sep25 / sep24 - 1) * 100, '% ; Aug25 YoY', (aug25 / aug24 - 1) * 100, '%')

# v12 deepening: a, a-4, a+7; rotation 甲->乙->丙->甲; final equal; groups x(甲) y(乙) z(丙), x+y+z = 41; ask z
res = set()
for a in range(20, 200):
    for x in range(1, a):
        for y in range(1, a - 4):
            z = 41 - x - y
            if z < 1 or z > a + 7: continue
            A, B, C = a - x + z, a - 4 - y + x, a + 7 - z + y
            if A == B == C:
                res.add((x, y, z))
print('v12 deep: (x,y,z) groups', res)

# v15 deepening: big = 2 small (from 5(5B+2S) = 6(2B+6S)); 8 trucks total, 4 trips exactly, all full -> number of big trucks
for B in range(0, 9):
    S = 8 - B
    if 4 * (2 * B + S) == 60:
        print('v15 deep: big trucks', B, 'small', S)

# v17 deepening: legs 18 (甲乙), d (甲乙丙), 12 (乙丙); total fare 150 proportional to km; 丙 pays 9 less than 甲; find d
for d in range(1, 200):
    r = F(150, 30 + d)
    jia = r * 18 / 2 + r * d / 3
    bing = r * d / 3 + r * 12 / 2
    if jia - bing == 9:
        print('v17 deep: shared km d =', d, 'rate', r, 'jia', jia, 'bing', bing)

# v07 deepening: 甲 30 all year; 乙 80 from Jan, withdraws 40 at the start of month w (w=2..12); 丙 joins Oct (80 x 3)
# condition: 乙's share is 2.5x 丙's -> find w
for w in range(2, 13):
    yi = 80 * (w - 1) + 40 * (13 - w)
    if F(yi) == F(5, 2) * 240:
        print('v07 deep: 乙 withdraws at start of month', w, 'weight', yi)
