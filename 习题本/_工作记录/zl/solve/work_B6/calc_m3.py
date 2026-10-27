# MK2736F-M2: 2024 C city above-scale industrial enterprises
d = {  # item: (1-9 value, 1-9 yoy%, 1-12 value, 1-12 yoy%)
    'firms': (7927, 4.4, 7992, 4.4),
    'firms_lm': (1000, 0.8, 1008, 1.1),
    'loss_firms': (1663, -8.9, 1404, -4.6),
    'revenue': (20668.30, 6.1, 28029.28, 6.6),
    'cost': (18008.39, 6.6, 24287.06, 6.8),
    'profit': (1069.98, 15.0, 1489.34, 15.6),
    'profit_lm': (718.15, 13.4, 1006.69, 17.9),
    'loss_amt': (190.78, -13.0, 281.22, -15.4),
    'loss_amt_lm': (109.05, -15.6, 175.56, -23.0),
    'receivable': (4806.05, 6.3, 4781.75, 6.0),
    'finished': (965.56, -0.2, 1027.08, 3.5),
}

print('=== Q1 avg profit per firm 2024 vs 2023 (万元) ===')
p24, f24 = d['profit'][2], d['firms'][2]
p23, f23 = p24 / 1.156, f24 / 1.044
a24, a23 = p24 / f24 * 1e4, p23 / f23 * 1e4
print('avg24', a24, 'avg23', a23, 'change', a24 - a23, 'avg growth', 1.156 / 1.044 - 1)

print('=== Q2 large/medium loss amount monthly avg Q4 vs Q1-3 (亿元) ===')
q4 = d['loss_amt_lm'][2] - d['loss_amt_lm'][0]
m_q4 = q4 / 3
m_q13 = d['loss_amt_lm'][0] / 9
print('Q4 total', q4, 'Q4 monthly', m_q4, 'Q1-3 monthly', m_q13, 'diff', m_q4 - m_q13)
print('trap: full-year monthly - 1-9 monthly', d['loss_amt_lm'][2] / 12 - m_q13)

print('=== Q3 non-loss vs loss firms 1-9 ===')
nonloss = d['firms'][0] - d['loss_firms'][0]
print('nonloss', nonloss, 'ratio', nonloss / d['loss_firms'][0], 'more by (times)', nonloss / d['loss_firms'][0] - 1)
nonloss12 = d['firms'][2] - d['loss_firms'][2]
print('traps: total/loss', d['firms'][0] / d['loss_firms'][0], '1-12 ratio', nonloss12 / d['loss_firms'][2],
      '1-12 more-by', nonloss12 / d['loss_firms'][2] - 1)

print('=== Q4 2023 Q4 finished goods ===')
f23_12 = d['finished'][2] / 1.035
f23_9 = d['finished'][0] / 0.998
print('2023 1-12', f23_12, '2023 1-9', f23_9, '2023 Q4', f23_12 - f23_9)
print('trap 2024 Q4', d['finished'][2] - d['finished'][0])

print('=== Q5 ===')
rq4 = d['revenue'][2] - d['revenue'][0]
pq4 = d['profit'][2] - d['profit'][0]
print('A: Q4 revenue', rq4, 'Q4 profit', pq4, 'margin', pq4 / rq4)
ci = d['cost'][0] * 0.066 / 1.066
print('B: 1-9 cost increase (亿元)', ci, '= 万元', ci * 1e4)
print('C: loss firms change', d['loss_firms'][0] - d['loss_firms'][2], 'total firms change', d['firms'][2] - d['firms'][0])
r23_12 = d['revenue'][2] / 1.066
r23_9 = d['revenue'][0] / 1.061
rq4_23 = r23_12 - r23_9
print('D: 2023 Q4 revenue', rq4_23, '2024 Q4 yoy', rq4 / rq4_23 - 1)
