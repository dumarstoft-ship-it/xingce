# MK2706X-M2 住房公积金 2022
units, g_units = 452.72, 0.0880
staff, g_staff = 16979.57, 0.0331
new_units, new_staff = 75.22, 1985.44
dep22, g_dep22 = 31935.05, 0.0953
cum_dep = 256927.26
balance22 = 92454.82
wd_people = 6782.63
wd22, g_wd22 = 21363.27, 0.0515
house_share22, house_drop = 79.2, 3.0
g_dep = {2019: 12.61, 2020: 10.55, 2021: 11.24, 2022: 9.53}
g_wd = {2019: 10.46, 2020: 13.94, 2021: 9.51, 2022: 5.15}

print('Q1: balance end-2021')
net = dep22 - wd22
print('  net inflow 2022 =', round(net, 2), ' balance21 =', round(balance22 - net, 2))
opts = {'A': 81883.04, 'B': 88930.89, 'C': 95978.74, 'D': 103026.6}
for k, v in opts.items():
    print('   ', k, v, ' diff from 92454.82 =', round(v - balance22, 2))

print('Q2: 2020 deposit')
d20 = dep22 / (1 + g_dep[2022] / 100) / (1 + g_dep[2021] / 100)
print('  d21 =', dep22 / (1 + g_dep[2022] / 100), ' d20 =', d20)

print('Q3: years with withdrawal rate up')
for y in g_dep:
    print('  ', y, 'wd', g_wd[y], 'dep', g_dep[y], 'up' if g_wd[y] > g_dep[y] else 'down')

print('Q4: 2021 housing vs non-housing withdrawal')
s21 = house_share22 + house_drop
r = s21 / (100 - s21)
print('  share21 =', s21, ' ratio =', r, ' times more =', r - 1)
print('  (2022 ratio =', house_share22 / (100 - house_share22), ')')

print('Q5')
print('  A: wd_people/staff =', wd_people / staff)
print('  B: per-capita withdrawal (万元) =', wd22 * 1e4 / wd_people)
print('  C: units 2021 =', units / (1 + g_units), ' (452.72-75.22 =', units - new_units, ')')
print('  D: cum withdrawals =', round(cum_dep - balance22, 2))
