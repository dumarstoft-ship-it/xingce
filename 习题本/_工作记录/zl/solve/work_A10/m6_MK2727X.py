# MK2727X-M3 aquatic products import/export 2022.6-2023.5
months = ["2022.6","2022.7","2022.8","2022.9","2022.10","2022.11","2022.12","2023.1","2023.2","2023.3","2023.4","2023.5"]
imq = [39,43,42,37,38,45,45,28,33,48,52,47]
imq_g = [17.0,24.0,18.5,50.3,25.2,19.8,9.6,-23.8,32.0,54.2,57.9,23.9]
imv = [101,126,128,130,130,140,134,97,95,129,128,136]
imv_g = [32.8,60.6,56.3,8.3,48.9,42.8,23.2,-9.9,28.2,61.4,59.0,39.9]
exq = [31,32,30,31,32,33,34,30,23,32,30,33]
exq_g = [4.2,8.8,-2.9,-9.5,-7.7,-12.6,-1.1,-22.0,33.0,17.0,-1.5,-6.4]
exv = [133,130,121,121,130,137,143,116,87,128,118,122]
exv_g = [19.7,18.7,5.9,-6.4,-0.5,-2.9,1.6,-23.8,35.0,16.4,-3.6,-14.6]

# Q1: 2022 H2 = Jul-Dec (index 1..6)
im_h2 = sum(imv[1:7]); ex_h2 = sum(exv[1:7])
print("Q1 H2 import", im_h2, "export", ex_h2, "balance", ex_h2 - im_h2)
print("Q1 (trap incl June) import", sum(imv[0:7]), "export", sum(exv[0:7]))

# Q2: 2023 Jan-May import unit price (万元/吨)
cnt = 0
for i in range(7, 12):
    p = imv[i]/imq[i]
    cnt += p > 3
    print("Q2", months[i], round(p, 4))
print("Q2 count >3", cnt)

# Q3: 2022 Jan-May import values from 2023 growth
cum = 0
for i, m in zip(range(7, 12), ["2022.1","2022.2","2022.3","2022.4","2022.5"]):
    v = imv[i]/(1+imv_g[i]/100)
    cum += v
    print("Q3", m, round(v, 2), "cum", round(cum, 2))
print("Q3 2022.6", imv[0], "cum", cum + imv[0])

# Q4: export unit price vs last year
cnt = 0
for i in range(12):
    cur = exv[i]/exq[i]
    prev = (exv[i]/(1+exv_g[i]/100))/(exq[i]/(1+exq_g[i]/100))
    low = cur < prev
    cnt += low
    print("Q4", months[i], "price", round(cur, 4), "prev", round(prev, 4), "lower", low, "(value g", exv_g[i], "qty g", exq_g[i], ")")
print("Q4 count", cnt)

# Q5: 2023 Q1 export value mom growth
mom = [(exv[7]/exv[6]-1)*100, (exv[8]/exv[7]-1)*100, (exv[9]/exv[8]-1)*100]
print("Q5 mom Jan, Feb, Mar (%)", [round(x, 2) for x in mom], "diffs", round(mom[1]-mom[0], 2), round(mom[2]-mom[1], 2))
