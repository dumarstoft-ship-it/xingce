import sys, math
from PIL import Image
im = Image.open(sys.argv[1]).convert('L')
x0,y0,x1,y1 = map(int, sys.argv[2:6])
# find circle bounding box: dark pixels in region
dark = [(x,y) for x in range(x0,x1) for y in range(y0,y1) if im.getpixel((x,y))<90]
xs = [p[0] for p in dark]; ys=[p[1] for p in dark]
L,R,T,B = min(xs),max(xs),min(ys),max(ys)
cx,cy = (L+R)/2,(T+B)/2; rad = ((R-L)+(B-T))/4
print("bbox",L,R,T,B,"center",cx,cy,"r",rad)
# sample angles at several radii; find black line crossings
res = {}
for frac in [0.4,0.55,0.7,0.85]:
    r = rad*frac
    hits=[]
    prev=False
    for i in range(3600):
        a = i/10.0
        # angle measured clockwise from 12 o'clock
        x = cx + r*math.sin(math.radians(a)); y = cy - r*math.cos(math.radians(a))
        v = im.getpixel((int(round(x)),int(round(y))))
        d = v<90
        if d and not prev: start=a
        if not d and prev: hits.append(round((start+a-0.1)/2,1))
        prev=d
    res[frac]=hits
    print(frac, hits)
