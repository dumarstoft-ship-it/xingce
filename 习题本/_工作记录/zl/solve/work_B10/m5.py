# MK2732X-M1 X地区房地产
rows = {
 "投资":   ((1168.53, 0.008), (823.05, -0.006)),
 "施工":   ((15375.68, -0.044), (10467.79, -0.043)),
 "竣工":   ((1297.88, 0.137), (950.00, 0.221)),
 "销售面积": ((1903.23, 0.255), (1711.29, 0.242)),
 "销售额":  ((1167.46, 0.321), (989.70, 0.294)),
}
# Q1 投资中住宅占比变化
(T, rt), (Rv, rr) = rows["投资"]
now = Rv/T; prev = (Rv/(1+rr))/(T/(1+rt))
print("Q1 share now", now, "prev", prev, "diff pp", 100*(now-prev), " formula", 100*now*(rr-rt)/(1+rr))
# Q2 2022 非住宅施工面积
(T, rt), (Rv, rr) = rows["施工"]
T22, R22 = T/(1+rt), Rv/(1+rr)
print("Q2 T22", T22, "R22", R22, "nonres22", T22-R22, " trap nonres23", T-Rv)
# Q3 住宅增速 vs 非住宅增速
cnt = 0
for k, ((T, rt), (Rv, rr)) in rows.items():
    nr_now = T-Rv; nr_prev = T/(1+rt) - Rv/(1+rr)
    g_nr = nr_now/nr_prev-1
    faster = rr > g_nr
    cnt += faster
    print("Q3", k, "res", rr, "nonres", round(g_nr,5), "total", rt, "res faster?", faster)
print("Q3 count", cnt)
# Q4 非住宅销售额增量
(T, rt), (Rv, rr) = rows["销售额"]
incT = T*rt/(1+rt); incR = Rv*rr/(1+rr)
print("Q4 incT", incT, "incR", incR, "nonres inc", incT-incR, " check", (T-Rv)-(T/(1+rt)-Rv/(1+rr)))
# Q5 ① 2022 非住宅销售面积占比
(Ta, ra), (Ra, rra) = rows["销售面积"]
Ta22, Ra22 = Ta/(1+ra), Ra/(1+rra)
print("Q5-1 2022 nonres share of sales area", (Ta22-Ra22)/Ta22)
(Ts, rs), (Rs, rrs) = rows["销售额"]
Ts22 = Ts/(1+rs)
print("Q5-2 2022 unit price (亿元/万m2 -> 元/m2)", Ts22/Ta22, Ts22/Ta22*1e4)
print("Q5-3 needs 2021 data: only 2023 growth of 住宅单价 computable:", (1+rrs)/(1+rra)-1)
