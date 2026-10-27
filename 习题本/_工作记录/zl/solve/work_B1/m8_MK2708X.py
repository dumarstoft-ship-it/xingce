# MK2708X-M2 textile & apparel 2023
print("Q1: 2021 apparel output")
g23 = -0.0869; g22 = -(8.69-5.33)/100
print('  2022 growth', g22, ' 2022 output', 193.9/(1+g23), ' 2021 output', 193.9/(1+g23)/(1+g22))
print("Q2: 2022 growth rates")
a = 12.9-19.4; b = 10.8-7.3
print('  限上服装鞋帽针纺 2022', a, ' 穿类网上 2022', b, ' diff', a-b)
print("Q3: textile yarn/fabric export growth 2023")
tot22 = 2936.4/(1-0.081); app22 = 1591.4/(1-0.078); tex22 = tot22-app22
print('  tot22', tot22, ' app22', app22, ' tex22', tex22, ' growth', (1345.0/tex22-1)*100)
print('  check parts sum', 1345.0+1591.4)
print("Q4: 2022 textile profit margin")
r22 = 47009/(1-0.008); p22 = 1802/1.072
print('  rev22', r22, ' prof22', p22, ' margin22', p22/r22*100, ' (2023 margin', 1802/47009*100, ')')
print('  formula 3.833% * 0.992/1.072 =', 1802/47009*0.992/1.072*100)
print("Q5")
print('  (2) 2022 限上服装类 growth', 15.4-23.1)
print('  (3) 1345.0/12 =', 1345.0/12, '亿美元 (statement says 亿元)')
