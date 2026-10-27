# MK2712X-M1 payments 2023Q1
print("Q1: total bank accounts QoQ growth")
unit = 9517.38/10000; pers = 141.26
prev = unit/1.0293 + pers/1.0037
print('  sum now', unit+pers, ' prev', prev, ' growth', ((unit+pers)/prev-1)*100, ' using 142.21:', (142.21/prev-1)*100)
print("Q2: per-capita debit cards")
pop = 95.73/6.78
print('  pop (亿)', pop, ' debit per capita', 87.82/pop, ' = 6.78*87.82/95.73 =', 6.78*87.82/95.73)
print("Q3: QoQ growth of merchants/POS/ATM")
r = {}
for n, now, dec in [('merchant',2561.38,161.47),('POS',3309.74,246.33),('ATM',88.27,1.32)]:
    r[n] = -dec/(now+dec)*100
    print('  ', n, r[n])
print('  max-min', max(r.values())-min(r.values()))
print("Q4: avg amount per bank cashier's cheque")
print('  ', ((1-0.0384)/(1-0.1593)-1)*100)
print("Q5")
print('  A: 2022Q1 NON-cash payments =', 1145.87/1.1846, '(material has no cash-payment data)')
print('  B: basic deposit share', 6689.88/9517.38*100)
print('  C: avg per bill (万元)', 23.63e8/2417.44, ' [23.63万亿=23.63e12 元 / 2417.44e4 笔 = ', 23.63e12/2417.44e4/1e4, '万元]')
print('  D: cheque', (1782.31, 17.81e4), 'commercial', (628.50, 5.72e4), 'bank draft', (2.36, 316.25), 'cashier', (4.27, 756.42), ' (万笔, 亿元)')
