# MK2706X-M1 express delivery 2023
vol = {  # city: (2023 volume 亿件, increase 亿件)
 '金华':(136.9,18.9),'广州':(114.5,13.2),'深圳':(63.7,5.7),'揭阳':(40.7,3.4),'杭州':(40.1,5.3),
 '上海':(37.0,8.5),'东莞':(34.3,5.5),'汕头':(29.8,5.2),'苏州':(27.9,3.6),'泉州':(24.8,3.7)}
rev = {  # city: (2023 revenue 亿元, increase 亿元)
 '上海':(2089.4,243.9),'广州':(892.2,51.7),'深圳':(668.4,66.2),'金华':(372.3,30.5),'杭州':(366.7,31.2),
 '东莞':(352.8,63.8),'北京':(311.0,19.5),'苏州':(277.8,28.8),'佛山':(201.7,27.3),'揭阳':(200.6,22.5)}
print("Q1: 2022 revenue ranking")
r23 = list(rev.keys())
b = {c:(rev[c][0]-rev[c][1]) for c in rev}
r22 = sorted(b, key=lambda c:-b[c])
for i,c in enumerate(r22):
    print(i+1, c, round(b[c],1), '2023 rank', r23.index(c)+1, '' if r23.index(c)==i else '<-- changed')
print('changed count', sum(1 for i,c in enumerate(r22) if r23.index(c)!=i))

print("\nQ2: revenue growth rates")
for c in ['北京','揭阳','佛山','东莞']:
    print(c, f"{rev[c][1]/b[c]*100:.2f}%")

print("\nQ3: contribution of top10 to national volume growth")
tot = 1320.7; g = 0.194
inc_nat = tot*g/(1+g)
inc10 = sum(v[1] for v in vol.values())
print('national base', tot/(1+g), 'national inc', inc_nat, 'top10 inc', inc10, 'rate', inc10/inc_nat*100)

print("\nQ4: Guangzhou avg revenue per item")
a23 = rev['广州'][0]/vol['广州'][0]
a22 = (rev['广州'][0]-rev['广州'][1])/(vol['广州'][0]-vol['广州'][1])
print('2023', a23, '2022', a22, 'change %', (a23/a22-1)*100)
gr = rev['广州'][1]/(rev['广州'][0]-rev['广州'][1]); gv = vol['广州'][1]/(vol['广州'][0]-vol['广州'][1])
print('rev growth', gr*100, 'vol growth', gv*100, '(a-b)/(1+b)', (gr-gv)/(1+gv)*100)

print("\nQ5: pie shares")
cs = ['上海','广州','深圳','杭州']
s = sum(vol[c][0] for c in cs)
for c in cs:
    print(c, vol[c][0], f"{vol[c][0]/s*100:.2f}%  angle {vol[c][0]/s*360:.1f} deg")
