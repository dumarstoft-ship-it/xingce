# MK2715X-M3: 2024年10月社零
# Q1: 2023年1-9月 = 2023年1-10月 - 2023年10月
t110, g110 = 398960, 0.035
t10, g10 = 45396, 0.048
b110 = t110/(1+g110); b10 = t10/(1+g10)
print("Q1 2023 1-10=%.2f 2023 10=%.2f 2023 1-9=%.2f; 2024 1-9=%d" % (b110, b10, b110-b10, t110-t10))
# wrong: (t110-t10)/(1+something)
print("Q1 trap: 353564/1.035=%.1f" % ((t110-t10)/1.035))

# Q2: growth amount in Oct 2024
items = {"粮油食品":(1844,10.1),"服装":(1347,8.0),"化妆品":(468,40.1),"通讯器材":(835,14.4)}
for k,(v,r) in items.items():
    print("Q2 %s inc=%.2f" % (k, v*r/(100+r)))

# Q3: below-quota catering growth
cat, cr = 4952, 0.032
catu, cur = 1322, -0.003
now = cat - catu
base = cat/(1+cr) - catu/(1+cur)
print("Q3 now=%d base=%.3f growth=%.4f%%" % (now, base, (now/base-1)*100))

# Q4: 1-10 categories with growth > goods retail growth (3.2%)
cats = [("粮油食品",17658,9.9),("饮料",2675,3.9),("烟酒",5002,6.1),("服装",11571,1.1),("化妆品",3563,3.0),
        ("金银珠宝",2720,-3.0),("日用品",6556,2.9),("体育娱乐",1128,11.5),("家电",7908,7.8),("中西药",5815,4.3),
        ("文化办公",3420,-0.6),("家具",1303,1.9),("通讯器材",6331,12.2),("石油",20179,1.3),("汽车",39921,-1.5),("建筑装潢",1337,-3.0)]
up = [c for c in cats if c[2] > 3.2]
print("Q4 >3.2%%: %d %s" % (len(up), [c[0] for c in up]))
up2 = [c for c in cats if c[2] > 2.7]
print("Q4 alt >2.7%% (限上商品): %d" % len(up2))
# check the precise proportion change (exact via base values)
G = 354593; Gg = 0.032
for name, v, r in cats:
    s_now = v/G; s_base = (v/(1+r/100))/(G/(1+Gg))
    flag = s_now > s_base
    if flag != (r > 3.2): print("mismatch", name)

# Q5
oct_cats = [("粮油食品",1844),("饮料",254),("烟酒",480),("服装",1347),("化妆品",468),("金银珠宝",264),("日用品",692),
            ("体育娱乐",136),("家电",993),("中西药",583),("文化办公",438),("家具",152),("通讯器材",835),("石油",1968),("汽车",4452),("建筑装潢",150)]
print("Q5-1 share=%.4f%%" % (15664/40444*100))
thr = 40444*0.02
big = [c for c in oct_cats if c[1] > thr]
print("Q5-2 thr=%.2f count=%d %s" % (thr, len(big), [c[0] for c in big]))
mx = max(cats, key=lambda c:c[1]); mn = min(cats, key=lambda c:c[1])
print("Q5-3 max=%s %d min=%s %d ratio=%.4f 多倍=%.4f" % (mx[0], mx[1], mn[0], mn[1], mx[1]/mn[1], mx[1]/mn[1]-1))
print("Q5-4 dec=%.3f ; wrong formula /1.066=%.3f ; 1968*0.066=%.3f" % (1968*0.066/(1-0.066), 1968*0.066/1.066, 1968*0.066))
