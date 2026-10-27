# MK2715X-M3 retail sales Oct 2024
cat = [  # name, Oct value, Oct g%, Jan-Oct value, Jan-Oct g%
 ('粮油食品',1844,10.1,17658,9.9),('饮料',254,-0.9,2675,3.9),('烟酒',480,-0.1,5002,6.1),
 ('服装鞋帽',1347,8.0,11571,1.1),('化妆品',468,40.1,3563,3.0),('金银珠宝',264,-2.7,2720,-3.0),
 ('日用品',692,8.5,6556,2.9),('体育娱乐',136,26.7,1128,11.5),('家电',993,39.2,7908,7.8),
 ('中西药',583,1.4,5815,4.3),('文化办公',438,18.0,3420,-0.6),('家具',152,7.4,1303,1.9),
 ('通讯器材',835,14.4,6331,12.2),('石油制品',1968,-6.6,20179,1.3),('汽车',4452,3.7,39921,-1.5),
 ('建筑装潢',150,-5.8,1337,-3.0)]
print("Q1: 2023 Jan-Sep total retail")
a = 398960/1.035; b = 45396/1.048
print('  2023 1-10', a, ' 2023 Oct', b, ' 2023 1-9', a-b, '  (2024 1-9 =', 398960-45396, ')')
print("Q2: Oct increase amounts")
for n in ['粮油食品','服装鞋帽','化妆品','通讯器材']:
    c = [x for x in cat if x[0]==n][0]
    print('  ', n, c[1]*c[2]/100/(1+c[2]/100))
print("Q3: below-quota catering Oct growth")
now = 4952-1322; base = 4952/1.032 - 1322/(1-0.003)
print('  now', now, ' base', base, ' growth', (now/base-1)*100)
print("Q4: Jan-Oct categories with growth > 3.2% (商品零售额 growth)")
up = [x[0] for x in cat if x[4] > 3.2]
print('  ', up, len(up))
print('   (if threshold 2.7%:', len([x for x in cat if x[4] > 2.7]), ')')
print("Q5")
print('  (1) 15664/40444 =', 15664/40444*100)
thr = 40444*0.02
big = [(x[0], x[1]) for x in cat if x[1] > thr]
print('  (2) 2% of 40444 =', thr, big, len(big))
hi = max(cat, key=lambda x:x[3]); lo = min(cat, key=lambda x:x[3])
print('  (3) max', hi[0], hi[3], ' min', lo[0], lo[3], ' ratio', hi[3]/lo[3], ' 多', hi[3]/lo[3]-1)
print('  (4) petroleum Oct decrease', 1968*0.066/(1-0.066), ' wrong-formula', 1968*0.066/1.066, 1968*0.066)
