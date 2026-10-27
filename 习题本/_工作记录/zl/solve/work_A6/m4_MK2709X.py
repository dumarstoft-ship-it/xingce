# MK2709X-M1: 在线外卖用户规模 & 团餐行业
years = [2018,2019,2020,2021,2022,2023,2024]
users = [4.1,4.0,4.2,5.4,5.2,5.5,5.9]
share = [49.0,44.0,42.3,52.7,48.8,49.9,53.4]
net = {y: u/(s/100) for y,u,s in zip(years,users,share)}
for y in years: print("net %d = %.4f" % (y, net[y]))
# Q1
print("Q1 diff 2024-2020 = %.4f" % (net[2024]-net[2020]))
# Q2 growth of users 2020-2023
ug = {years[i]: users[i]/users[i-1]-1 for i in range(1,len(years))}
for y in [2020,2021,2022,2023]: print("Q2 user growth %d = %.4f%%" % (y, ug[y]*100))
# Q3 team-meal projection
s = {2020:1.5,2021:1.8,2022:2.1,2023:2.4,2024:2.7}
r = {2020:-1.9,2021:16.3,2022:15.2,2023:15.1,2024:14.8}
inc_sub = s[2024]-s[2023]
inc_f = s[2024]*r[2024]/(100+r[2024])
for name, inc in [("subtract",inc_sub),("formula",inc_f)]:
    v = s[2024]; y = 2024
    while v <= 4:
        y += 1; v += inc
    print("Q3 %s inc=%.4f first >4 in %d (value %.3f); n_needed=%.3f" % (name, inc, y, v, (4-2.7)/inc))
# Q4 net growth
ng = {years[i]: net[years[i]]/net[years[i-1]]-1 for i in range(1,len(years))}
for y in years[1:]: print("Q4 net growth %d = %.4f%%" % (y, ng[y]*100))
# Q5
for y in [2021,2022,2023,2024]:
    print("Q5A inc %d formula=%.4f subtract=%.2f" % (y, s[y]*r[y]/(100+r[y]), s[y]-s[y-1]))
s2019 = 1.5/(1-0.019)
print("Q5B 2019=%.4f growth 2024/2019=%.4f%%" % (s2019, (2.7/s2019-1)*100))
import functools
comp = functools.reduce(lambda a,b:a*b, [1+r[y]/100 for y in r])
print("Q5B compound=%.4f%%" % ((comp-1)*100))
ups = [y for y in years[1:] if ug[y] > ng[y]]
print("Q5C years user growth > net growth:", ups)
print("Q5D total=%.2f" % sum(s.values()))
