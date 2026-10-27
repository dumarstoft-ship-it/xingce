# MK2723X-M2 export delivery value 2023
rows = [('纺织业',218.3,-3.1,2456.5,-10.6),('家具制造业',135.9,1.4,1366.6,-13.6),('化学纤维制造业',51.9,5.4,627.7,0.6),
('非金属矿物制品业',152.9,-0.1,1681.5,-5.4),('黑色金属冶炼和压延加工业',157.6,5.1,2025.6,4.2),('有色金属冶炼和压延加工业',129.0,0.9,1693.3,-8.9),
('金属制品业',388.3,3.7,4189.4,-12.0),('通用设备制造业',625.2,3.8,6678.3,-2.3),('专用设备制造业',534.2,5.4,5477.1,3.5),
('汽车制造业',739.8,17.3,8113.4,26.3),('电子机械和器材制造业',1359.1,-2.0,17026.7,2.8),('计算机通信电子',5727.4,-5.5,62390.8,-6.3)]
yes = []
for n,d,dg,c,cg in rows:
    avg = (c-d)/11
    print('Q1', n, d, round(avg,2), d > avg, 'd*12', round(d*12,1), c)
    if d > avg: yes.append(n)
print('Q1 count', len(yes))
r = rows[8]; c22 = r[3]/(1+r[4]/100); d22 = r[1]/(1+r[2]/100)
print('Q2', c22, d22, c22-d22)
top2 = sorted(rows, key=lambda x: -x[4])[:2]
incs = [x[3]*x[4]/(100+x[4]) for x in top2]
print('Q3', [x[0] for x in top2], incs, incs[0]/incs[1])
r = rows[9]; cur = r[3]-r[1]; base = r[3]/(1+r[4]/100) - r[1]/(1+r[2]/100)
print('Q4', cur, base, cur/base-1)
mind = min(rows, key=lambda x: x[2]); minc = min(rows, key=lambda x: x[4])
print('Q5-1 slowest Dec', mind[0], mind[2], mind[4], 'slowest cum', minc[0], minc[4])
fell = [x[0] for x in rows if x[2] < x[4]]
print('Q5-2 share fell', fell, len(fell))
for x in rows:
    s_now = x[1]/x[3]; s_base = (x[1]/(1+x[2]/100))/(x[3]/(1+x[4]/100))
    print('   ', x[0], round(s_now*100,3), round(s_base*100,3))
print('Q5-3', 135.9/1.014, 157.6/1.051)
