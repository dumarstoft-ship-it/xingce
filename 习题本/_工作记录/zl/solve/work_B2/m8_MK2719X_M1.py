# MK2719X-M1 culture enterprises 2024 Q1
rev = 31057; g = 0.085; n_firms = 7.6  # 万家
print("Q1 per firm per month (万元)", rev/n_firms/3, " per quarter", rev/n_firms)
sub = 12633; sg = 0.119
inc_sub = sub*sg/(1+sg); inc_tot = rev*g/(1+g)
print("Q2 inc sub", inc_sub, "inc tot", inc_tot, "contrib", inc_sub/inc_tot*100)
r23 = rev/(1+g); m23 = 6.81+0.17
p23 = r23*m23/100
print("Q3 2023 rev", r23, "2023 margin", m23, "2023 profit", p23, "growth", (2116/p23-1)*100)
print("   via formula", (1.085*6.81/6.98-1)*100, " trap (6.64)", (1.085*6.81/6.64-1)*100, (2116/(r23*0.0664)-1)*100)
ind = {'新闻信息服务':(4101,11.1),'内容创作生产':(7054,12.0),'创意设计服务':(5219,10.4),'文化传播渠道':(4026,6.8),
       '文化投资运营':(145,10.4),'文化娱乐休闲服务':(375,10.5),'文化辅助生产和中介服务':(3583,7.3),'文化装备生产':(1378,6.0),'文化消费终端生产':(5175,2.7)}
print("Q4 increments")
for k in ['新闻信息服务','创意设计服务','文化传播渠道','文化消费终端生产']:
    v,gr = ind[k]; print(k, round(v*gr/100/(1+gr/100),1))
print("Q5")
print("A 2023 per-100 assets", 63.0-0.5, " check 2024 annualized", rev/197329*100*4)
print("B 2023 service rev (亿元)", 16331/1.109)
print("C industries growth > 8.5:", [k for k,(v,gr) in ind.items() if gr>8.5], sum(1 for k,(v,gr) in ind.items() if gr>8.5))
print("   sum of industries 2024", sum(v for v,_ in ind.values()))
print("D 2023 central - west", 3491/1.065 - 2524/1.049, " 2024 diff", 3491-2524)
