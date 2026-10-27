# MK2726X-M3 third-party payments
tot_inc = 63.6*0.164/1.164; on_inc = 32.2*0.167/1.167
print("Q1 total inc", tot_inc, "online inc", on_inc, "offline inc", tot_inc-on_inc)
print("   check offline 2022", 63.6/1.164-32.2/1.167, "growth", (31.4/(63.6/1.164-32.2/1.167)-1)*100)
t22 = 544.7/1.11; p22 = 345.4/1.124; e22 = t22-p22
print("Q2 method1 ent 2022", e22, "growth", (199.3/e22-1)*100)
e23 = 82.7+113.9+2.7; inc = -0.7+16.2+0.5
print("   method2 sum", e23, "inc", inc, "growth", inc/(e23-inc)*100)
s23 = 32.2/63.6; s22 = (32.2/1.167)/(63.6/1.164)
print("Q3 share 2023", s23*100, "2022", s22*100, "diff pp", (s23-s22)*100)
inc_n = 5451.7*0.203/1.203
print("Q4 increase", inc_n)
v = 5451.7; y = 2023
while v <= 8000:
    v += inc_n; y += 1
    print("  ", y, round(v,1))
print("Q5 ① 2022 online-offline", 32.2/1.167 - (63.6/1.164-32.2/1.167))
print("   ② 2021 count", 5451.7/1.203/(1+0.203-0.162))
print("   ③ 2022 ratio", (113.9-16.2)/(82.7+0.7))
print("   ④ 2022 per-transaction (万亿元/亿笔)", (63.6/1.164)/(5451.7/1.203))
