from math import comb
# v01 3x4 lattice
tot=comb(12,3)
rows=3*comb(4,3); cols=4*comb(3,3); diag3=4  # 2 lines per direction with exactly 3 points
diag2_lines=4  # lines with only 2 points (2 per direction)
print('v01 correct', tot-rows-cols-diag3)
print('v01 miss diagonals', tot-rows-cols)
print('v01 also subtract 2-point diagonals', tot-rows-cols-diag3-diag2_lines)
print('v01 one per row/line', tot-(3+4+4))
print('v01 only one diag direction', tot-rows-cols-2)
# positive method check: 2+1 distribution and 1+1+1
pos=3*comb(4,2)*8 + (4**3-4-4)
print('v01 positive', pos)
# v02
total=comb(9,3)*comb(6,3)//2
comp=1*(comb(6,3)//2) + comb(6,3)*1
print('v02 total',total,'comp',comp,'ans',total-comp)
print('v02 A-groups distinct', comb(9,3)*comb(6,3) - (comb(6,3)*1*... if False else 3*comb(6,3)))
print('v02 all de-ordered', comb(9,3)*comb(6,3)//6 - comb(6,3)//2)
print('v02 complement in labeled frame', total-3*comb(6,3))
print('v02 ignore', total)
# v03
print('v03 correct', comb(5+3,3), 'borrow', comb(8,3))
print('v03 exact', comb(5+2,2))
print('v03 must leave', comb(8,3)-comb(7,2), 'forgot borrow', comb(7,3))
print('v03 reserve also >=2', comb(11-8+3,3))
print('v03 sum', sum(comb(T-6+2,2) for T in range(6,12)), [comb(T-6+2,2) for T in range(6,12)])
