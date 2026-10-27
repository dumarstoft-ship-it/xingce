# MK2719X-M1
rev=31057; g=0.085; firms=7.6e4
print('Q1 per firm per month (wan yuan)', rev*1e4/firms/3, ' per quarter', rev*1e4/firms)
inc16 = 12633*0.119/1.119; inctot = rev*g/(1+g)
print('Q2', inc16, inctot, inc16/inctot*100)
print('Q3 via rate', (1.085*6.81/6.98-1)*100, ' via abs', (2116/((rev/1.085)*0.0698)-1)*100, ' check rate', 2116/rev*100)
ind = {'新闻信息服务':(4101,11.1),'内容创作生产':(7054,12.0),'创意设计服务':(5219,10.4),'文化传播渠道':(4026,6.8),'文化投资运营':(145,10.4),'文化娱乐休闲服务':(375,10.5),'文化辅助生产和中介服务':(3583,7.3),'文化装备生产':(1378,6.0),'文化消费终端生产':(5175,2.7)}
for k,(v,r) in ind.items():
    print(k, 'inc', v*r/(100+r), 'share up?', r>8.5)
print('sum ind', sum(v for v,r in ind.values()))
print('count share up', sum(1 for v,r in ind.values() if r>8.5))
# check overall growth from parts
base = sum(v/(1+r/100) for v,r in ind.values()); print('base sum', base, 'implied growth', (sum(v for v,r in ind.values())/base-1)*100)
print('A: 2023 per 100', 63.0-0.5, ' quarterly check', rev/197329*100, rev/197329*400, (rev/1.085)/(197329/1.076)*400)
print('B: serv 2023', 16331/1.109)
c = 3491/1.065; w = 2524/1.049
print('D: central', c, 'west', w, 'diff', c-w, ' 2024 diff', 3491-2524)
