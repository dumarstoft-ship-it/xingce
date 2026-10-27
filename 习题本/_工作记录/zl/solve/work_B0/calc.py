def p(label, v):
    print(f'{label}: {v}')

print('===== MK2710X-M2 (南昌人口) =====')
# Q1 城镇化率变化
u22, r22 = 516.01, 137.80
u21, r21 = u22 - 9.78, r22 - 0.28
tot21 = u21 + r21
rate21 = u21 / tot21 * 100
p('Q1 2021 urban', u21); p('Q1 2021 rural', r21); p('Q1 2021 total', tot21)
p('Q1 rate21 %', rate21); p('Q1 rate22 % (given 78.92), computed', u22 / (u22 + r22) * 100)
p('Q1 change pp', 78.92 - rate21)
# Q2 2021 死亡人口
dr21 = 7.21 - 2.19
p('Q2 death rate 2021 permille', dr21)
p('Q2 death 2021 = 4.58*dr/7.21', 4.58 * dr21 / 7.21)
p('Q2 avg pop 2021', 4.58 / 7.21 * 1000)
# Q3 2021 65+/60+
P22 = 653.81
a60_22 = P22 * 0.1521; a65_22 = P22 * 0.1118
a60_21 = a60_22 - 4.75; a65_21 = a65_22 - 4.20
p('Q3 60+ 2022', a60_22); p('Q3 65+ 2022', a65_22)
p('Q3 60+ 2021', a60_21); p('Q3 65+ 2021', a65_21)
p('Q3 ratio %', a65_21 / a60_21 * 100)
p('Q3 via shares', (11.18 - 0.48) / (15.21 - 0.50) * 100)
p('Q3 share check 60+ 2021', a60_21 / tot21 * 100)
# Q4 城镇常住人口
tab = {
    '东湖区': (41.89, 101.10, 94.43), '西湖区': (49.17, 101.25, 100.00), '青云谱区': (36.04, 107.75, 100.00),
    '青山湖区': (68.84, 109.07, 95.12), '新建区': (61.28, 118.33, 71.61), '红谷滩区': (64.45, 106.42, 91.92),
    '南昌县': (123.86, 109.46, 63.25), '安义县': (26.77, 116.20, 55.11), '进贤县': (65.07, 106.18, 52.78),
    '经开区': (57.30, 122.85, 87.01), '高新区': (47.58, 111.87, 82.51), '湾里管理局': (11.56, 102.14, 52.66)}
urb = {k: v[0] * v[2] / 100 for k, v in tab.items()}
for k, v in sorted(urb.items(), key=lambda x: -x[1]):
    print('   ', k, round(v, 3))
p('Q4 sum pop', sum(v[0] for v in tab.values()))
p('Q4 sum urban', sum(urb.values()))
# Q5
f_ncx = 123.86 * 100 / (100 + 109.46)
m_gx = 47.58 * 111.87 / (100 + 111.87)
p('Q5 南昌县女', f_ncx); p('Q5 高新区男', m_gx); p('Q5 ratio', f_ncx / m_gx)

print('===== MK26ZX-M3 (工业机器人) =====')
prod23 = 55.64 / 1.142
p('Q1 prod 2023', prod23); p('Q1 diff', prod23 - 31.6)
q123_23 = 17906 / 1.1495
q4 = 21268 - q123_23
p('Q2 2023 Q1-3', q123_23); p('Q2 2023 Q4', q4); p('Q2 share %', q4 / 21268 * 100)
amt = {2020: 633.24, 2021: 268.08, 2022: 256.81, 2023: 162.17, 2024: 508.09}
cnt = {2020: 115, 2021: 162, 2022: 153, 2023: 130, 2024: 125}
avg = {y: amt[y] / cnt[y] for y in amt}
for y in avg:
    print('   avg', y, round(avg[y], 4))
p('Q3 ratio 2024/2023', avg[2024] / avg[2023]); p('Q3 increase times', avg[2024] / avg[2023] - 1)
p('Q5A sales change %', (30 / 31.6 - 1) * 100)
p('Q5B coop share %', 6058 / 21268 * 100)
inc = 2000 * 0.4232 / 1.4232
p('Q5C coop increase (2000 base)', inc); p('Q5C monthly', inc / 9)
p('Q5C needed 2024 value for >90/month', 810 * 1.4232 / 0.4232)
p('Q5D avg events', sum(cnt.values()) / 5)

print('===== MK2740X-M1 (水利) =====')
for name, v, d in [('建筑', 9089, 597), ('安装', 583, 97), ('机电', 321, 34), ('其他', 2003, 375)]:
    print('   ', name, 'growth %', round(d / (v - d) * 100, 3))
p('Q1 sum parts', 9089 + 583 + 321 + 2003)
t22 = 11996 / 1.101
s22 = 9009 / 1.031
l22 = t22 - s22
p('Q2 total 2022', t22); p('Q2 small 2022', s22); p('Q2 large 2022', l22); p('Q2 growth %', (2987 / l22 - 1) * 100)
p('Q2 check parts 2023', 2987 + 9009)
p('Q3 per-capita wage growth %', ((1 - 0.105) / (1 - 0.134) - 1) * 100)
p('Q4 increase 2025 vs 2023', 27925 * (1.115 ** 2 - 1))
parts = [3227, 5665, 2079, 1025]
S = sum(parts)
p('Q5 sum', S)
cum = 0
for x in parts:
    cum += x
    print('    share %.2f%%  cum angle %.2f' % (x / S * 100, cum / S * 360))

print('===== MK2710X-M1 (百度) =====')
rd = [32.9, 40.3, 39.2, 45.3, 41.7, 47.3, 46.9, 47.6, 44.4]
ratio = [15.8, 15.5, 13.9, 16.7, 17.3, 18.0, 16.7, 16.5, 19.7]
p('Q1 sum 8 quarters', sum(rd[:8])); p('Q1 per month', sum(rd[:8]) / 24)
net19 = 142 / 0.81
oth19 = 83 / 1.28
rev19_a = 41.7 / 0.173
p('Q2 net 2019Q1', net19); p('Q2 total via RD', rev19_a); p('Q2 share via RD %', net19 / rev19_a * 100)
p('Q2 total via parts', net19 + oth19); p('Q2 share via parts %', net19 / (net19 + oth19) * 100)
p('Q3 2020Q2 est', 44.4 * 44.4 / 47.6); p('Q3 qoq %', (44.4 / 47.6 - 1) * 100)
import itertools
pairs = sorted(((abs(ratio[i] - ratio[j]), i, j) for i, j in itertools.combinations(range(9), 2)))[:4]
print('   Q4 closest pairs', pairs)
p('Q4 rd diff', 46.9 - 45.3)
p('Q5A 2019Q1 SGA', 39 / 0.64)
rev18 = [rd[i] / ratio[i] * 100 for i in range(4)]
print('   Q5B 2018 revenues', [round(x, 1) for x in rev18])
p('Q5C growth %', 41.3 / (65 - 41.3) * 100)
p('Q5D 2018 RD', sum(rd[:4])); p('Q5D 2019 RD', sum(rd[4:8]))

print('===== MK2736F-M3 (J省文化企业) =====')
all_rev = 2515.16 / 0.708
p('Q1 all culture revenue', all_rev); p('Q1 share %', 291.23 / all_rev * 100); p('Q1 trap share in 规上 %', 291.23 / 2515.16 * 100)
fa18 = 24.09 / 1.871
p('Q2 foreign assets 2018', fa18); p('Q2 per firm', fa18 / (16 - 4))
g_soe = 78.6 - 56.2
p('Q3 SOE rev growth %', g_soe); p('Q3 SOE rev 2018', 291.23 / (1 + g_soe / 100))
for name, n, d in [('国有', 203, 81), ('港澳台', 61, 6), ('外商', 16, 4), ('民营', 2474, 1133)]:
    print('    Q4', name, 'growth %', round(d / (n - d) * 100, 2))
p('Q4 counts sum 2023', 203 + 61 + 16 + 2474)
p('Q5 assets sum 2023', 1140.26 + 192.11 + 24.09 + 1634.97)
tot18 = 2991.44 / (1 + (72.0 - 21.2) / 100)
pri18 = 1634.97 / 1.72
hmt18 = 192.11 / 1.055
soe18 = tot18 - pri18 - hmt18 - fa18
p('Q5 total 2018', tot18); p('Q5 private 2018', pri18); p('Q5 HMT 2018', hmt18); p('Q5 SOE 2018 (residual)', soe18)
sh18 = [soe18 / tot18, hmt18 / tot18, fa18 / tot18, pri18 / tot18]
print('    Q5 2018 shares %', [round(x * 100, 2) for x in sh18])
cum = 0
for x in sh18:
    cum += x
    print('    cum angle %.2f' % (cum * 360))
sh23 = [x / 2991.44 for x in (1140.26, 192.11, 24.09, 1634.97)]
print('    Q5 2023 shares %', [round(x * 100, 2) for x in sh23])
# alternative (designer?) SOE assets using 22.4% growth
soe18b = 1140.26 / 1.224
totb = soe18b + hmt18 + fa18 + pri18
print('    Q5 alt (SOE assets /1.224) shares %', [round(x / totb * 100, 2) for x in (soe18b, hmt18, fa18, pri18)], 'total', round(totb, 2))
# measured pies (angles of boundaries)
meas = {'A': (137.11, 160.28, 163.23), 'B': (41.67, 59.45, 70.91), 'C': (125.13, 140.76, 203.57), 'D': (161.25, 192.71, 195.47)}
for k, (a, b, c) in meas.items():
    sh = [a / 360, (b - a) / 360, (c - b) / 360, (360 - c) / 360]
    dev = sum(abs(sh[i] - sh18[i]) for i in range(4)) * 100
    print('    pie', k, [round(x * 100, 2) for x in sh], 'sum|dev| vs 2018 = %.2f pp' % dev)

print('===== MK2724X-M1 (水上运输船舶) =====')
s23 = 55.76 / 81.25
p('Q1 share 2023 %', s23 * 100)
p('Q1 share 2022 %', 55.76 / 0.974 / (81.25 / 0.943) * 100)
p('Q1 change pp', s23 * 100 * (-0.026 + 0.057) / (1 - 0.026))
dn = 62.40 * 0.131 / 1.131
dc = 68.83 * 0.149 / 1.149
do = 173.01 * (-0.058) / (1 - 0.058)
p('Q2 内河 change', dn); p('Q2 沿海 change', dc); p('Q2 远洋 change', do)
p('Q2 total change check', 304.24 * 0.018 / 1.018)
p('Q3 avg dwt growth %', (1.012 / 0.974 - 1) * 100)
ao = 12700 / 972
ac = 242200 / 10672
p('Q4 远洋 avg seats', ao); p('Q4 沿海 avg seats', ac); p('Q4 ratio', ao / ac)
p('Q5A pull %', dc / (304.24 / 1.018) * 100)
print('    Q5B 内河', (1 - 0.026) / (1 - 0.026) - 1, '沿海', (1 - 0.098) / (1 - 0.030) - 1, '远洋', (1 - 0.384) / (1 - 0.299) - 1)
p('Q5C total ships', 106600 + 10672 + 972); p('Q5C trap', 10.66 + 10672 + 972)
p('Q5D share %', 4826.20 / 30052.07 * 100)

print('===== MK2719X-M3 (A省教育) =====')
pri22 = 518.49 + 4.61
grad22 = 12.36 - 0.63
p('Q1 ratio', pri22 / grad22); p('Q1 多多少倍', pri22 / grad22 - 1)
items = [('小学', 518.49, -4.61), ('初中', 270.78, 7.04), ('高中', 147.30, 5.07), ('中职', 70.37, -4.26),
         ('研究生', 12.36, 0.63), ('本专科', 177.80, 9.29), ('特教在校', 5.17, -0.19), ('幼儿', 183.70, -32.3)]
for n, v, d in items:
    print('    Q2', n, 'growth %', round(d / (v - d) * 100, 3))
p('Q2 特教招收 growth %', 0.06 / 0.74 * 100)
p('Q2 普通高校合计 growth %', (0.63 + 9.29) / (12.36 - 0.63 + 177.80 - 9.29) * 100)
p('Q3 growth %', (1.182 * 495 / 497 - 1) * 100)
area22 = 1669.7 / (1 - 0.007)
k22 = 15327 + 671
p('Q4 area 2022 (万m2)', area22); p('Q4 kindergartens 2022', k22); p('Q4 per kg m2', area22 * 1e4 / k22)
p('Q5-1 book increase', 1762.28 * 0.182 / 1.182)
p('Q5-2 2028 kindergartens', 15327 - 5 * 671)
p('Q5-3 total students', sum(v for _, v, _ in items))

print('===== MK2713X-M3 (党内统计) =====')
p('Q1 increase', 517.6 * 0.022 / 1.022)
old = 890.7 + 2787.2
young = 1241.2 + 1119.6 + 1086.4 + 945.9 + 907.1 + 940.5
p('Q2 56+', old); p('Q2 <56', young); p('Q2 少 %', (1 - old / young) * 100); p('Q2 sum check', old + young)
dev_tot = 110.5 / 0.459
p('Q3 develop total', dev_tot); p('Q3 by occupations', 15.8 + 37.5 + 35.1 + 26.7 + 11.9 + 91.9 + 21.8)
p('Q3 minority share %', 25.2 / dev_tot * 100)
p('Q4 min share %', 56.2 + (100 - 30.4) - 100)
p('Q4 precise', (5578.6 + 9918.5 - 3018.5 - 9918.5) / 9918.5 * 100)
p('Q5A multiple', 1619.0 / 35.1)
end22 = 9918.5 - 114.4
inc22 = 114.4 + 18.5
p('Q5B 2022 end', end22); p('Q5B 2022 net increase', inc22); p('Q5B 2021 end', end22 - inc22); p('Q5B trap', end22 - (114.4 - 18.5))
male = 9918.5 - 3018.5
p('Q5C male', male); p('Q5C male/female', male / 3018.5)
p('Q5D share %', 2611.2 / 9918.5 * 100)
