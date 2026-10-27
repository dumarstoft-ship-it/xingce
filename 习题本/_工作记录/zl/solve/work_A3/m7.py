# MK2730X-M2 Internet business 2024H1
per = ['1-2','1-3','1-4','1-5','1-6']
rev = [2463,3840,5547,6861,8676]
prof = [169.7,278.9,384.9,521.4,743.7]
pg = [6.5,-15.3,-19.7,-12.8,1.9]
rg24 = [7.6,8.4,3.7,5.0,5.6]
rg23 = {'1-2':-3.9,'1-3':1.6,'1-4':3.3,'1-5':2.8,'1-6':2.6,'1-7':2.8,'1-8':2.6,'1-9':3.4,'1-10':5.9,'1-11':6.1,'1-12':6.8}
# Q1
r23 = 3840/1.084; p23 = 278.9/(1-0.153)
print("Q1: 2023Q1 rev =", r23, " profit =", p23, " margin =", p23/r23, " (2024 margin =", 278.9/3840, ")")
# Q2
keys = list(rg23.keys())
cnt=0
for i in range(5,11):
    up = rg23[keys[i]] > rg23[keys[i-1]]
    cnt += up
    print("Q2:", keys[i], rg23[keys[i-1]], "->", rg23[keys[i]], "month>cum" if up else ("month<cum" if rg23[keys[i]]<rg23[keys[i-1]] else "equal"))
print("Q2 count =", cnt)
# Q3
c23_14 = 5547/1.037
print("Q3: 2023 1-4 rev =", c23_14, " increment =", c23_14*0.033/1.033)
# Q4
east = 8676-408.8-525.4-20.8
print("Q4: east =", east, " share =", east/8676)
# Q5
for p,a,b in zip(per,pg,rg24):
    print("Q5A:", p, "profit g", a, " rev g", b, " margin falls" if (1+a/100)<(1+b/100) else " margin rises", " margin24 =", round(prof[per.index(p)]/rev[per.index(p)]*100,2), " margin23 =", round(prof[per.index(p)]/(1+a/100)/(rev[per.index(p)]/(1+b/100))*100,2))
q2p = 743.7-278.9
print("Q5B: Q2 profit =", q2p, " ratio Q2/Q1 =", q2p/278.9)
c23_12 = 2463/1.076; c23_13 = 3840/1.084
print("Q5C: 2023 Mar =", c23_13-c23_12, " Apr =", c23_14-c23_13)
nat = 5.6
print("Q5D: east", nat-0.4, " central", nat+6.4, " west 4.6  northeast -2.1")
inc = {'east': east*(nat-0.4)/(100+nat-0.4), 'central': 408.8*(nat+6.4)/(100+nat+6.4), 'west': 525.4*4.6/104.6, 'ne': 20.8*(-2.1)/97.9}
print("     increments:", {k: round(v,1) for k,v in inc.items()})
