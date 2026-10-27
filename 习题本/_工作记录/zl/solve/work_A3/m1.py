# MK2710X-M1 Baidu
rd = [32.9,40.3,39.2,45.3,41.7,47.3,46.9,47.6,44.4]
yoy = [16.2,28.1,20.8,22.3,26.7,17.4,19.6,5.1,6.5]
ratio = [15.8,15.5,13.9,16.7,17.3,18.0,16.7,16.5,19.7]
labels = ['18Q1','18Q2','18Q3','18Q4','19Q1','19Q2','19Q3','19Q4','20Q1']
print("Q1: sum 2018-2019 =", sum(rd[:8]), " /24 =", sum(rd[:8])/24)
# Q2
net19 = 142/(1-0.19)
other19 = 83/1.28
tot19_a = 41.7/0.173
tot19_b = net19 + other19
print("Q2: net19 =", net19, " tot19 via ratio =", tot19_a, " share =", net19/tot19_a)
print("    tot19 via parts =", tot19_b, " share =", net19/tot19_b)
print("    tot20 via ratio =", 44.4/0.197)
# Q3
g = 44.4/47.6 - 1
print("Q3: QoQ g =", g, " Q2 est =", 44.4*(1+g))
# Q4
import itertools
pairs = sorted(((abs(ratio[i]-ratio[j]), labels[i], labels[j], rd[i], rd[j]) for i,j in itertools.combinations(range(9),2)))
for p in pairs[:4]:
    print("Q4:", p, " rd diff =", round(abs(p[3]-p[4]),2))
# Q5
print("Q5A: 2019Q1 SGA =", 39/(1-0.36))
for i in range(4):
    print("Q5B:", labels[i], "total rev =", rd[i]/(ratio[i]/100))
print("Q5C: base =", 65-41.3, " growth =", 41.3/(65-41.3))
print("Q5D: 2018 =", sum(rd[:4]), " 2019 =", sum(rd[4:8]), " 2020Q1 only =", rd[8])
