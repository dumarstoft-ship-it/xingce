# MK2704X-M3
years = [2018,2019,2020,2021,2022]
non = [5109,5670,6296,6688,7105]
yes = [1925,1915,2136,2189,2214]
gr = [11.5,7.8,11.2,5.3,5.0]
tot = [a+b for a,b in zip(non,yes)]
for i,y in enumerate(years):
    s = yes[i]/tot[i]*100
    line = f"{y} total {tot[i]} share_yes {s:.3f}%"
    if i>0:
        line += f" total_g {(tot[i]/tot[i-1]-1)*100:.2f} (chart {gr[i]}) yes_g {(yes[i]/yes[i-1]-1)*100:.2f} non_g {(non[i]/non[i-1]-1)*100:.3f} non_inc {non[i]-non[i-1]}"
    print(line)
# Q2
print("Q2 org growth", (1.008/1.02-1)*100)
# Q4
print("Q4 2019 org", 89.1-2.5, "share", tot[1]/((89.1-2.5)*1e4)*100)
# Q5
print("Q5A per org", 1108.3/89.1)
print("Q5B 2022 share", tot[4]/(89.1e4)*100)
print("Q5C 2017 total", tot[0]/1.115)
print("Q5D inc 2020", non[2]-non[1], "inc 2019", non[1]-non[0])
