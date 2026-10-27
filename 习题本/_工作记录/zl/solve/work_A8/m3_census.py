# MK2701X-M3 legal entities 2018 vs 2013
print('== Q1 JJJ avg employees per unit growth')
print((1 + 0.096) / (1 + 0.905) - 1, ' formula', (0.096 - 0.905) / 1.905)
print('== Q2 YRD female share')
fem = [498.6, 1360.2, 997.0, 499.7]; emp = [1204.4, 3929.2, 2951.8, 1366.2]; units = [44.1, 205.4, 154.5, 81.3]
print('female', sum(fem), 'emp', sum(emp), 'share', sum(fem) / sum(emp), 'units', sum(units))
print('== Q3 YRD 2013 avg')
u13 = 485.3 - 208.0; e13 = 9451.6 - 553.4
print('units13', u13, 'emp13', e13, 'avg', e13 / u13, ' trap 2018 avg', 9451.6 / 485.3)
print('== Q4 west growth')
print('share method', 2.007 * 18.6 / 18.2 - 1)
w13 = 2178.9 / 2.007 * 0.182
print('w13', w13, 'growth', 405.8 / w13 - 1, ' actual 2018 share', 405.8 / 2178.9)
print('== Q5')
jjj = 98.9 + 29.1 + 115.1
print('A JJJ', jjj, jjj / 2178.9, 'sum shares', 4.5 + 1.3 + 5.3)
print('B east avg', 21621.0 / 1280.2, 'west avg', 7393.4 / 405.8, 'mid avg', 9309.2 / 492.9)
j13 = 243.1 / 1.905
print('C YRD13', u13, 'JJJ13', j13, 'ratio', u13 / j13)
print('D mid female share', 3535.0 / 9309.2)
