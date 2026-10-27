# MK2715X-M2 上汽集团 2024年1-10月
prod = [24.39, 18.97, 39.02, 35.47, 32.77, 30.72, 23.75, 26.17, 33.67, 41.66]
sale = [24.49, 20.78, 38.14, 36.00, 33.22, 30.05, 25.15, 25.76, 31.33, 40.19]
nprod = [7.15, 5.93, 8.40, 7.48, 8.22, 9.42, 6.92, 8.78, 14.22, 16.53]
nsale = [6.43, 6.10, 8.48, 7.46, 8.29, 9.34, 7.11, 8.66, 12.93, 15.71]
print('check sums:', round(sum(prod), 2), '(306.58)', round(sum(sale), 2), '(305.12)',
      round(sum(nprod), 2), '(93.02)', round(sum(nsale), 2), '(90.51)')

oct_p, g_oct_p = 41.66, -0.1374
oct_s, g_oct_s = 40.19, -0.1822
cum_p, g_cum_p = 306.58, -0.2099
cum_s, g_cum_s = 305.12, -0.2113
noct_p, g_noct_p = 16.53, 0.6045
noct_s, g_noct_s = 15.71, 0.5108
ncum_p, g_ncum_p = 93.02, 0.2446
ncum_s, g_ncum_s = 90.51, 0.2022

print('Q1: Oct share of Jan-Oct production, change')
s24 = oct_p / cum_p
s23 = (oct_p / (1 + g_oct_p)) / (cum_p / (1 + g_cum_p))
print('  s24 =', s24, ' s23 =', s23, ' change pp =', (s24 - s23) * 100)
print('  formula =', s24 * (g_oct_p - g_cum_p) / (1 + g_oct_p) * 100)

print('Q2: Oct 2023 NEV share of sales')
print('  ', (noct_s / (1 + g_noct_s)) / (oct_s / (1 + g_oct_s)), ' (2024:', noct_s / oct_s, ')')

print('Q3: quarterly production')
q = [sum(prod[0:3]), sum(prod[3:6]), sum(prod[6:9])]
print('  Q1 =', round(q[0], 2), ' Q2 =', round(q[1], 2), ' Q3 =', round(q[2], 2))

print('Q4: Q3 NEV sales/production')
p3 = sum(nprod[6:9]); s3 = sum(nsale[6:9])
print('  prod =', round(p3, 2), ' sales =', round(s3, 2), ' ratio =', s3 / p3)

print('Q5')
gt = [i + 1 for i in range(10) if sale[i] > prod[i]]
lt = [i + 1 for i in range(10) if sale[i] < prod[i]]
print('  A: months sales>prod', gt, len(gt), '; sales<prod', lt, len(lt))
print('  B: Oct NEV prod', noct_p, ' Jan-Sep avg', (ncum_p - noct_p) / 9, ' (chart-based', sum(nprod[:9]) / 9, ')')
print('  C: NEV prod growth', g_noct_p, ' vs total prod growth', g_oct_p,
      ' share24', noct_p / oct_p, ' share23', (noct_p / (1 + g_noct_p)) / (oct_p / (1 + g_oct_p)))
print('  D: prod share', ncum_p / cum_p, ' sales share', ncum_s / cum_s)
