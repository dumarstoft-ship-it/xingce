# MK2710X-M3
jun=3.49; may=jun/1.012; apr_ring=may/1.012; apr_sub=10.34-jun-may
print("Q1 May", may, " Apr via ring", apr_ring, " Apr via Q2-sum", apr_sub)
ex=11.46; im=8.64
bex=ex/1.037; bim=im/0.999
base=bex+bim
print("Q2 base", base, " growth%", (20.10/base-1)*100, " check ex+im:", ex+im)
g=20.10/base-1
s23=0.527; s22=0.527-0.033
print("Q3 private growth via shares%", ((s23/s22)*(1+g)-1)*100, " via values%", (10.59/(s22*base)-1)*100)
eu=2.75*1.9/101.9; us=2.25*(-8.4)/91.6
print("Q4 EU inc(yi)", eu*1e4, " US inc(yi)", us*1e4, " diff(yi)", (eu-us)*1e4)
print("Q5 (1) Q2 qoq%", (10.34/9.76-1)*100)
print("Q5 (2) pp diff", 52.7-(30.7+16.4), " value diff(wan yi)", 10.59-(6.16+3.29), " ratio", 52.7/(30.7+16.4))
print("Q5 (3) share%", (3.08+2.75+2.25)/20.10*100)
