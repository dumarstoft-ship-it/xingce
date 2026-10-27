# MK2701X-M1 NEV / PHEV 2023
sales = [12.1, 14.9, 16.3, 16.5, 19.4, 23.3, 23.9, 24.9, 27.7, 31.0, 32.3, 36.4]
yoy = [42.5, 98.0, 84.3, 144.5, 94.4, 93.0, 77.0, 72.8, 64.4, 80.2, 89.5, 92.6]
print('sum monthly', round(sum(sales), 1), 'vs annual 280.7')
print('== Q1 2021 NEV sales')
g22 = 0.379 + 0.555
s22 = 949.5 / 1.379
print('2022 growth', g22, '2022 sales', s22, '2021 sales', s22 / (1 + g22), 'factor', 1.379 * (1 + g22))
print('== Q2 PHEV share change')
sh23 = 280.7 / 949.5; sh22 = (280.7 / 1.847) / (949.5 / 1.379)
print(sh23, sh22, 'pp', (sh23 - sh22) * 100, ' formula', sh23 * (0.847 - 0.379) / 1.847 * 100)
print('== Q3/Q4 quarters')
q = [round(sum(sales[i:i + 3]), 1) for i in range(0, 12, 3)]
print('quarters', q, 'Q4 qoq', q[3] / q[2] - 1, 'max/min', max(q) / min(q), 'more times', max(q) / min(q) - 1)
print('== Q5')
print('A 2022 PHEV growth', 84.7 + 66.9)
m3_22 = sales[2] / (1 + yoy[2] / 100); m4_22 = sales[3] / (1 + yoy[3] / 100)
print('B 2022 Mar', m3_22, 'Apr', m4_22)
print('C H1 avg', sum(sales[:6]) / 6)
imax = yoy.index(max(yoy)); imin = yoy.index(min(yoy))
print('D fastest month', imax + 1, sales[imax], 'slowest month', imin + 1, sales[imin])
