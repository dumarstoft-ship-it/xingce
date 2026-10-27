# MK2706X-M1 快递 2023
nat_vol, g_vol = 1320.7, 0.194
nat_rev, g_rev = 12074.0, 0.143

t1 = [  # 业务量 亿件, 同比增加
    ('金华', 136.9, 18.9), ('广州', 114.5, 13.2), ('深圳', 63.7, 5.7), ('揭阳', 40.7, 3.4),
    ('杭州', 40.1, 5.3), ('上海', 37.0, 8.5), ('东莞', 34.3, 5.5), ('汕头', 29.8, 5.2),
    ('苏州', 27.9, 3.6), ('泉州', 24.8, 3.7)]
t2 = [  # 收入 亿元, 同比增加
    ('上海', 2089.4, 243.9), ('广州', 892.2, 51.7), ('深圳', 668.4, 66.2), ('金华', 372.3, 30.5),
    ('杭州', 366.7, 31.2), ('东莞', 352.8, 63.8), ('北京', 311.0, 19.5), ('苏州', 277.8, 28.8),
    ('佛山', 201.7, 27.3), ('揭阳', 200.6, 22.5)]

print('Q1: 2022 revenue ranking')
base = [(c, v - d) for c, v, d in t2]
rank23 = {c: i + 1 for i, (c, v, d) in enumerate(t2)}
srt = sorted(base, key=lambda x: -x[1])
diff = 0
for i, (c, b) in enumerate(srt):
    r22 = i + 1
    flag = '' if r22 == rank23[c] else '  <-- changed'
    if flag:
        diff += 1
    print('  %s 2022=%.1f rank22=%d rank23=%d%s' % (c, b, r22, rank23[c], flag))
print('  changed count =', diff)

print('Q2: growth rates')
d2 = {c: (v, d) for c, v, d in t2}
for c in ['北京', '揭阳', '佛山', '东莞']:
    v, d = d2[c]
    print('  %s %.4f%%' % (c, d / (v - d) * 100))

print('Q3: contribution rate')
s_inc = sum(d for c, v, d in t1)
nat_inc = nat_vol * g_vol / (1 + g_vol)
print('  top10 increase =', s_inc, ' national increase =', nat_inc, ' rate =', s_inc / nat_inc)
# trap: share of volume
s_vol = sum(v for c, v, d in t1)
print('  (top10 volume share =', s_vol / nat_vol, ')')

print('Q4: Guangzhou revenue per item')
v1, d1 = 114.5, 13.2
r1, e1 = 892.2, 51.7
avg23 = r1 / v1; avg22 = (r1 - e1) / (v1 - d1)
gr = e1 / (r1 - e1); gv = d1 / (v1 - d1)
print('  avg23 =', avg23, ' avg22 =', avg22, ' change =', avg23 / avg22 - 1)
print('  rev growth =', gr, ' vol growth =', gv, ' (gr-gv)/(1+gv) =', (gr - gv) / (1 + gv))

print('Q5: pie shares of volume')
d1t = {c: v for c, v, d in t1}
cs = ['上海', '广州', '深圳', '杭州']
tot = sum(d1t[c] for c in cs)
for c in cs:
    print('  %s %.2f%%' % (c, d1t[c] / tot * 100))
tot2 = sum(d2[c][0] for c in cs)
print('  (revenue shares:', [(c, round(d2[c][0] / tot2 * 100, 1)) for c in cs], ')')
