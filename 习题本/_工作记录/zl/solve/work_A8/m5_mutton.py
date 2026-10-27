# MK2740X-M3 mutton imports Jan 2024
print('== Q1 Australia import value')
vols = {'NZ': 19327.58, 'AU': 19208.14, 'UY': 1226.35, 'CL': 366.47}
print('sum vols', round(sum(vols.values()), 2), 'total mutton vol 40128.54')
au = 13155.32 - 6573.92 - 383.08 - 100.69
print('AU value', round(au, 2))
# cross-check with yoy growths
tot22 = 13155.32 / (1 - 0.1219)
nz22 = 6573.92 / (1 - 0.2515); uy22 = 383.08 / 1.1602; cl22 = 100.69 / (1 + 8.7431)
au22 = tot22 - nz22 - uy22 - cl22
print('cross-check AU 2023-01', au22, '-> 2024-01', au22 * 1.0408)
print('== Q2')
lamb = 644.29 / 672.14; sheep = 5730.41 / 39009.96
print('lamb share', lamb, 'sheep share', sheep, 'diff pp', (lamb - sheep) * 100)
print('check components', 39009.96 + 672.14 + 446.44)
print('== Q3 goat avg price Jan 2023')
v23 = 183.90 / (1 + 9.7401); q23 = 446.44 / (1 + 10.6728)
print('val23', v23, 'vol23', q23, 'price', v23 / q23, ' current price', 183.90 / 446.44)
print('== Q4 AU Dec 2023 vs Jan 2023 volume')
print(1.3377 / 1.0338 - 1)
print('== Q5')
print('A frozen bone-in sheep value decrease', 9318.15 / (1 - 0.216) * 0.216)
print('B mom abs', {'NZ': 18.22, 'AU': 3.18, 'UY': 3.06, 'CL': 15.14})
print('C Chile multiple', 1 + 21.4373)
print('D share', 24929.62 / 40128.54)
