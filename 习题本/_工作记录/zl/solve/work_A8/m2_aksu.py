# MK2722X-M2 Aksu
gdp = 266.02
ind = [(28.66, 0.058, 0.4), (82.29, 0.027, 0.8), (155.07, 0.036, 2.3)]
print('== Q1')
print('sum pulls', sum(p for _, _, p in ind))
base = sum(v / (1 + r) for v, r, _ in ind)
print('sum values', sum(v for v, _, _ in ind), 'base', base, 'growth', gdp / base - 1)
print('== Q2 increment shares')
incs = [v * r / (1 + r) for v, r, _ in ind]
tot = sum(incs)
print('incs', incs, 'total', tot, 'shares', [i / tot for i in incs])
print('pull-based shares', [p / 3.5 for _, _, p in ind])
print('value shares (GDP structure)', [v / gdp for v, _, _ in ind])
# measured pie angles (clockwise from 12 o'clock)
pies = {'A': (63.05, 150.4), 'B': (69.85, 239.15), 'C': (38.75, 150.2), 'D': (133.55, 277.9)}
for k, (a1, a2) in pies.items():
    print('pie', k, 'white', round(a1 / 360, 3), 'hatched', round((a2 - a1) / 360, 3), 'grey', round((360 - a2) / 360, 3))
print('== Q3')
sep = 183.37 - 158.65
print('Sep', sep, 'Q4', sep * 3, 'year', 183.37 + sep * 3)
print('== Q4 Sep shares')
s19 = [0.038, 0.286, 0.676]; s18 = [0.042, 0.284, 0.674]
for i in range(3):
    v19 = 183.37 * s19[i]; v18 = 158.65 * s18[i]
    print('ind', i + 1, '1-9', round(v19, 3), '1-8', round(v18, 3), 'Sep', round(v19 - v18, 3), 'Sep share', (v19 - v18) / sep, 'vs 1-9 share', s19[i])
print('== Q5')
print('A structure', [round(v / gdp * 100, 2) for v, _, _ in ind])
print('B 2023 secondary', 82.29 / 1.027)
print('C growth 1-9 vs 1-8', 183.37 / 158.65 - 1)
print('D 1-8 sec - prim', 158.65 * (0.284 - 0.042), ' (trap 1-9)', 183.37 * (0.286 - 0.038))
