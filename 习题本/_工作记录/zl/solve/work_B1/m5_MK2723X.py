# MK2723X-M3 H province 2023
print("Q1: 2022 summer grain share")
s22 = 1498.6/1.008; t22 = 3809.9/(1-0.014)
print('  summer22', s22, ' total22', t22, ' share', s22/t22*100, ' (2023 share', 1498.6/3809.9*100, ')')
print('  formula: 39.33% * (1-1.4%)/(1+0.8%) =', 1498.6/3809.9*(1-0.014)/1.008*100)
print("Q2: 2022 growth rates")
tot22 = 6.9-1.4; man22 = 6.4-2.4; min22 = 13.0+4.5; ele22 = 5.8+1.9
print('  total', tot22, ' manuf', man22, ' mining', min22, ' elec', ele22)
print("Q3: 2023 change amounts (万吨)")
for name, v, g in [('grain',3809.9,-0.014),('meat',491.1,0.033),('egg',404.6,0.016),('milk',571.9,0.046)]:
    print('  ', name, v*g/(1+g))
print("Q4: 2021 GDP")
g22 = 0.055-0.017
print('  2022 growth', g22, ' 2021 GDP', 43944.1/(1.055*(1+g22)))
print("Q5: 2023 industry shares")
T = 43944.1
for n, v in [('1st',4466.2),('2nd',16435.3),('3rd',23042.6)]:
    print('  ', n, v/T*100, 'deg', v/T*360)
print('  sum of parts', 4466.2+16435.3+23042.6)
