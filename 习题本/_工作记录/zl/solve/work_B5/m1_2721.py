# MK2721X-M1
# Q1
print("Q1 2022:", 829.6/1.038)
# Q2 mixed average
a_over_b = (811.4-706.4)/(866.6-811.4)
print("Q2 ratio min/other:", a_over_b, "->", a_over_b*10, ":10")
# Q3
r_dg = 390.8-96.9
print("Q3 daigong return rate:", r_dg, "% ; spend:", 462.1/(1+r_dg/100))
# also self brand spend for reference
print("   self brand spend:", 1067.1/(1+390.8/100))
# Q4
spend_all = 266.9/1.416
print("Q4 spend overall:", spend_all, " rate:", (829.6-spend_all)/spend_all*100)
for opt,v in zip("ABCD",[269.2,307.4,340.1,386.5]):
    print("  opt",opt,v)
# Q5
print("Q5 A:", (866.6/811.4-1)*100)
print("Q5 B:", 1067.1/462.1)
print("Q5 C:", 829.6*1.245)
