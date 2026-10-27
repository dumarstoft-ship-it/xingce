# MK2710X-M3 calculations
print('--- Q1: 2023年4月 进出口总值')
jun = 3.49
may = jun / 1.012
apr_chain = may / 1.012
apr_sub = 10.34 - jun - may
print('5月', may, '4月(环比回推)', apr_chain, '4月(二季度减5、6月)', apr_sub)
print('trap 10.34-3.49*2', 10.34 - 2 * 3.49, ' (10.34-3.49)/2', (10.34 - 3.49) / 2)

print('--- Q2: 上半年进出口增速')
ex_b = 11.46 / 1.037; im_b = 8.64 / 0.999
tot_b = ex_b + im_b
g = 20.10 / tot_b - 1
print('出口基期', ex_b, '进口基期', im_b, '总基期', tot_b, 'growth', g)
print('naive avg (3.7-0.1)/2', (3.7 - 0.1) / 2)

print('--- Q3: 民营企业进出口增速')
sh_now = 0.527; sh_base = 0.527 - 0.033
print('formula (1+g)*52.7/49.4-1 =', (1 + g) * sh_now / sh_base - 1)
print('direct 10.59/(tot_b*0.494)-1 =', 10.59 / (tot_b * sh_base) - 1)

print('--- Q4: 欧盟增量 - 美国增量 (亿元)')
eu = 2.75e4 * 0.019 / 1.019
us = 2.25e4 * (-0.084) / (1 - 0.084)
print('欧盟增量', eu, '美国增量', us, 'difference', eu - us, ' trap |us|-eu', -us - eu)

print('--- Q5')
print('1: Q2 环比', 10.34 / 9.76 - 1)
print('2: 民营 52.7 vs 外商+国有', 30.7 + 16.4, 'diff pts', 52.7 - (30.7 + 16.4),
      ' value-based', (10.59 - 6.16 - 3.29) / 20.10 * 100, ' ratio', 10.59 / (6.16 + 3.29))
print('3: (东盟+欧盟+美国)/总值', (3.08 + 2.75 + 2.25) / 20.10)
