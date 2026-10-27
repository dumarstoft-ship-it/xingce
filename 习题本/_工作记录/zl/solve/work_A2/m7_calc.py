# MK2738X-M2
mon=[2,3,4,5,6]
n={6:9660,5:9654,4:9655,3:9645,2:9642}
A={6:50906.0,5:50496.1,4:50472.4,3:50392.7,2:49889.6}
L={6:20405.4,5:20126.9,4:20183.7,3:20093.6,2:19651.4}
S={6:2025.6,5:1635.1,4:1320.8,3:1008.2,2:634.4}
M={6:809.0,5:663.9,4:535.8,3:408.3,2:260.5}
F={6:22.2,5:24.6,4:16.3,3:15.5,2:14.0}
print('Q1', A[6]/n[6])
for m in [3,4,5,6]: print('Q2', m, L[m]/A[m]*100)
sm={m:S[m]-S[m-1] for m in [3,4,5,6]}; mm={m:M[m]-M[m-1] for m in [3,4,5,6]}; fm={m:F[m]-F[m-1] for m in [3,4,5,6]}
print('monthly sales', sm); print('monthly mgmt', mm); print('monthly fin', fm)
print('Q3 Apr fin mom', (fm[4]/fm[3]-1)*100)
s6=S[6]+M[6]+F[6]; s2=S[2]+M[2]+F[2]
print('Q4', s6, s2, s6/s2)
print('A n', [n[m] for m in mon])
print('B equity', {m:round(A[m]-L[m],1) for m in mon})
print('D monthly ratio', {m:sm[m]/mm[m] for m in [3,4,5,6]}, 'cum ratio', {m:S[m]/M[m] for m in [3,4,5,6]})
