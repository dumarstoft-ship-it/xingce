# MK2733X-M3 N市银行 2023年（亿元）
rev, g_rev = 615.85, 6.40
np_, g_np = 255.35, 10.66
nii, g_nii = 409.07, 9.02
nonii, g_nonii = 206.78, 1.57
fee, g_fee = 57.67, -22.76
dep, g_dep = 15662.98, 20.76
corp, corp_sh = 11527.05, 73.6
priv, g_priv = 4135.93, 46.23
print("check 营收=利息+非息", nii + nonii, "对公+对私", corp + priv, "对公占比", corp / dep * 100)

print("== Q1 2022年营收-归母净利 ==")
r22, n22 = rev / (1 + g_rev / 100), np_ / (1 + g_np / 100)
print(r22, n22, r22 - n22)

print("== Q2 对公存款增速 ==")
dep22 = dep / (1 + g_dep / 100); priv22 = priv / (1 + g_priv / 100); corp22 = dep22 - priv22
g_corp = (corp / corp22 - 1) * 100
print("2022 总", dep22, "对私", priv22, "对公", corp22, "增速", g_corp)

print("== Q3 利息净收入增量不变 ==")
inc = nii * g_nii / (100 + g_nii)
print("增量", inc, "需年数", (600 - nii) / inc)
v = nii
for y in range(2024, 2031):
    v += inc
    print(y, round(v, 2))

print("== Q4 对公占比变化 ==")
s23 = corp / dep * 100; s22 = corp22 / dep22 * 100
print(s23, s22, s23 - s22)
print(" formula", s23 * (g_corp - g_dep) / (100 + g_corp))

print("== Q5 ==")
fee22 = fee / (1 + g_fee / 100); nonii22 = nonii / (1 + g_nonii / 100)
print("1) 2022手续费/非息", fee22, nonii22, fee22 / nonii22)
inc_rev = rev * g_rev / (100 + g_rev)
print("2) 营收增量", inc_rev, "利息增量", inc, "倍数", inc_rev / inc)
nii22 = nii / (1 + g_nii / 100)
print("3) 2022 利息/非息", nii22, nonii22, nii22 / nonii22, " 2023:", nii / nonii)
