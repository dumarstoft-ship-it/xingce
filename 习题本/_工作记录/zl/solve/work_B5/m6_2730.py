# MK2730X-M2
rev={2:2463,3:3840,4:5547,5:6861,6:8676}
pro={2:169.7,3:278.9,4:384.9,5:521.4,6:743.7}
pg={2:6.5,3:-15.3,4:-19.7,5:-12.8,6:1.9}
rg24={2:7.6,3:8.4,4:3.7,5:5.0,6:5.6}
rg23={2:-3.9,3:1.6,4:3.3,5:2.8,6:2.6,7:2.8,8:2.6,9:3.4,10:5.9,11:6.1,12:6.8}
# Q1
r23q1=rev[3]/(1+rg24[3]/100); p23q1=pro[3]/(1+pg[3]/100)
print("Q1 rev23Q1",r23q1," pro23Q1",p23q1," margin%",p23q1/r23q1*100)
# Q2
cnt=[m for m in range(7,13) if rg23[m]>rg23[m-1]]
print("Q2 months with cum growth rising:", cnt, len(cnt))
# Q3
r23_14=rev[4]/(1+rg24[4]/100)
print("Q3 rev23 1-4:", r23_14, " increase:", r23_14*rg23[4]/(100+rg23[4]))
# Q4
east=rev[6]-408.8-525.4-20.8
print("Q4 east:", east, " share%:", east/rev[6]*100)
# Q5
for m in range(2,7):
    print("Q5 A period 1-%d: profit g %.1f vs rev g %.1f -> margin24 %.3f%% margin23 %.3f%%"%(m,pg[m],rg24[m],pro[m]/rev[m]*100,(pro[m]/(1+pg[m]/100))/(rev[m]/(1+rg24[m]/100))*100))
print("Q5 B Q2/Q1 profit:", (pro[6]-pro[3])/pro[3])
r23={m:rev[m]/(1+rg24[m]/100) for m in range(2,7)}
print("Q5 C 2023 Mar:", r23[3]-r23[2], " Apr:", r23[4]-r23[3])
g={"east":5.6-0.4,"central":5.6+6.4,"west":4.6,"ne":-2.1}
print("Q5 D growth:", g)
base_e=east/(1+g["east"]/100)
print("   east increase amount:", east-base_e, " central inc:", 408.8-408.8/1.12)
