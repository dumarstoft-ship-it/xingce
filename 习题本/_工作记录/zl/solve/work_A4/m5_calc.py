# MK2733X-M2 calculations
years = [2018, 2019, 2020, 2021, 2022]
prod = {2018: (378859, 262170, 27278, 20458, 68953),
        2019: (397317, 272162, 27415, 22250, 75490),
        2020: (407295, 274924, 27696, 24438, 80237),
        2021: (427115, 284886, 28617, 25627, 87985),
        2022: (463808, 314084, 29358, 27494, 92872)}
cons = {2018: (471925, 278436, 89194, 35866, 68429),
        2019: (487488, 281281, 92623, 38999, 74585),
        2020: (498314, 283541, 93683, 41858, 79232),
        2021: (525896, 293976, 97817, 46279, 87824),
        2022: (540956, 304042, 96839, 45444, 94631)}
for name, t in (('prod', prod), ('cons', cons)):
    for y in years:
        tot, *parts = t[y]
        print(name, y, 'sum check', sum(parts), tot, sum(parts) == tot)

print('--- Q1: 其他能源生产增速')
for y in years[1:]:
    a, b = prod[y][4], prod[y - 1][4]
    print(y, 'inc', a - b, 'growth %.2f%%' % ((a / b - 1) * 100))

print('--- Q2: 2021 原煤/原油 消费增量')
dc = cons[2021][1] - cons[2020][1]
do = cons[2021][2] - cons[2020][2]
print('原煤增量', dc, '原油增量', do, 'ratio', dc / do)

print('--- Q3: 2022 消费结构')
tot = cons[2022][0]
for nm, v in zip(['原煤(灰)', '原油(格)', '天然气(白)', '其他(黑)'], cons[2022][1:]):
    print('  %s %.2f%%  %.1f deg' % (nm, v / tot * 100, v / tot * 360))
print('Option B measured: gray %.1f checker %.1f white %.1f black %.1f' % (201.6 / 3.6, (269.4 - 201.6) / 3.6, (296 - 269.4) / 3.6, (360 - 296) / 3.6))
print('Option D measured: gray %.1f checker %.1f white %.1f black %.1f' % (201 / 3.6, (263 - 201) / 3.6, (305.7 - 263) / 3.6, (360 - 305.7) / 3.6))
print('2022 production shares (option A?):', [round(v / prod[2022][0] * 100, 2) for v in prod[2022][1:]])
print('2018 production shares (option C?):', [round(v / prod[2018][0] * 100, 2) for v in prod[2018][1:]])
for y in years:
    print('cons shares', y, [round(v / cons[y][0] * 100, 2) for v in cons[y][1:]])

print('--- Q4: 天然气年均生产')
g = [prod[y][3] for y in years]
print(g, sum(g), sum(g) / 5)

print('--- Q5')
for y in years:
    d = cons[y][1] - prod[y][1]
    print('A', y, '原煤 消费-生产', d, '|d|>10000', abs(d) > 10000)
for y in years[1:]:
    print('B', y, [cons[y][i] - cons[y - 1][i] for i in (1, 2, 3)])
s = sum(cons[2021][1:4])
print('C 2021 三项之和', s, 'share', s / cons[2021][0], ' 1-其他', 1 - cons[2021][4] / cons[2021][0])
print('D 2022 vs 2020', cons[2022][0] / cons[2020][0] - 1)
