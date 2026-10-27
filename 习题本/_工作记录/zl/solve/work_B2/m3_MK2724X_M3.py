# MK2724X-M3 hydrogen fuel cell vehicles
tot23 = 7760; g = 0.55
print("Q1 increase", tot23*g/(1+g))
dec = 2260; nov = dec/(1+1.875)
print("Q2 Nov", nov, "1-10 sum", tot23-dec-nov, "avg", (tot23-dec-nov)/10)
types = {'重卡':(3643,47.8,47,-2.2),'轻卡':(2104,161,27.1,10.95),'客车':(1240,-1.6,16,-9.15),'乘用车':(538,137,6.9,2.35),'中卡':(235,-5.2,3,-1.95)}
tot22 = tot23/(1+g)
print("Q3 2022 total", tot22)
res=[]
for k,(v,gr,sh,chg) in types.items():
    b = v/(1+gr/100)
    res.append((k, round(sh-chg,2), round(b,1), round(b/tot22*100,2)))
for r in sorted(res,key=lambda x:-x[1]): print(r)
hk22 = 3643/1.478
print("Q4 2022 heavy", hk22, "2021", hk22/(1+2.164))
sub = {'牵引车':(1326,253.6),'自卸车':(492,44.7),'其他':(595,829.6)}
s21 = 0
for k,(v,gr) in sub.items():
    b=v/(1+gr/100); s21+=b; print(k, round(b,2))
print("sum 2022 subtypes", 1326+492+52+595, "sum 2021 subtypes (搅拌车=0)", s21)
print("Q5")
print("① 2025 light trucks", 2104*(1+1.61)**2)
avg111 = (hk22-779)/11
print("② 1-11 avg", avg111, "ratio", 779/avg111, "多几倍", 779/avg111-1)
avg111b = (2465-779)/11
print("   with 2465:", avg111b, 779/avg111b)
print("③ 2021 tractor/dump", (1326/3.536)/(492/1.447), "2022 ratio", 1326/492)
