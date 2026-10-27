yrs = list(range(2015,2024))
ppl = dict(zip(yrs,[39.9,44.4,50.0,55.4,60.1,28.8,32.5,25.3,48.9]))
spd = dict(zip(yrs,[3.4,3.9,4.6,5.1,5.7,2.2,2.9,2.0,4.9]))
print("Q1 growth via text", (2.403/1.933-1)*100)
print("Q1 via chart", spd[2023]/ppl[2023]*1e4, spd[2022]/ppl[2022]*1e4, (spd[2023]/ppl[2023])/(spd[2022]/ppl[2022])-1)
print("Q2")
u22 = 4.2/2.475; r22 = 0.7/2.064
print(u22, r22, u22/r22, u22/r22-1)
print("Q3")
u23_avg = 4.2e12/37.6e8
u22_avg = (4.2e12/2.475)/(37.6e8/1.949)
print(u23_avg, u22_avg, u23_avg-u22_avg)
print("Q4")
for y in range(2018,2024):
    print(y, (spd[y]/spd[y-1]-1)*100)
print("Q5")
print("A", 37.4e8/56275, "元")
tot22 = 48.9/1.933; urb22 = 37.6/1.949
print("B rural share 2022", (tot22-urb22)/tot22, "2023", (48.9-37.6)/48.9)
s = sum(ppl[y] for y in range(2016,2021))
print("C", s, s/60)
for y in range(2018,2023):
    print("D", y, spd[y], round(spd[y]-spd[y-1],2))
