# MK2711X-M1 软件业务
tot, r, r_prev = 14461, 0.11, 0.11+0.006
# Q1 2021年1-2月
print("Q1 2021", tot/((1+r)*(1+r_prev)), " trap 2022:", tot/(1+r), " trap r_prev=10.4%:", tot/((1+r)*(1.104)), " tot*1.11", tot*1.11)
# Q2 前5 / 6-10
prov = [("北京",3163,12.7),("广东",2714,14.5),("江苏",1880,9.0),("山东",1480,15.8),("浙江",1270,3.9),
        ("上海",1188,8.1),("四川",672,15.0),("山西",340,6.7),("福建",301,6.9),("重庆",276,19.2)]
top5 = sum(p[1] for p in prov[:5]); nxt5 = sum(p[1] for p in prov[5:])
print("Q2 top5", top5, "6-10", nxt5, "ratio", top5/nxt5)
# Q3 副省级城市 51.4%, 回落0.5pp -> 上年51.9%
s_now, s_prev = 0.514, 0.519
g = s_now/s_prev*(1+r)-1
print("Q3 growth", g, " cur", tot*s_now, " prev", tot/(1+r)*s_prev)
# Q4 地区占比
reg = {"东部":12244,"中部":476,"西部":1492,"东北":249}
print("Q4 sum", sum(reg.values()))
for k,v in reg.items(): print("  ", k, v/tot, "deg", 360*v/tot)
print("  西部/中部", 1492/476, " 中部/东北", 476/249)
# measured pies (deg): A: 303,20.7,28.2,8.1 ; C: 304.3,11.7,37.6,6.3 ; D: 321.8,7.3,15.7,15.2
for k,degs in {"A":[303,20.7,28.2,8.1],"C":[304.3,11.7,37.6,6.3],"D":[321.8,7.3,15.7,15.2]}.items():
    print("  pie", k, [round(d/360*100,2) for d in degs])
# Q5
cq, zj = 276, 1270; rcq, rzj = 0.192, 0.039
print("Q5-1 cur ratio", cq/zj, "prev", (cq/(1+rcq))/(zj/(1+rzj)))
print("Q5-2 西/中", 1492/476, " 多几倍", 1492/476-1)
gd = 2714*0.145/1.145; sx = 340*0.067/1.067
print("Q5-3 广东增量", gd, "山西增量", sx, "差", gd-sx)
