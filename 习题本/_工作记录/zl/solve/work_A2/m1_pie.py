from PIL import Image
import numpy as np, math
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2740X-Z115_q.png').convert('L')).astype(float)
H,W = im.shape
regions = {'A':(170,480),'B':(495,800),'C':(820,1125),'D':(1130,1426)}
def classify(cx,cy,r,ang):
    # angle measured clockwise from 12 o'clock
    th = math.radians(ang)
    x = cx + r*math.sin(th); y = cy - r*math.cos(th)
    xi, yi = int(round(x)), int(round(y))
    win = im[yi-3:yi+4, xi-3:xi+4]
    m = win.mean(); s = win.std()
    if s > 25: return 'H'
    if m < 80: return 'K'
    if m > 235: return 'W'
    if 150 < m < 220: return 'G'
    return '?'
for k,(y0,y1) in regions.items():
    sub = im[y0:y1, 100:450]
    dark = sub < 120
    ys,xs = np.where(dark)
    x0,x1,yy0,yy1 = xs.min()+100, xs.max()+100, ys.min()+y0, ys.max()+y0
    cx = (x0+x1)/2; cy=(yy0+yy1)/2; R = ((x1-x0)+(yy1-yy0))/4
    print(k, 'bbox', x0,x1,yy0,yy1, 'center', cx, cy, 'R', R)
    for rr in [0.5,0.7,0.85]:
        seq = []
        step=0.25
        angs = np.arange(0,360,step)
        labs = [classify(cx,cy,R*rr,a) for a in angs]
        # find transitions
        segs=[]
        cur=labs[0]; start=0
        for i,l in enumerate(labs):
            if l!=cur:
                segs.append((cur, angs[start], angs[i]))
                cur=l; start=i
        segs.append((cur, angs[start], 360))
        print('  r=',rr, [(c, round(a,2), round(b,2), round(b-a,2)) for c,a,b in segs if b-a>1.5])
