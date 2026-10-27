# MK2702X-M1 textile & apparel
print("Q1: 2022 Q3 textile profit")
p9 = 1026/(1-0.088); p6 = 595/(1-0.213)
print('  2022 Q1-3', p9, ' 2022 H1', p6, ' Q3', p9-p6)
print("Q2: export change ratio 9M vs H1")
d9 = 2232*(-0.095)/(1-0.095); d6 = 1427*(-0.083)/(1-0.083)
print('  9M change', d9, ' H1 change', d6, ' ratio', d9/d6)
print("Q3: 2022 apparel profit growth")
print('  margin method 0.954*5.3/5.4-1 =', (0.954*5.3/5.4-1)*100)
rev21 = 14539/(1-0.046)
print('  rev21', rev21, ' profit21 @5.4%', rev21*0.054, ' growth', (764/(rev21*0.054)-1)*100)
print('  actual 2022 margin 764/14539 =', 764/14539*100)
print('  with 5.25/5.35:', (0.954*5.25/5.35-1)*100)
print("Q4: 2022 H2 apparel margin")
r = 14539-6885; p = 764-307
print('  rev', r, ' profit', p, ' margin', p/r*100)
print("Q5")
# A: Q3 value-added growth; weights unknown; if H1:Q3 base weight = w:1
for w in [1, 1.5, 2, 2.5]:
    rq3 = (-2.2*(w+1) - (-3.0)*w)
    print('  A: weight H1:Q3 =', w, ': Q3 growth', rq3)
print('  B: Aug decline =', 4.8+3.6)
print('  C: 1551*1.064 =', 1551*1.064)
print('  D: 13067*27% =', 13067*0.27)
