# MK2734X-M1: 2024 employment
urban_pop, urb_rate = 94350, 0.67
E24 = 73439
U_emp, dU = 47345, 1074
R_emp, dR = 26094, -2699
T3, dT3, T3sh = 35866, 60, 0.488
fem, femsh = 31900, 0.434
print("check sum 24:", U_emp+R_emp)
E20 = (U_emp-dU) + (R_emp-dR)
print("Q1 E20=%d growth=%.4f%% ; alt (/E24)=%.4f%%" % (E20, (E24/E20-1)*100, (dU+dR)/E24*100))
pop = urban_pop/urb_rate
print("Q2 pop=%.2f fem share=%.4f%% ; via 43.4%%: %.4f%%" % (pop, fem/pop*100, E24*femsh/pop*100))
mw24, mg = 29973, 0.049
print("Q3 inc=%.3f" % (mw24*mg/(1+mg)))
s24 = T3/E24; s20 = (T3-dT3)/E20
print("Q4 s24=%.4f%% (given 48.8) s20=%.4f%% diff=%.4f pp; using 48.8: %.4f" % (s24*100, s20*100, (s24-s20)*100, 48.8-s20*100))
# Q5
r = 0.051
U = U_emp*r/(1-r)
print("Q5A unemployed=%.2f ; trap urban_pop*r=%.2f ; 47345*r=%.2f" % (U, urban_pop*r, U_emp*r))
male = E24 - fem
print("Q5B male=%d ratio m/f=%.4f (4:3=%.4f); by share=%.4f" % (male, male/fem, 4/3, (1-femsh)/femsh))
print("Q5C 2020 rate = %.1f%%" % (5.1+0.5))
mw20 = mw24/(1+mg)
print("Q5D mw20=%.2f 13000/mw20=%.4f%%" % (mw20, 13000/mw20*100))
