# MK2740X-M3
total_q = 40128.54; total_v = 13155.32
nz_q, au_q, ur_q, cl_q = 19327.58, 19208.14, 1226.35, 366.47
nz_v, ur_v, cl_v = 6573.92, 383.08, 100.69
print("sum qty of 4 countries", nz_q+au_q+ur_q+cl_q, "vs total", total_q)
au_v = total_v - nz_v - ur_v - cl_v
print("Q1 Aus value", au_v)
# consistency check via base period
base_total = total_v/(1-0.1219)
base_sum = nz_v/(1-0.2515) + au_v/1.0408 + ur_v/1.1602 + cl_v/(1+8.7431)
print("  base total", base_total, "sum of country bases", base_sum)
# also sub-category check
print("  categories qty sum", 39009.96+672.14+446.44, "value sum", 12709.07+262.35+183.90)

# Q2
lamb_share = 644.29/672.14
sheep_share = 5730.41/39009.96
print("Q2 lamb share", lamb_share*100, "sheep share", sheep_share*100, "diff", (lamb_share-sheep_share)*100)

# Q3
q2023 = 446.44/(1+10.6728)
v2023 = 183.90/(1+9.7401)
print("Q3 2023 goat qty", q2023, "value", v2023, "price", v2023/q2023)
print("  2024 price", 183.90/446.44, "factor", (1+10.6728)/(1+9.7401))

# Q4
jan23 = 19208.14/1.3377
dec23 = 19208.14/1.0338
print("Q4 jan23", jan23, "dec23", dec23, "growth", (dec23/jan23-1)*100, "=", (1.3377/1.0338-1)*100)

# Q5
dec_A = 9318.15/(1-0.2160)*0.2160
print("Q5A frozen bone-in decrease", dec_A)
print("Q5B mom abs:", {'NZ':18.22,'AU':3.18,'UR':3.06,'CL':15.14})
print("Q5C multiple", 1+21.4373)
print("Q5D share", 24929.62/40128.54*100)
