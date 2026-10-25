import math, sys, json
def pts(A,B,C,p,q,r):
    D=(B[0]+p*(B[0]-A[0]), B[1]+p*(B[1]-A[1]))
    E=(C[0]+q*(C[0]-B[0]), C[1]+q*(C[1]-B[1]))
    F=(A[0]+r*(A[0]-C[0]), A[1]+r*(A[1]-C[1]))
    return D,E,F
def make_svg(A,B,C,p,q,r,W=300,H=250,m=26,fill=True,rot=0.0,flip=False):
    D,E,F=pts(A,B,C,p,q,r)
    P={'A':A,'B':B,'C':C,'D':D,'E':E,'F':F}
    # rotate / flip, then y up -> svg y down
    c,s=math.cos(rot),math.sin(rot)
    for k,(x,y) in list(P.items()):
        x2,y2=c*x-s*y, s*x+c*y
        if flip: x2=-x2
        P[k]=(x2,-y2)
    xs=[v[0] for v in P.values()]; ys=[v[1] for v in P.values()]
    sc=min((W-2*m)/(max(xs)-min(xs)), (H-2*m)/(max(ys)-min(ys)))
    ox=(W-sc*(max(xs)-min(xs)))/2 - sc*min(xs); oy=(H-sc*(max(ys)-min(ys)))/2 - sc*min(ys)
    Q={k:(round(ox+sc*v[0],1), round(oy+sc*v[1],1)) for k,v in P.items()}
    def cen(*ks): return (sum(Q[k][0] for k in ks)/len(ks), sum(Q[k][1] for k in ks)/len(ks))
    gD=cen('D','E','F'); gA=cen('A','B','C')
    lab=[]
    for k in 'DEF':
        x,y=Q[k]; dx,dy=x-gD[0],y-gD[1]; n=math.hypot(dx,dy)
        lab.append((k,x+13*dx/n,y+13*dy/n))
    for k in 'ABC':
        x,y=Q[k]; dx,dy=x-gA[0],y-gA[1]; n=math.hypot(dx,dy)
        lab.append((k,x+12*dx/n,y+12*dy/n))
    f=lambda k: f"{Q[k][0]},{Q[k][1]}"
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Noto Sans SC, Arial, sans-serif" font-size="15" fill="#111">']
    if fill:
        out.append(f'<polygon points="{f("A")} {f("B")} {f("C")}" fill="#d9d9d9" stroke="none"/>')
    out.append(f'<polygon points="{f("D")} {f("E")} {f("F")}" fill="none" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(f'<path d="M{f("A")} L{f("D")} M{f("B")} L{f("E")} M{f("C")} L{f("F")}" fill="none" stroke="#111" stroke-width="1.3"/>')
    for k,x,y in lab:
        out.append(f'<text x="{round(x,1)}" y="{round(y+5,1)}" text-anchor="middle">{k}</text>')
    out.append('</svg>')
    return '\n'.join(out), Q
if __name__=='__main__':
    cfg=json.loads(sys.argv[1])
    svg,Q=make_svg(**cfg)
    print(svg)
