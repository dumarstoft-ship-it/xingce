# MK2711X-M2 baijiu
# Q1
g=(1+0.0452)*(1+0.1039)-1
print("Q1 moutai liquor revenue growth", g)
# check: 2022 moutai liquor revenue
print("   moutai liquor rev 2022 (亿元)", 3.79*284.52, " series", 3.03*52.60)
# Q2
q123_21=557.8/1.122; full21=557.8+104.3
print("Q2 2021 Q1-3",q123_21,"full",full21,"Q4",full21-q123_21)
# Q3
r21=3042.69*0.7942; r20=2566.91*0.8066
print("Q3 2021",r21,"2020",r20,"diff",r21-r20)
# Q4
m22=2201.72/6626.45
p21=2201.72/1.2936; s21=6626.45/1.0964; m21=p21/s21
print("Q4 margin22",m22,"margin21",m21,"diff pp",(m22-m21)*100, " formula", m22*(0.2936-0.0964)/1.2936*100)
# Q5
vol21=3.03/1.0146; rev21=vol21*41
print("Q5A 2021 series vol",vol21,"rev(亿元)",rev21, " alt via 2022 price/1.2829:", vol21*52.60/1.2829)
print("Q5B avg loss per loss firm (万元)", 18.82e4/169)
print("Q5C i-moutai share", 118.83/1275.54)
print("Q5D 2021 output", 671.24/(1-0.0558))
print("   check loss ratio", 169/963)
