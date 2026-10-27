# MK2740X-M2: digital reading
users = {2018: (4.30, 13.76), 2019: (4.68, 8.84), 2020: (4.94, 5.56), 2021: (5.06, 2.43), 2022: (5.30, 4.74)}
print('=== Q1 user increase per year (亿人) ===')
cnt = 0
for y, (v, g) in users.items():
    inc_g = v * g / (100 + g)
    inc_d = v - users[y - 1][0] if y - 1 in users else None
    print(y, 'inc by rate %.4f' % inc_g, 'inc by diff', None if inc_d is None else round(inc_d, 4))
    if inc_g > 0.3:
        cnt += 1
print('count >0.3:', cnt)

print('=== Q2 2021 copyright revenue ===')
rev22 = 463.52
rev21 = rev22 / 1.115
print('rev21', rev21, 'copyright21', rev21 * 0.1580)
print('traps: 22rev*21share', rev22 * 0.158, '22rev*22share', rev22 * 0.2102, '21rev*22share', rev21 * 0.2102)

print('=== Q3 2021 works growth ===')
tot22 = 5271.86
tot21 = tot22 - 1825.00
tot20 = tot22 - 2168.26
print('tot21', tot21, 'tot20', tot20, 'g21', tot21 / tot20 - 1, 'g22', tot22 / tot21 - 1, 'two-year', tot22 / tot20 - 1)

print('=== Q4 net-lit increase / ebook increase ===')
nl = 3458.84 * 0.0793 / 1.0793
eb = 206.92 * 0.1461 / 1.1461
print('net lit inc', nl, 'ebook inc', eb, 'ratio', nl / eb, 'trap current ratio', 3458.84 / 206.92)

print('=== Q5 ===')
age19_45 = 36.60 + 30.55
male = 55.87
print('(1) 19-45 share', age19_45, 'min overlap male&19-45', age19_45 + male - 100)
print('    age sum', 16.93 + 36.60 + 30.55 + 13.23 + 2.74, 'alt 19-45 via complement', 100 - 16.93 - 13.23 - 2.74,
      'alt overlap', 100 - 16.93 - 13.23 - 2.74 + male - 100)
copy = {2018: 12.33, 2019: 28.90, 2020: 11.90, 2021: 15.80, 2022: 21.02}
print('(2) copyright share max', max(copy.values()), 'min', min(copy.values()), 'diff', max(copy.values()) - min(copy.values()),
      'trap 2019-2018', copy[2019] - copy[2018])
ads = {2018: 7.77, 2019: 10.27, 2020: 29.41, 2021: 31.50, 2022: 30.25}
n = 0
for y in range(2019, 2023):
    up = ads[y] > ads[y - 1]
    # share_t/share_{t-1} = (1+g_ads)/(1+g_total); total growth > ads growth iff ads share fell
    tot_gt = not up
    n += tot_gt
    print('   ', y, 'ads share %.2f -> %.2f' % (ads[y - 1], ads[y]), 'total growth > ads growth?', tot_gt)
print('(3) years total growth > ads growth:', n)
# check shares sum
for y in range(2018, 2023):
    pass
sub = {2018: 79.90, 2019: 60.83, 2020: 58.69, 2021: 52.70, 2022: 48.73}
for y in range(2018, 2023):
    print('   share sum', y, round(sub[y] + copy[y] + ads[y], 2))
# 2022 ads growth check
print('   2022 ads growth', (463.52 * 0.3025) / (rev21 * 0.3150) - 1, 'total 11.5%')
