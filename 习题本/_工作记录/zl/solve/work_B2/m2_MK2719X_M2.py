# MK2719X-M2 S province electricity
months = [6,7,8,9,10,11,12]
tot = dict(zip(months,[224.5,248.1,248.0,223.7,231.1,250.0,283.1]))
totg = dict(zip(months,[-1.1,7.3,6.3,4.3,9.0,13.3,7.6]))
cum = dict(zip(months,[1036.2,1215.1,1396.0,1566.2,1742.2,1925.0,2122.4]))
cumg = dict(zip(months,[3.6,3.6,3.8,3.6,4.1,4.7,4.8]))
print("Q1 H2 avg", sum(tot[m] for m in range(7,13)), sum(tot[m] for m in range(7,13))/6)
print("Q2 mom growth this year vs last year")
cnt=0
for m in range(7,13):
    this = tot[m]/tot[m-1]-1
    last = (tot[m]/(1+totg[m]/100))/(tot[m-1]/(1+totg[m-1]/100))-1
    print(m, round(this*100,2), round(last*100,2), this>last)
    cnt += this>last
print("count", cnt)
print("Q3 2022 Q4 industrial mom")
c22 = {m: cum[m]/(1+cumg[m]/100) for m in months}
q4_22 = c22[12]-c22[9]; q3_22 = c22[9]-c22[6]
print("2022 Q4", q4_22, "2022 Q3", q3_22, "mom", (q4_22/q3_22-1)*100)
print("Q4 monthly industrial yoy")
for m in range(7,13):
    m23 = cum[m]-cum[m-1]; m22 = c22[m]-c22[m-1]
    print(m, round(m23,1), round(m22,2), round((m23/m22-1)*100,2))
print("Q5 share")
for m in range(7,13):
    ind = cum[m]-cum[m-1]
    print(m, round(ind,1), tot[m], round(ind/tot[m]*100,2))
