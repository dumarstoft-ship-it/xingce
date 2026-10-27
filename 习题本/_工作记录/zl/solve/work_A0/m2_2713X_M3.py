# MK2713X-M3 党内统计公报
print("Q1")
org=517.6; g=0.022
print("increase", org*g/(1+g), "base", org/(1+g))
print("sum of org components", 29.8+32.5+455.4)

print("Q2")
ages=[1241.2,1119.6,1086.4,945.9,907.1,940.5,890.7,2787.2]
total=9918.5
print("sum ages", sum(ages))
ge56=890.7+2787.2; lt56=sum(ages[:6])
print("ge56", ge56, "lt56", lt56, "lt56 by total", total-ge56)
print("fewer pct (vs lt56)", (lt56-ge56)/lt56*100, "(vs ge56)", (lt56-ge56)/ge56*100)
print("using total-ge56:", (total-ge56-ge56)/(total-ge56)*100)

print("Q3")
dev_total=110.5/0.459
occ=[15.8,37.5,35.1,26.7,11.9,91.9,21.8]
print("dev total from female share", dev_total, "sum occ", sum(occ))
print("minority share", 25.2/dev_total*100, "using occ sum", 25.2/sum(occ)*100)

print("Q4")
print("min male college share", 56.2+(100-30.4)-100)
print("by numbers:", (5578.6+(total-3018.5)-total)/total*100)

print("Q5")
print("A", 1619.0/35.1)
inc23=114.4; inc22=114.4+18.5
e22=total-inc23; e21=e22-inc22
print("B: end2022", e22, "net inc 2022", inc22, "end2021", e21, "wrong-trap", e22-(114.4-18.5))
male=total-3018.5
print("C: male", male, "male/female", male/3018.5, "more by", male/3018.5-1)
print("D", 2611.2/total*100)
print("join-time sum", 6.8+1286.3+6014.2+2611.2)
