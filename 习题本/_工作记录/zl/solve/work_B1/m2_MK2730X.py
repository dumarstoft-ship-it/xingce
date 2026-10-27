# MK2730X-M3 electricity 2022 1-9
tot, gtot = 64931, 0.04
west, ne = 18685, 3328
ge, gc = 0.025, 0.084
s21 = dict(E=47.5, C=18.5, W=28.7, NE=5.3)
s22 = dict(E=46.8, C=19.3, W=28.8, NE=5.1)
tot21 = tot/(1+gtot)
print("Q1: east 2021")
print(' via 2022 share/1.025:', tot*s22['E']/100/(1+ge))
print(' via 2021 total*47.5%:', tot21*s21['E']/100)
print("Q2: west growth")
print(' 18685 / (tot21*28.7%) -1:', (west/(tot21*s21['W']/100)-1)*100)
print(' (1.04*28.8/28.7)-1:', (1.04*s22['W']/s21['W']-1)*100)
print(' check west share 2022:', west/tot*100, ' NE share', ne/tot*100)
print("Q3: residential 2021 growth: 1.214/1.135-1 =", (1.214/1.135-1)*100)
print("Q4: hi-tech share of manufacturing")
A, a = 6793, 0.023; B, b = 31580, 0.006
sh22 = A/B; sh21 = (A/(1+a))/(B/(1+b))
print(' share22', sh22*100, 'share21', sh21*100, 'diff pp', (sh22-sh21)*100, ' formula', sh22*(a-b)/(1+a)*100)
print("Q5")
print(' (1) 2021 shares order:', sorted(s21.items(), key=lambda x:-x[1]))
t3, g3 = 11379, 0.049
inc3 = t3*g3/(1+g3); inctot = tot*gtot/(1+gtot)
print(' (2) tertiary inc', inc3, 'total inc', inctot, 'contrib %', inc3/inctot*100)
print(' (3) 17163/4121 =', 17163/4121, ' 多 =', 17163/4121-1, '倍')
