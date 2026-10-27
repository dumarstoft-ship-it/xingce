# MK2720X-M2 railway freight
print('== Q1 2022 growth: freight shipped vs converted turnover')
g_ship22 = 1.0 + 3.4
g_conv22 = 20.4 - 21.1
print('ship22', g_ship22, 'conv22', round(g_conv22, 2), 'diff', round(g_ship22 - g_conv22, 2))
print('distractors: 2023 diff', 1.0 - 20.4, ' reversed', (1.0 - 3.4) - (20.4 + 21.1))

print('== Q2 table: highest/lowest growth')
tab = {'煤': (278101, 1.9), '冶炼物资': (90986, -5.3), '石油': (13050, 5.4), '粮食': (6847, -8.0), '化肥及农药': (5027, -7.2), '集装箱': (79111, 7.4)}
hi = max(tab, key=lambda k: tab[k][1]); lo = min(tab, key=lambda k: tab[k][1])
print(hi, lo, tab[hi][0] / tab[lo][0], 'options', 23 / 2, 55, 1 / 40, 2 / 7)
print('trap 煤/化肥', 278101 / 5027, '粮食/煤', 6847 / 278101, '集装箱/煤', 79111 / 278101)

print('== Q3 China-Europe trains')
v = 190; inc = v - v / 1.18
print('inc', inc)
y = 2023
while v <= 300:
    y += 1; v += inc; print(y, round(v, 2))

print('== Q4 passenger turnover increment')
conv23, gc = 51189.74, 0.204
fr23, gf = 36460.39, 0.014
inc_conv = conv23 * gc / (1 + gc); inc_fr = fr23 * gf / (1 + gf)
print('inc_conv', inc_conv, 'inc_fr', inc_fr, 'diff', inc_conv - inc_fr)
p23 = conv23 - fr23; p22 = conv23 / (1 + gc) - fr23 / (1 + gf)
print('pass23', p23, 'pass22', p22, 'inc', p23 - p22, 'growth', p23 / p22 - 1)

print('== Q5')
gA = 1.002 * (1 + (0.2 + 4.6) / 100) - 1
print('A national rail 2 yr growth', gA)
other_turn = 36460.39 - 32638.50
print('B other share of freight turnover', other_turn, other_turn / 36460.39)
print('B(trap) other share of conv turnover', 3834.12 / 51189.74)
print('C 2022 grain', 6847 / 0.92, 'fert', 5027 / 0.928)
print('D avg distance growth', (1 - 0.001) / (1 + 0.002) - 1)
