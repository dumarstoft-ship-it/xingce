# MK2733X-M3
rev23, rg = 615.85, 0.0640
np23, ng = 255.35, 0.1066
nii23, nig = 409.07, 0.0902
dep23, dg = 15662.98, 0.2076
corp23 = 11527.05
priv23, pg = 4135.93, 0.4623
nonint23, nong = 206.78, 0.0157
fee23, feeg = 57.67, -0.2276
# Q1
rev22 = rev23/(1+rg); np22 = np23/(1+ng)
print("Q1 rev22", rev22, "np22", np22, "diff", rev22-np22)
# Q2
dep22 = dep23/(1+dg); priv22 = priv23/(1+pg); corp22 = dep22-priv22
print("Q2 dep22", dep22, "priv22", priv22, "corp22", corp22, "growth", (corp23/corp22-1)*100)
print("  check corp23+priv23", corp23+priv23, "share23", corp23/dep23*100)
# Q3
nii22 = nii23/(1+nig); inc = nii23-nii22
print("Q3 nii22", nii22, "inc", inc)
v = nii23
for y in range(2024, 2032):
    v += inc
    print("  ", y, round(v,2))
print("  n needed", (600-nii23)/inc)
# Q4
s23 = corp23/dep23; s22 = corp22/dep22
print("Q4 share23", s23*100, "share22", s22*100, "diff", (s23-s22)*100)
print("  via 73.6 given", 73.6 - s22*100)
# Q5
nonint22 = nonint23/(1+nong); fee22 = fee23/(1+feeg)
print("Q5-1 nonint22", nonint22, "fee22", fee22, "share", fee22/nonint22*100)
rev_inc = rev23-rev22
print("Q5-2 rev inc", rev_inc, "nii inc", inc, "ratio", rev_inc/inc, " rev23/nii23", rev23/nii23, " revinc/nii23", rev_inc/nii23)
print("Q5-3 nii22/nonint22", nii22/nonint22, " 2023 ratio", nii23/nonint23)
