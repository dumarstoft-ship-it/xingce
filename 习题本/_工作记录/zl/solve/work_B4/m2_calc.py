# MK2721X-M2 mineral exploration 2023
rows = [('煤炭',19.72,19.3,179,29.7),('铁矿',5.52,30.2,59,68.6),('锰矿',0.71,-14.5,3,-50.0),('铜矿',8.71,32.6,49,48.5),
('铅锌矿',8.63,50.9,69,81.6),('铝土矿',2.70,5.9,27,0),('镍矿',1.04,100.0,24,380.0),('钨矿',1.86,25.7,14,40.0),
('锡矿',0.52,-5.5,4,0),('钼矿',0.96,31.5,6,0),('金矿',14.04,31.1,98,44.1),('银矿',1.61,32.0,16,166.7),
('磷矿',1.99,-30.9,15,-28.6),('石墨',0.96,-32.4,6,-40.0),('钾盐',0.83,-1.2,2,-50.0)]
print('Q1', [r[0] for r in rows if r[2] > r[4]], len([r for r in rows if r[2] > r[4]]))
m = max(rows, key=lambda r: r[4]); print('Q2', m[0], m[3]*m[4]/(100+m[4]))
s = sum(r[3] for r in rows); print('Q3', s, s/len(rows), len(rows))
g = rows[10]; c = rows[0]
for n in range(1,8):
    print('Q4', 2023+n, g[1]*(1+g[2]/100)**n, c[1]*(1+c[2]/100)**n)
import math
print('Q4 n*', math.log(c[1]/g[1])/math.log((1+g[2]/100)/(1+c[2]/100)))
w = rows[7]; print('Q5A', (1+w[2]/100)/(1+w[4]/100)-1)
top_inv = sorted(rows, key=lambda r: -r[1])[:3]; top_dr = sorted(rows, key=lambda r: -r[3])[:3]
print('Q5B', [r[0] for r in top_inv], sum(r[1] for r in top_inv), [r[0] for r in top_dr], sum(r[1] for r in top_dr), sum(r[1] for r in top_inv)-sum(r[1] for r in top_dr))
for r in rows:
    if r[4] < 0:
        base = r[3]/(1+r[4]/100)
        print('Q5C', r[0], 'base', round(base,2), 'decrease', round(base-r[3],2), 'rate', r[4])
print('Q5D', [r[0] for r in rows if r[1] < 1 and r[3] < 10])
