# MK2736F-M2 2024年C市规模以上工业企业经济效益
# key: (1-9 value, 1-9 growth%, 1-12 value, 1-12 growth%)
T = {
    'firms': (7927, 4.4, 7992, 4.4),
    'firms_lm': (1000, 0.8, 1008, 1.1),
    'loss_firms': (1663, -8.9, 1404, -4.6),
    'rev': (20668.30, 6.1, 28029.28, 6.6),
    'cost': (18008.39, 6.6, 24287.06, 6.8),
    'profit': (1069.98, 15.0, 1489.34, 15.6),
    'profit_lm': (718.15, 13.4, 1006.69, 17.9),
    'loss_amt': (190.78, -13.0, 281.22, -15.4),
    'loss_amt_lm': (109.05, -15.6, 175.56, -23.0),
    'recv': (4806.05, 6.3, 4781.75, 6.0),
    'inv': (965.56, -0.2, 1027.08, 3.5),
}

def base(v, g):
    return v / (1 + g / 100)

print('Q1: avg profit per firm (万元)')
p24 = T['profit'][2]; f24 = T['firms'][2]
p23 = base(p24, T['profit'][3]); f23 = base(f24, T['firms'][3])
a24 = p24 / f24 * 1e4; a23 = p23 / f23 * 1e4
print('  2024 avg =', a24, ' 2023 avg =', a23, ' change =', a24 - a23)

print('Q2: large/medium loss amount, Q4 monthly vs Q1-3 monthly')
v9, g9, v12, g12 = T['loss_amt_lm']
q4 = v12 - v9
print('  Q4 total =', q4, ' Q4 monthly =', q4 / 3, ' Q1-3 monthly =', v9 / 9, ' diff =', q4 / 3 - v9 / 9)
print('  (trap (q4 - v9/3)/12 =', (q4 - v9 / 3) / 12, ')')

print('Q3: non-loss vs loss firms, Jan-Sep')
n = T['firms'][0] - T['loss_firms'][0]
print('  non-loss =', n, ' ratio =', n / T['loss_firms'][0], ' times more =', n / T['loss_firms'][0] - 1)
print('  (total/loss =', T['firms'][0] / T['loss_firms'][0], ')')

print('Q4: 2023 Q4 finished goods (as 1-12 minus 1-9)')
v9, g9, v12, g12 = T['inv']
b12 = base(v12, g12); b9 = base(v9, g9)
print('  2023 1-12 =', b12, ' 2023 1-9 =', b9, ' Q4 2023 =', b12 - b9, ' (2024 Q4 =', v12 - v9, ')')

print('Q5')
r9, gr9, r12, gr12 = T['rev']
p9, gp9, p12, gp12 = T['profit']
rq4 = r12 - r9; pq4 = p12 - p9
print('  A: Q4 rev =', rq4, ' Q4 profit =', pq4, ' margin =', pq4 / rq4)
c9, gc9, c12, gc12 = T['cost']
print('  B: Jan-Sep cost increase (亿元) =', c9 * (gc9 / 100) / (1 + gc9 / 100))
print('  C: loss firms 1663 -> 1404, diff =', T['loss_firms'][0] - T['loss_firms'][2], ' (only net change, not 扭亏为盈 count)')
rq4_23 = base(r12, gr12) - base(r9, gr9)
print('  D: 2023 Q4 rev =', rq4_23, ' 2024 Q4 rev =', rq4, ' growth =', rq4 / rq4_23 - 1)
