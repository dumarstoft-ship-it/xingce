# MK26ZX-M2 Zhejiang per-100-household holdings
# item: (all23, all22, urb23, urb22, rur23, rur22)
T = {
 '空调': (220.2, 218.8, 238.5, 236.4, 181.8, 184.3),
 '空气净化器': (12.1, 8.8, 15.7, 11.3, 4.6, 4.0),
 '烤箱': (11.4, 6.3, 12.4, 6.5, 9.5, 5.9),
 '洗碗机': (7.3, 4.6, 9.5, 5.8, 2.5, 2.2),
 '地面清洁电器': (23.0, 17.7, 29.6, 22.8, 9.3, 7.8),
 '照相机': (12.3, 11.9, 16.4, 15.7, 3.7, 4.4),
 '乐器': (8.7, 7.4, 11.3, 10.3, 3.2, 1.8),
 '健身器材': (9.1, 8.1, 11.0, 10.7, 5.1, 3.1),
 '家用汽车': (64.7, 55.5, 72.2, 64.4, 43.9, 38.1),
 '新能源汽车': (4.1, 1.4, 4.3, 1.6, 3.6, 1.0),
}
print('== Q1 urban enjoyment goods growth')
for k in ['空气净化器', '烤箱', '洗碗机', '地面清洁电器']:
    print(k, T[k][2] / T[k][3] - 1)
print('== Q2 rural NEV share of cars')
s23 = 3.6 / 43.9; s22 = 1.0 / 38.1
print(s23, s22, 'pp change', (s23 - s22) * 100)
print('== Q3 urban instruments total growth with households +5.3%')
g = 11.3 / 10.3 - 1
print('per100 growth', g, 'total growth', (1 + g) * 1.053 - 1)
print('== Q4 changes')
print('A rural AC', 181.8 - 184.3, 'B rural camera', 3.7 - 4.4, 'C urban camera', 16.4 - 15.7, 'D urban AC', 238.5 - 236.4)
print('== Q5')
print('(1) urban/rural household ratio implied by weighted average, by item (2023, 2022):')
for k, (a23, a22, u23, u22, r23, r22) in T.items():
    print('  ', k, round((a23 - r23) / (u23 - a23), 3) if u23 != a23 else None, round((a22 - r22) / (u22 - a22), 3) if u22 != a22 else None)
print('(2) 2022 urban floor cleaner + car per 100:', 22.8 + 64.4, ' min overlap if <=1 each:', max(0, 22.8 + 64.4 - 100))
print('(3) rural NEV per100 ratio', 3.6 / 1.0, 'increase multiple', 3.6 / 1.0 - 1)
