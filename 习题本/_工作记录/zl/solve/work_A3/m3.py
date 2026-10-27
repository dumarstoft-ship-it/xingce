# MK2719X-M2 S province electricity
m = [6,7,8,9,10,11,12]
tot = [224.5,248.1,248.0,223.7,231.1,250.0,283.1]
g = [-1.1,7.3,6.3,4.3,9.0,13.3,7.6]
cum = [1036.2,1215.1,1396.0,1566.2,1742.2,1925.0,2122.4]
cg = [3.6,3.6,3.8,3.6,4.1,4.7,4.8]
# Q1
h2 = tot[1:]
print("Q1: H2 sum =", sum(h2), " avg =", sum(h2)/6, " (7-month trap:", sum(tot)/7, ")")
# Q2
prev = [t/(1+x/100) for t,x in zip(tot,g)]
cnt = 0
for i in range(1,7):
    q23 = tot[i]/tot[i-1]-1
    q22 = prev[i]/prev[i-1]-1
    flag = q23 > q22
    cnt += flag
    print(f"Q2: {m[i]}月 2023 MoM={q23*100:.2f}%  2022 MoM={q22*100:.2f}%  higher={flag}  (yoy {g[i-1]}->{g[i]})")
print("Q2 count =", cnt)
# Q3
c22 = [c/(1+x/100) for c,x in zip(cum,cg)]
q4_22 = c22[6]-c22[3]
q3_22 = c22[3]-c22[0]
print("Q3: 2022 cum Jun/Sep/Dec =", c22[0], c22[3], c22[6])
print("    2022Q3 =", q3_22, " 2022Q4 =", q4_22, " QoQ =", q4_22/q3_22-1)
q4_23 = cum[6]-cum[3]; q3_23 = cum[3]-cum[0]
print("    (2023Q3 =", q3_23, " 2023Q4 =", q4_23, " QoQ =", q4_23/q3_23-1, ")")
# Q4
ind23 = [cum[i]-cum[i-1] for i in range(1,7)]
ind22 = [c22[i]-c22[i-1] for i in range(1,7)]
for i in range(6):
    print(f"Q4: {m[i+1]}月 ind23={ind23[i]:.1f} ind22={ind22[i]:.2f} yoy={(ind23[i]/ind22[i]-1)*100:.2f}%")
# Q5
ratios = [a/b for a,b in zip(ind23, tot[1:])]
for i in range(6):
    print(f"Q5: {m[i+1]}月 share = {ratios[i]*100:.2f}%")
print("    diffs:", [round((ratios[i]-ratios[i-1])*100,2) for i in range(1,6)])
