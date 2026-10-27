# MK2706X-M3
tot=3.87; tg=0.059; ex=2.46; eg=0.125
im23 = tot-ex; im22 = tot/(1+tg) - ex/(1+eg)
print('Q1 imports 23', im23, '22', im22, 'growth', (im23/im22-1)*100)
print('Q2', (1.78/1.067)/(ex/(1+eg))*100, ' 2023 share', 1.78/ex*100)
items={'消费品':(1349.1,3.1),'半导体':(301.6,316.2),'大宗':(238.9,56.8)}
for k,(v,r) in items.items(): print('Q3', k, v*r/(100+r))
print('Q4', 65.7*(12.3-5.9)/112.3, ' check share', 2.54/3.87*100)
bl23 = tot*0.237; print('Q5-1 bonded 2023', bl23, '2022', bl23/1.052)
sz_inc = tot*tg/(1+tg); gd22 = sz_inc/0.026; gd23 = tot/0.466
print('Q5-3 sz inc', sz_inc, 'GD 2022', gd22, 'GD 2023', gd23, 'GD growth', (gd23/gd22-1)*100)
