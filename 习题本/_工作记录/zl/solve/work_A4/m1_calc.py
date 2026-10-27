# MK2736F-M3 calculations
print('--- Q1: 2023 国有控股营收占全部文化产业比重')
gy_rev = 291.23
gs_rev = 2515.16  # 规上营收, 占全部文化产业 70.8%
all_rev = gs_rev / 0.708
print('全部文化产业营收', all_rev)
print('国有占全部', gy_rev / all_rev * 100)
print('trap 国有占规上', gy_rev / gs_rev * 100)
print('trap 港澳台占规上', 123.43 / gs_rev * 100, '国有营收/规上资产', gy_rev / 2991.44 * 100)

print('--- Q2: 2018 外商控股平均每个企业资产')
ws_asset_2018 = 24.09 / 1.871
ws_n_2018 = 16 - 4
print('2018资产', ws_asset_2018, '企业数', ws_n_2018, '平均', ws_asset_2018 / ws_n_2018)
print('traps: 2023 avg', 24.09 / 16, ' 24.09/1.871/... ', 24.09 / 1.871 / 4)

print('--- Q3: 2018 国有控股营收')
g = 78.6 - 56.2
print('国有营收增速', g, '2018营收', gy_rev / (1 + g / 100))
print('trap 78.6+56.2', gy_rev / (1 + (78.6 + 56.2) / 100))

print('--- Q4: 企业数增速')
for name, n23, inc in [('国有', 203, 81), ('港澳台', 61, 6), ('外商', 16, 4)]:
    print(name, '2018', n23 - inc, 'growth %.2f%%' % (inc / (n23 - inc) * 100))

print('--- Q5: 2018 资产结构')
tot23 = 2991.44
print('2023 sum of four', 1140.26 + 192.11 + 24.09 + 1634.97, 'count sum', 203 + 61 + 16 + 2474)
tot_g = 72.0 - 21.2
tot18 = tot23 / (1 + tot_g / 100)
my18 = 1634.97 / 1.72
gat18 = 192.11 / 1.055
ws18 = 24.09 / 1.871
gy18 = tot18 - my18 - gat18 - ws18
print('total growth', tot_g, 'total2018', tot18)
for name, v in [('国有(余量)', gy18), ('港澳台', gat18), ('外商', ws18), ('民营', my18)]:
    print('  %s %.2f  share %.2f%%  deg %.1f' % (name, v, v / tot18 * 100, v / tot18 * 360))
print('2023 shares (option A check):')
for name, v in [('国有', 1140.26), ('港澳台', 192.11), ('外商', 24.09), ('民营', 1634.97)]:
    print('  %s %.2f%%' % (name, v / tot23 * 100))
print('2023 revenue shares (option B check):')
for name, v in [('国有', 291.23), ('港澳台', 123.43), ('外商', 81.08), ('民营', 2019.41)]:
    print('  %s %.2f%%' % (name, v / gs_rev * 100))
# measured option D: black 161.4 deg, gray 31.1, sliver 2.7, white 164.8
print('Option D measured shares %:', [round(x / 360 * 100, 2) for x in (161.4, 31.1, 2.7, 164.8)])
print('Option A measured shares %:', [round(x / 360 * 100, 2) for x in (137.4, 22.8, 2.75, 197.05)])
# alternative: 国有 assets grown at 22.4% (revenue rate)
gy18b = 1140.26 / 1.224
s = gy18b + my18 + gat18 + ws18
print('alt (国有 /1.224) shares', [round(v / s * 100, 2) for v in (gy18b, gat18, ws18, my18)])
