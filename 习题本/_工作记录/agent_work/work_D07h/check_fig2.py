# sanity check: the figure for v02 matches the stem (collinearity + extension ratios), no numbers shown
import re, math
s = open('fig2_final.svg').read()
poly = re.findall(r'points="([^"]+)"', s)
tri_abc = [tuple(map(float, p.split(','))) for p in poly[0].split()]
tri_def = [tuple(map(float, p.split(','))) for p in poly[1].split()]
A, B, C = tri_abc
D, E, F = tri_def
def d(P, Q): return math.dist(P, Q)
def col(P, Q, R): return abs((Q[0]-P[0])*(R[1]-P[1]) - (R[0]-P[0])*(Q[1]-P[1])) / (d(P, Q) * d(P, R))
print('A-B-D collinear', round(col(A, B, D), 4), 'BD/AB', round(d(B, D) / d(A, B), 3), 'B between A,D', abs(d(A,B)+d(B,D)-d(A,D))<0.05)
print('B-C-E collinear', round(col(B, C, E), 4), 'CE/BC', round(d(C, E) / d(B, C), 3), 'C between B,E', abs(d(B,C)+d(C,E)-d(B,E))<0.05)
print('C-A-F collinear', round(col(C, A, F), 4), 'AF/CA', round(d(A, F) / d(C, A), 3), 'A between C,F', abs(d(C,A)+d(A,F)-d(C,F))<0.05)
def area(P, Q, R): return abs((Q[0]-P[0])*(R[1]-P[1]) - (R[0]-P[0])*(Q[1]-P[1])) / 2
print('area ratio in figure', round(area(D, E, F) / area(A, B, C), 2))
print('text labels', re.findall(r'>([^<]+)</text>', s))
print('digits in svg text?', any(ch.isdigit() for t in re.findall(r'>([^<]+)</text>', s) for ch in t))
