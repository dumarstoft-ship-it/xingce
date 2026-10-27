# MK2728X-M2: 跨区域人员流动量 (cumulative, 万人次)
cross = {2:1171807,3:1671682,4:2189330,5:2736268,6:3241011,7:3799308,8:4396867,9:4909109,10:5492663,11:5972154,12:6459234}
cross_g = {3:10.2,4:8.4,5:8.3,6:7.4,7:6.6,8:6.1,9:5.4,10:5.5,11:5.4,12:5.4}
road = {2:1086652,3:1547451,4:2021233,5:2523351,6:2983967,7:3489943,8:4029157,9:4499504,10:5036908,11:5478704,12:5929002}
road_g = {2:10.3,3:9.0,4:7.4,5:7.4,6:6.6,7:5.8,8:5.4,9:4.7,10:4.9,11:4.8,12:4.8}
c25 = {2:(1229386,4.9),3:(1738829,4.0)}
r25 = {2:(1139263,4.8),3:(1607309,3.9)}
# Q1 quarters
q = [cross[3], cross[6]-cross[3], cross[9]-cross[6], cross[12]-cross[9]]
print("Q1 quarters:", q, "min Q%d" % (q.index(min(q))+1))
# Q2 2023 Q1 non-road share
c23 = cross[3]/1.102; r23 = road[3]/1.09
print("Q2 c23=%.1f r23=%.1f nonroad=%.1f share=%.4f%%" % (c23, r23, c23-r23, (c23-r23)/c23*100))
# Q3 2025Q1 road vs 2023Q1
print("Q3 compound=%.4f%% ; via values=%.4f%%" % (((1.039*1.09)-1)*100, (r25[3][0]/(road[3]/1.09)-1)*100))
print("Q3 check 2025/2024 =%.4f%%" % ((r25[3][0]/road[3]-1)*100))
# Q4 H2 highest cumulative growth month -> July; road MoM in July
for m in range(7,13): print("Q4 cum growth 1-%d: %.1f" % (m, cross_g[m]))
jul = road[7]-road[6]; jun = road[6]-road[5]
print("Q4 jul=%d jun=%d mom=%.4f%%" % (jul, jun, (jul/jun-1)*100))
# Q5
inc = road[12]*0.048/1.048
print("Q5A increment=%.1f 万人次 = %.3f 亿人次" % (inc, inc/1e4))
prev_base = None
base = {m: road[m]/(1+road_g[m]/100) for m in road}
for m in range(3,13):
    cur = road[m]-road[m-1]; b = base[m]-base[m-1]
    print("Q5B month %d 2024=%d 2023=%.0f growth=%.3f%%" % (m, cur, b, (cur/b-1)*100))
# rounding-robust check for September
lo = None
w8b = road[8]; w9 = road[9]
import itertools
vals = []
for g8 in [5.35,5.4,5.4499]:
    for g9 in [4.65,4.7,4.7499]:
        b8 = road[8]/(1+g8/100); b9 = road[9]/(1+g9/100)
        vals.append(((road[9]-road[8])/(b9-b8)-1)*100)
print("Q5B Sept growth range under rounding: %.3f%% to %.3f%%" % (min(vals), max(vals)))
print("Q5C H1 nonroad share=%.4f%%" % ((cross[6]-road[6])/cross[6]*100))
print("Q5D annual=%.1f 万人次 = %.3f 亿人次" % (c25[3][0]/3*12, c25[3][0]/3*12/1e4))
