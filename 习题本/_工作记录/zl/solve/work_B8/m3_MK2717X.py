# MK2717X-M1 洗护用品
on = {2017:605, 2018:722, 2019:874, 2020:1096, 2021:1249}
off = {2017:1286, 2018:1300, 2019:1349, 2020:1355, 2021:1430}
tot = {y: on[y]+off[y] for y in on}
print("totals", tot)
print("Q1 sum", sum(tot.values()), "online sum", sum(on.values()), "offline sum", sum(off.values()))
for y in range(2018,2022):
    print("Q2", y, tot[y]/tot[y-1]-1, "1.1*prev", tot[y-1]*1.1)
# Q3
don = on[2021]-on[2020]; doff = off[2021]-off[2020]
print("Q3 increments", don, doff)
o, f = on[2021], off[2021]
for y in range(2022, 2027):
    o += don; f += doff
    print("  ", y, o, f, "offline share", f/(o+f))
# Q4
for y in on:
    print("Q4", y, "off share", off[y]/tot[y], "on share", on[y]/tot[y], "diff pp", (off[y]-on[y])/tot[y]*100)
# Q5
for y in range(2018,2021):
    print("Q5A", y, "on g", on[y]/on[y-1]-1, "off g", off[y]/off[y-1]-1)
print("Q5B on share 2019", on[2019]/tot[2019], "2020", on[2020]/tot[2020])
print("Q5C inc2021", on[2021]-on[2020], "inc2018", on[2018]-on[2017], "ratio", (on[2021]-on[2020])/(on[2018]-on[2017]))
print("Q5D online sum", sum(on.values()))
