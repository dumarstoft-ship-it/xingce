# MK2702X-M1 calculations
print('--- Q1: 2022 Q3 纺织利润')
p_q13_22 = 1026 / (1 - 0.088)
p_h1_22 = 595 / (1 - 0.213)
print('2022前三季度', p_q13_22, '2022上半年', p_h1_22, 'Q3', p_q13_22 - p_h1_22)
print('trap 2023 Q3', 1026 - 595)

print('--- Q2: 出口同比增量倍数')
inc_q13 = 2232 * (-0.095) / (1 - 0.095)
inc_h1 = 1427 * (-0.083) / (1 - 0.083)
print('前三季度增量', inc_q13, '上半年增量', inc_h1, 'ratio', inc_q13 / inc_h1)
print('trap ratio of rates', 9.5 / 8.3, 'ratio of totals', 2232 / 1427)

print('--- Q3: 2022 服装利润增速')
rev22 = 14539; prof22 = 764
rev21 = rev22 / (1 - 0.046)
m21 = 0.053 + 0.001
print('formula (1+g_rev)*m22/m21-1 =', (1 - 0.046) * 0.053 / m21 - 1)
print('direct: profit21 = rev21*5.4% =', rev21 * m21, 'growth', prof22 / (rev21 * m21) - 1)
print('actual margin 2022', prof22 / rev22)
print('formula using actual margin 5.255/5.355:', (1 - 0.046) * (prof22 / rev22) / (prof22 / rev22 + 0.001) - 1)

print('--- Q4: 2022 H2 服装营业收入利润率')
rev_h1 = 6885; prof_h1 = 307
print('H2 rev', rev22 - rev_h1, 'H2 profit', prof22 - prof_h1, 'margin', (prof22 - prof_h1) / (rev22 - rev_h1))
print('H1 margin', prof_h1 / rev_h1, 'full', prof22 / rev22)

print('--- Q5')
# A: Q3 value added growth, weights unknown; illustrate with revenue weights
rq13_22 = 33952 / (1 - 0.033)
rh1_22 = 21818 / (1 - 0.051)
rq3_22 = rq13_22 - rh1_22
x = (-2.2 * rq13_22 + 3.0 * rh1_22) / rq3_22
print('A: implied Q3 VA growth with revenue base weights', x, ' time-weight 2/3:', (-2.2 * 3 + 3.0 * 2))
print('B: 8月降幅', 4.8 + 3.6, ' trap', 4.8 - 3.6)
print('C: 2023 服装出口', 1551 * 1.064)
print('D: 2022H1 亏损企业数', 13067 * 0.27)
