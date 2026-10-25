# Build the SVG for D07-math-2-v08: irregular quadrilateral split by its diagonals.
# Regions clockwise from the top: 甲 (top), 乙 (right), 丙 (bottom), 丁 (left).
# Proportions chosen so the drawn areas match 150/120/100/125: OA:OC = 5:4, OB:OD = 6:5.
import math, json, sys
cx, cy = 128, 98
u, v = 23, 18.5
thA, thB = math.radians(158), math.radians(47)
P = {
  'A': (5*u*math.cos(thA), 5*u*math.sin(thA)),
  'B': (6*v*math.cos(thB), 6*v*math.sin(thB)),
  'C': (4*u*math.cos(thA+math.pi), 4*u*math.sin(thA+math.pi)),
  'D': (5*v*math.cos(thB+math.pi), 5*v*math.sin(thB+math.pi)),
}
def svg(p): return (cx+p[0], cy-p[1])
S = {k: svg(p) for k, p in P.items()}
O = (cx, cy)
def area(a,b,c): return abs((b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]))/2
reg = {'甲':('A','B'),'乙':('B','C'),'丙':('C','D'),'丁':('D','A')}
areas = {k: area(O,S[a],S[b]) for k,(a,b) in reg.items()}
print({k: round(x,1) for k,x in areas.items()}, 'ratios', {k: round(x/areas['丙']*100,1) for k,x in areas.items()})
xs=[p[0] for p in S.values()]; ys=[p[1] for p in S.values()]
print('bbox', min(xs),max(xs),min(ys),max(ys))
def f(x): return f'{x:.1f}'
poly = ' '.join(f'{f(S[k][0])},{f(S[k][1])}' for k in 'ABCD')
lab = []
for k,(a,b) in reg.items():
    gx = (O[0]+S[a][0]+S[b][0])/3; gy = (O[1]+S[a][1]+S[b][1])/3
    lab.append(f'<text x="{f(gx)}" y="{f(gy+6)}">{k}</text>')
W, H = 250, 190
out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="四边形被两条对角线分成甲乙丙丁四块">'
       f'<g fill="none" stroke="#111" stroke-width="2" stroke-linejoin="round">'
       f'<polygon points="{poly}"/>'
       f'<line x1="{f(S["A"][0])}" y1="{f(S["A"][1])}" x2="{f(S["C"][0])}" y2="{f(S["C"][1])}"/>'
       f'<line x1="{f(S["B"][0])}" y1="{f(S["B"][1])}" x2="{f(S["D"][0])}" y2="{f(S["D"][1])}"/></g>'
       f'<g font-family="\'Noto Sans SC\', sans-serif" font-size="17" fill="#111" text-anchor="middle">' + ''.join(lab) + '</g></svg>')
open(sys.argv[1], 'w').write(out)
print(out)
