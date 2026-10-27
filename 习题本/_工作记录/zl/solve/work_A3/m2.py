# MK2735D-M2 power generation 2023
months = ['1-2','3','4','5','6','7','8','9','10','11','12']
daily = [228.8,231.4,219.5,222.1,246.6,273.0,272.6,248.5,227.2,243.7,267.4]
yoy = [0.7,5.1,6.1,5.6,2.8,3.6,1.1,7.7,5.2,8.4,8.0]  # dec2022 = 3.0
days = [59,31,30,31,30,31,31,30,31,30,31]
total = 89090
tot = [d*n for d,n in zip(daily,days)]
for m,t in zip(months,tot): print(m, round(t,1))
print("sum of monthly totals =", sum(tot), " vs 89090")
print("Q1: Dec share =", tot[-1]/total, " (30-day trap", 267.4*30/total, ")")
print("Q2: Jun - May =", tot[4]-tot[3], " trap (diff*30)=", (246.6-222.1)*30, " (diff*31)=", (246.6-222.1)*31)
d22 = 267.4/1.08
d21 = d22/1.03
print("Q3: Dec2022 daily =", d22, " Dec2021 daily =", d21)
avg = total/12
print("Q4: monthly avg =", avg)
for m,t in zip(months[5:],tot[5:]): print("   ", m, round(t,1), "<=avg" if t<=avg else ">avg")
print("Q5A: thermal share =", 62318/total, " 70% of total =", 0.7*total)
print("Q5B: daily QoQ Jul-Oct:", [round(daily[i]-daily[i-1],1) for i in range(5,9)], " yoy change:", [round(yoy[i]-yoy[i-1],1) for i in range(5,9)])
ups = [months[i] for i in range(1,11) if daily[i]>daily[i-1]]
print("Q5C: QoQ up months (from Mar):", ups, len(ups), " ; 1-2 avg vs Dec2022:", 228.8, d22)
# Jan/Feb possibilities
janfeb = 228.8*59
print("   if Jan daily = Dec22 daily, Feb daily =", (janfeb - d22*31)/28)
hy22 = 11409/(1-0.056)
print("Q5D: hydro 2022 =", hy22, " decrease =", hy22-11409)
