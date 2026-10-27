# MK2711X-M1 software revenue Jan-Feb 2023
print('== Q1 2021 Jan-Feb revenue')
f = 1.11 * (1 + 0.11 + 0.006)
print('factor', f, '2021', 14461 / f, '2022', 14461 / 1.11)
print('== Q2 top5 / 6-10')
prov = [('北京', 3163, 12.7), ('广东', 2714, 14.5), ('江苏', 1880, 9.0), ('山东', 1480, 15.8), ('浙江', 1270, 3.9),
        ('上海', 1188, 8.1), ('四川', 672, 15.0), ('山西', 340, 6.7), ('福建', 301, 6.9), ('重庆', 276, 19.2)]
t5 = sum(p[1] for p in prov[:5]); b5 = sum(p[1] for p in prov[5:])
print('top5', t5, '6-10', b5, 'ratio', t5 / b5)
print('== Q3 15 sub-provincial cities growth')
print(1.11 * 51.4 / 51.9 - 1)
print('== Q4 regional shares')
reg = [('东部', 12244), ('中部', 476), ('西部', 1492), ('东北', 249)]
tot = sum(v for _, v in reg)
print('total', tot, [(k, round(v / tot * 100, 2)) for k, v in reg])
pies = {'A': (302.9, 323.35, 351.75), 'B': (181.15, 199.5, 302.65), 'C': (304.8, 316.1, 353.6), 'D': (322.0, 328.95, 344.8)}
for k, (a1, a2, a3) in pies.items():
    print('pie', k, [round(x / 3.6, 1) for x in (a1, a2 - a1, a3 - a2, 360 - a3)])
print('== Q5')
hi = max(prov, key=lambda p: p[2]); lo = min(prov, key=lambda p: p[2])
print('(1) highest', hi, 'lowest', lo, 'current ratio', hi[1] / lo[1], 'base ratio', (hi[1] / (1 + hi[2] / 100)) / (lo[1] / (1 + lo[2] / 100)))
print('(2) west/mid', 1492 / 476, 'more times', 1492 / 476 - 1)
gd = 2714 * 0.145 / 1.145; sx = 340 * 0.067 / 1.067
print('(3) GD inc', gd, 'SX inc', sx, 'diff', gd - sx)
