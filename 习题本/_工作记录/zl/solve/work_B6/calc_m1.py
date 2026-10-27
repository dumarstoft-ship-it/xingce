# MK2728X-M2: 2024-2025.3 cross-region personnel flow (万人次)
cross = {  # cumulative value, cumulative yoy %
    '24_2': (1171807, None), '24_3': (1671682, 10.2), '24_4': (2189330, 8.4),
    '24_5': (2736268, 8.3), '24_6': (3241011, 7.4), '24_7': (3799308, 6.6),
    '24_8': (4396867, 6.1), '24_9': (4909109, 5.4), '24_10': (5492663, 5.5),
    '24_11': (5972154, 5.4), '24_12': (6459234, 5.4), '25_2': (1229386, 4.9),
    '25_3': (1738829, 4.0)}
hw = {
    '24_2': (1086652, 10.3), '24_3': (1547451, 9.0), '24_4': (2021233, 7.4),
    '24_5': (2523351, 7.4), '24_6': (2983967, 6.6), '24_7': (3489943, 5.8),
    '24_8': (4029157, 5.4), '24_9': (4499504, 4.7), '24_10': (5036908, 4.9),
    '24_11': (5478704, 4.8), '24_12': (5929002, 4.8), '25_2': (1139263, 4.8),
    '25_3': (1607309, 3.9)}

print('=== Q1 quarterly cross-region 2024 ===')
c = lambda k: cross[k][0]
q = {'Q1': c('24_3'), 'Q2': c('24_6') - c('24_3'), 'Q3': c('24_9') - c('24_6'), 'Q4': c('24_12') - c('24_9')}
for k, v in q.items():
    print(k, v)
print('min:', min(q, key=q.get))

print('=== Q2 2023Q1 non-highway share ===')
cr23 = c('24_3') / 1.102
hw23 = hw['24_3'][0] / 1.090
print('cross23', cr23, 'hw23', hw23, 'nonhw share', 1 - hw23 / cr23)
print('trap (2024 share)', 1 - hw['24_3'][0] / c('24_3'))
# rounding robustness
for gc in (1.1015, 1.1025):
    for gh in (1.0895, 1.0905):
        print(' range', gc, gh, 1 - (hw['24_3'][0] / gh) / (c('24_3') / gc))

print('=== Q3 2025Q1 hw vs 2023Q1 ===')
print('formula', 1.039 * 1.090 - 1, 'simple sum', 0.039 + 0.090)
print('direct', hw['25_3'][0] / (hw['24_3'][0] / 1.09) - 1)
print('2025Q1 vs 2024Q1 direct', hw['25_3'][0] / hw['24_3'][0] - 1)

print('=== Q4 ===')
h = lambda k: hw[k][0]
for m in range(7, 13):
    print('1-%d cumulative cross yoy' % m, cross['24_%d' % m][1])
months = {}
prev = None
order = ['24_2', '24_3', '24_4', '24_5', '24_6', '24_7', '24_8', '24_9', '24_10', '24_11', '24_12']
for i, k in enumerate(order):
    if i == 0:
        continue
    months[int(k.split('_')[1])] = h(k) - h(order[i - 1])
print('hw monthly 2024', months)
for m in range(4, 13):
    print('hw mom month %d: %.4f%%' % (m, (months[m] / months[m - 1] - 1) * 100))

print('=== Q5 ===')
inc = h('24_12') * 0.048 / 1.048
print('A: 2024 hw increase (万人次)', inc, '亿人次', inc / 1e4)
# B: monthly yoy for hw
hw23cum = {k: hw[k][0] / (1 + hw[k][1] / 100) for k in order}
for i, k in enumerate(order):
    if i == 0:
        continue
    m24 = h(k) - h(order[i - 1])
    m23 = hw23cum[k] - hw23cum[order[i - 1]]
    print('month', k, 'hw24', m24, 'hw23', round(m23), 'yoy %.3f%%' % ((m24 / m23 - 1) * 100))
# increment method for September
inc9 = h('24_9') * 0.047 / 1.047
inc8 = h('24_8') * 0.054 / 1.054
print('cum increment 1-9', inc9, '1-8', inc8, 'Sep increment', inc9 - inc8)
# robustness for Sep with rounding bounds
lo = h('24_9') - (h('24_9') / 1.0465 - h('24_8') / 1.0545)
hi = h('24_9') - (h('24_9') / 1.0475 - h('24_8') / 1.0535)
sep24 = h('24_9') - h('24_8')
print('Sep 2024', sep24, '2023 Sep range', h('24_9') / 1.0475 - h('24_8') / 1.0535, h('24_9') / 1.0465 - h('24_8') / 1.0545)
# C
nonhw_h1 = c('24_6') - h('24_6')
print('C: H1 nonhw', nonhw_h1, 'share', nonhw_h1 / c('24_6'))
# D
avg = c('25_3') / 3
print('D: monthly avg', avg, 'annual', avg * 12, '亿人次', avg * 12 / 1e4)
