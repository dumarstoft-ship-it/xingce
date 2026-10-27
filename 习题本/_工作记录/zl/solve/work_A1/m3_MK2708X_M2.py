# MK2708X-M2 纺织服装 2023
print('Q1: 2021 garment output')
p23 = 193.9
g23 = -0.0869
g22 = -(0.0869 - 0.0533)   # 降幅比2022年扩大5.33个百分点 -> 2022降幅3.36%
p22 = p23 / (1 + g23)
p21 = p22 / (1 + g22)
print('  g22 =', g22, ' p22 =', p22, ' p21 =', p21)

print('Q2: 2022 growth difference')
a22 = 12.9 - 19.4   # 服装鞋帽、针纺织品类
b22 = 10.8 - 7.3    # 穿类商品网上零售额
print('  a22 =', a22, ' b22 =', b22, ' diff =', a22 - b22)

print('Q3: textile yarn export growth')
tot23, gt = 2936.4, -0.081
clo23, gc = 1591.4, -0.078
tex23 = 1345.0
tot22 = tot23 / (1 + gt)
clo22 = clo23 / (1 + gc)
tex22 = tot22 - clo22
print('  tot22 =', tot22, ' clo22 =', clo22, ' tex22 =', tex22, ' growth =', tex23 / tex22 - 1)
print('  check 1345+1591.4 =', tex23 + clo23)

print('Q4: 2022 profit margin')
rev23, gr = 47009, -0.008
pro23, gp = 1802, 0.072
m22 = (pro23 / (1 + gp)) / (rev23 / (1 + gr))
print('  margin22 =', m22, ' margin23 =', pro23 / rev23)
print('  m23*(1+gr)/(1+gp) =', pro23 / rev23 * (1 + gr) / (1 + gp))

print('Q5')
print('  (1) Dec 2023 +2.6%, "重新恢复单月正增长" -> Nov negative growth')
dec23 = 253.0
jn23 = tot23 - dec23
jn22 = tot22 - dec23 / 1.026
print('      Jan-Nov 2023 cumulative growth =', jn23 / jn22 - 1)
print('  (2) 服装类 2022 growth =', 15.4 - 23.1, '%')
print('  (3) 1345.0/12 =', tex23 / 12, ' (unit: 亿美元, statement says 亿元)')
