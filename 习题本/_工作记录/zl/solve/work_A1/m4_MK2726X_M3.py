# MK2726X-M3 第三方支付 2023
tot, gt = 544.7, 0.110
per, gp = 345.4, 0.124
ent = 199.3
off_acq, d_off = 82.7, -0.7
ind, d_ind = 113.9, 16.2
cross, d_cross = 2.7, 0.5
mob, gm = 63.6, 0.164
onl, go = 32.2, 0.167
offl = 31.4
cnt, gc = 5451.7, 0.203
gc_up = 0.162

print('Q1: offline increase')
inc_mob = mob * gm / (1 + gm)
inc_onl = onl * go / (1 + go)
print('  mob inc =', inc_mob, ' onl inc =', inc_onl, ' offline inc =', inc_mob - inc_onl)

print('Q2: enterprise growth')
tot22 = tot / (1 + gt); per22 = per / (1 + gp)
ent22 = tot22 - per22
print('  method1: ent22 =', ent22, ' growth =', ent / ent22 - 1)
print('  check components sum =', off_acq + ind + cross)
inc = d_off + d_ind + d_cross
print('  method2: inc =', inc, ' growth =', inc / (ent - inc))

print('Q3: online share change')
s23 = onl / mob
s22 = (onl / (1 + go)) / (mob / (1 + gm))
print('  s23 =', s23, ' s22 =', s22, ' change (pp) =', (s23 - s22) * 100)
print('  formula a/b*(a-b)/(1+a) =', s23 * (go - gm) / (1 + go) * 100)

print('Q4: transaction count with constant increment')
inc_c = cnt * gc / (1 + gc)
print('  increment =', inc_c)
v = cnt; y = 2023
while v <= 8000:
    y += 1; v += inc_c
    print('  ', y, v)
print('  years needed =', (8000 - cnt) / inc_c)

print('Q5')
mob22 = mob / (1 + gm); onl22 = onl / (1 + go); off22 = mob22 - onl22
print('  (1) 2022 online =', onl22, ' offline =', off22, ' diff =', onl22 - off22)
g22 = gc - gc_up
c22 = cnt / (1 + gc); c21 = c22 / (1 + g22)
print('  (2) 2022 growth =', g22, ' 2022 cnt =', c22, ' 2021 cnt =', c21)
print('  (3) 2022 产业 =', ind - d_ind, ' 线下收单 =', off_acq - d_off, ' ratio =', (ind - d_ind) / (off_acq - d_off))
print('  (4) 2022 avg per tx (元) =', mob22 * 1e12 / (c22 * 1e8))
