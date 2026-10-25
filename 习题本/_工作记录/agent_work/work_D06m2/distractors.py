from fractions import Fraction as F
f=float
print('v01 forgot C21:', (F(2,5)-F(1,4))/F(1,4), ' forgot both-pass:', F(2,5)/F(1,2), ' stop early:', F(2,5)-F(1,4))
print('v02 no retake', f(F(8,10)*F(6,10)), ' theory retake only', f(F(96,100)*F(6,10)), ' prac retake only', f(F(8,10)*F(84,100)))
p=F(6,10); q=1-p
print('v03 2:0 only', f(p*p), ' one order', f(p*p+p*q*p), ' C32', f(p*p+3*p*p*q), ' formula', f(p*p*(3-2*p)))
print('v04 forgot (1-p):', (F(40)-25)/75, ' diff only', F(15,100), ' reversed', (F(75)-40)/(75-25))
print('v05 simple avg', f((F(2)+3+5)/3), ' reversed weights', f(F(2,10)*2+F(3,10)*3+F(5,10)*5))
print('v06 fixed mode', f(F(6,10)*F(81,100)+F(4,10)*F(36,100)), ' same-mode only', f(F(54,100)**2+F(24,100)**2), ' one day', f(F(78,100)))
print('v07 prod share', F(2,10), ' rate share', F(5,10), ' line2', F(9,29), ' line1', F(10,29))
tp=F(2,100)*F(95,100); fp=F(98,100)*F(5,100)
print('v08 tp/fp', f(tp/fp), ' correct', f(tp/(tp+fp)))
print('v09 1D', 12/60, 24/60, ' fail', (48/60)**2)
print('v10 /10', 410/10, ' 4-level avg', (200+50+10+0)/4, ' 3-level avg', (200+50+10)/3, ' each-1', (200+50+10)/20)
print('v11 forgot self 20%:', 10-6, ' forgot premium:', 10-0.2*10, ' swapped 80/20: ins=', 6+0.2*50*0.8, '-> no-ins better by', 6+0.2*50*0.8-10)
print('real wrong: simple avg', (70+20)/2, ' swapped', 0.7*0.7+0.3*0.2)
