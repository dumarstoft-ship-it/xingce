# MK2740X-M1
# Q1 growth rates
items = {'建筑':(9089,597),'安装':(583,97),'机电':(321,34),'其他':(2003,375)}
for k,(c,d) in items.items():
    print(k, c-d, d/(c-d)*100)
# Q2
tot_b = 11996/1.101
small_b = 9009/1.031
large_b = tot_b - small_b
print('Q2 total base', tot_b, 'small base', small_b, 'large base', large_b, 'growth', (2987/large_b-1)*100)
# check 2987+9009
print(2987+9009)
# Q3
print('Q3', ((1-0.105)/(1-0.134)-1)*100)
# Q4
print('Q4', 27925*(1.115**2-1), 27925*1.115**2, 27925*0.115, 27925*1.115*0.115)
# Q5
vals = [3227,5665,2079,1025]
s=sum(vals); print('sum', s)
for v in vals: print(v, v/11996*100, v/11996*360)
