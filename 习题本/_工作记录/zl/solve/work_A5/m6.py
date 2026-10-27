# MK2721X-M1 企业发明专利产业化 2023
avg=829.6; avg_g=3.8; domestic=811.4; private=866.6; other=706.4
brand=1067.1; oem=462.1; brand_roi=390.8; diff_pp=96.9
cxy_prem=24.5; cxy_rd=266.9; cxy_rd_prem=41.6
print("Q1 2022 avg", avg/(1+avg_g/100))
print("Q2 private:other =", (domestic-other)/(private-domestic), " (", domestic-other, "/", private-domestic, ")")
oem_roi = brand_roi-diff_pp
print("Q3 oem roi", oem_roi, " oem R&D", oem/(1+oem_roi/100), " brand R&D", brand/(1+brand_roi/100))
rd_all = cxy_rd/(1+cxy_rd_prem/100)
print("Q4 overall R&D", rd_all, " ROI", (avg-rd_all)/rd_all*100)
print("Q5 A", (private/domestic-1)*100, " B", brand/oem, " C", avg*(1+cxy_prem/100))
