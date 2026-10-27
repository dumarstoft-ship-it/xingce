# MK2721X-M2 2023年主要矿产勘查资金投入和钻探工作量
import math
rows = [('煤炭',19.72,19.3,179,29.7),('铁矿',5.52,30.2,59,68.6),('锰矿',0.71,-14.5,3,-50.0),('铜矿',8.71,32.6,49,48.5),
('铅锌矿',8.63,50.9,69,81.6),('铝土矿',2.70,5.9,27,0),('镍矿',1.04,100.0,24,380.0),('钨矿',1.86,25.7,14,40.0),
('锡矿',0.52,-5.5,4,0),('钼矿',0.96,31.5,6,0),('金矿',14.04,31.1,98,44.1),('银矿',1.61,32.0,16,166.7),
('磷矿',1.99,-30.9,15,-28.6),('石墨',0.96,-32.4,6,-40.0),('钾盐',0.83,-1.2,2,-50.0)]
q1 = [r[0] for r in rows if r[2] > r[4]]
print("Q1", len(q1), q1)
mx = max(rows, key=lambda r: r[4])
print("Q2 fastest", mx[0], mx[4], " increase", mx[3]*mx[4]/(100+mx[4]))
s = sum(r[3] for r in rows)
print("Q3 sum", s, " avg", s/len(rows), len(rows))
gold=14.04; gg=31.1; coal=19.72; cg=19.3
for n in range(1,8):
    G = gold*(1+gg/100)**n; C = coal*(1+cg/100)**n
    print("Q4", 2023+n, round(G,3), round(C,3), G>C)
print("   n* =", math.log(coal/gold)/math.log((1+gg/100)/(1+cg/100)))
w = [r for r in rows if r[0]=='钨矿'][0]
print("Q5 A 钨矿每米资金增速", ((1+w[2]/100)/(1+w[4]/100)-1)*100)
top_fund = sorted(rows, key=lambda r: -r[1])[:4]
top_drill = sorted(rows, key=lambda r: -r[3])[:4]
print("   B top fund", [(r[0],r[1]) for r in top_fund], " top drill", [(r[0],r[3]) for r in top_drill])
sf = sum(r[1] for r in sorted(rows, key=lambda r: -r[1])[:3]); sd = sum(r[1] for r in sorted(rows, key=lambda r: -r[3])[:3])
print("   B sums", sf, sd, " diff", round(sf-sd,4))
for r in rows:
    if r[4] < 0:
        print("   C", r[0], "drill decrease", round(r[3]*(-r[4])/(100+r[4]),3), "base", round(r[3]/(1+r[4]/100),3))
print("   D", [(r[0],r[1],r[3]) for r in rows if r[1]<1 and r[3]<10])
