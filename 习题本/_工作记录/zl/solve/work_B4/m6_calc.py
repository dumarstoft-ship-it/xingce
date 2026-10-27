# MK2706X-M3 Shenzhen foreign trade 2023
tot, tg = 3.87, 0.059; ex, eg = 2.46, 0.125
imp = tot-ex; tot22 = tot/(1+tg); ex22 = ex/(1+eg); imp22 = tot22-ex22
print('Q1', imp, imp22, imp/imp22-1)
me, mg = 1.78, 0.067
print('Q2', (me/(1+mg))/ex22, 'current', me/ex, 'formula', me/ex*(1+eg)/(1+mg))
items = {'消费品':(1349.1,3.1),'半导体制造设备':(301.6,316.2),'大宗商品':(238.9,56.8)}
for k,(v,g) in items.items(): print('Q3', k, v*g/(100+g))
pv, pg = 2.54, 0.123
print('Q4 current', pv/tot, 0.657, 'base', (pv/(1+pg))/tot22, 'change(pp)', (pv/tot - (pv/(1+pg))/tot22)*100, 'formula with 65.7%', 65.7*(pg-tg)/(1+pg))
bonded23 = tot*0.237; print('Q5-1 bonded 2022', bonded23, bonded23/1.052)
inc = tot - tot22; print('Q5-3 SZ increase', inc, 'GD 2022', inc/0.026, 'GD 2023 by share', tot/0.466, 'GD growth', (tot/0.466)/(inc/0.026)-1)
