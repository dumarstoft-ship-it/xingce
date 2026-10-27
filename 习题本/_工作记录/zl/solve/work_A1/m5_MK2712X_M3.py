# MK2712X-M3 2023年5月动力电池
# (may, yoy%, mom%, jan_may, yoy_cum%)
prod = {
    'total': (56556.1, 57.4, 20.4, 233496.1, 34.7),
    'ncm': (18611.0, 11.9, 5.8, 81879.3, 17.0),
    'lfp': (37817.7, 96.7, 29.0, 151258.1, 46.7),
    'lmo': (80.6, 120.3, 323.0, 161.3, -18.7),
    'lto': (15.8, -38.1, None, 47.7, -27.1),
    'oth': (31.0, None, -35.0, 149.7, None),
}
inst = {
    'total': (28242.3, 52.1, 12.3, 119231.6, 43.5),
    'ncm': (9028.1, 8.7, 12.8, 37911.2, 11.4),
    'lfp': (19153.3, 87.2, 11.8, 81195.7, 65.9),
    'lmo': (42.8, 1369.9, 621.0, 65.8, -8.2),
    'lto': (15.8, -38.1, None, 47.4, -20.8),
    'oth': (2.3, None, 41.3, 11.6, None),
}

print('Q1: Apr 2023 vs May 2022 production')
m, y, mo, c, yc = prod['total']
apr23 = m / (1 + mo / 100); may22 = m / (1 + y / 100)
print('  apr23 =', apr23, ' may22 =', may22, ' growth =', apr23 / may22 - 1)
print('  (1.574/1.204-1) =', 1.574 / 1.204 - 1)

print('Q2: LFP installed Jan-Mar 2023')
m, y, mo, c, yc = inst['lfp']
apr = m / (1 + mo / 100)
print('  apr =', apr, ' jan-mar =', c - m - apr)

print('Q3: 2022 Jan-May NCM share of production')
s = (prod['ncm'][3] / (1 + prod['ncm'][4] / 100)) / (prod['total'][3] / (1 + prod['total'][4] / 100))
print('  share22 =', s, ' share23 =', prod['ncm'][3] / prod['total'][3])

print('Q4: Jan-Apr 2023 installed LMO vs LTO')
lmo14 = inst['lmo'][3] - inst['lmo'][0]
lto14 = inst['lto'][3] - inst['lto'][0]
print('  lmo =', lmo14, ' lto =', lto14, ' diff =', lto14 - lmo14)

print('Q5')
m, y, mo, c, yc = inst['ncm']
print('  A: NCM installed MoM increase =', m - m / (1 + mo / 100), ' (YoY increase =', m - m / (1 + y / 100), ')')
m, y, mo, c, yc = prod['lfp']
print('  B: LFP prod May =', m, ' Jan-Apr avg =', (c - m) / 4)
print('  C: LFP/NCM installed Jan-May =', inst['lfp'][3] / inst['ncm'][3])
def jan_apr(d):
    m, y, mo, c, yc = d
    cur = c - m
    base = c / (1 + yc / 100) - m / (1 + y / 100)
    return cur, base
lc, lb = jan_apr(inst['lmo'])
tc, tb = jan_apr(inst['total'])
print('  D: LMO Jan-Apr 2023 =', lc, ' 2022 =', lb, ' growth =', lc / lb - 1)
print('     total Jan-Apr 2023 =', tc, ' 2022 =', tb, ' growth =', tc / tb - 1)
print('     share 2023 =', lc / tc, ' share 2022 =', lb / tb)
