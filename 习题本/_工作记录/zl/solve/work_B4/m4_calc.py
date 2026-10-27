# MK2730X-M1 air conditioner cumulative production
cum22 = {8:15722, 9:17492, 10:18960, 11:20449, 12:22247}
g22 = {8:1.9, 9:3.5, 10:3.2, 11:2.0, 12:1.8}
cum23 = {2:3331, 3:6260, 4:8870, 5:11425, 6:14060, 7:16348}
g23 = {2:10.8, 3:12.6, 4:12.2, 5:14.2, 6:16.6, 7:17.9}
h1_22 = cum23[6]/(1+g23[6]/100)
print('Q1 H1 2022', h1_22, 'H2', cum22[12]-h1_22)
sep = cum22[9]-cum22[8]; octo = cum22[10]-cum22[9]; nov = cum22[11]-cum22[10]; dec = cum22[12]-cum22[11]
print('Q2 monthly', sep, octo, nov, dec, 'oct mom', octo/sep-1)
jun23 = cum23[6]-cum23[5]; may22c = cum23[5]/(1+g23[5]/100); jun22 = h1_22 - may22c
print('Q3', jun23, may22c, jun22, jun23/jun22-1)
print('Q4', (1-0.154)/(1+0.013)-1)
print('Q5 MoM increments', octo-sep, nov-octo, dec-nov)
# cross-check July 2023 yoy 29%
jul22 = cum23[7]/(1+g23[7]/100) - h1_22; jul23 = cum23[7]-cum23[6]
print('check Jul', jul23, jul22, jul23/jul22-1)
