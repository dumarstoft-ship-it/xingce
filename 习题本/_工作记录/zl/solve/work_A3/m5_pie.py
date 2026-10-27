from PIL import Image
import math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2732X-Z120_q.png').convert('L')
W,H = im.size
print(W,H)
# find pie bounding boxes: scan for dark pixels in columns 100-430
px = im.load()
def bbox(y0,y1,x0=100,x1=430):
    xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if px[x,y] < 80:
                xs.append(x); ys.append(y)
    return min(xs),max(xs),min(ys),max(ys)
for name,(y0,y1) in {'A':(100,425),'B':(445,770),'C':(790,1115),'D':(1140,H)}.items():
    x0,x1,yy0,yy1 = bbox(y0,y1)
    cx=(x0+x1)/2; cy=(yy0+yy1)/2; r=(x1-x0)/2
    # sample ring at 0.6 r
    rr = 0.6*r
    cls=[]
    for k in range(3600):
        a = math.radians(k/10)
        x = cx + rr*math.sin(a); y = cy - rr*math.cos(a)
        v = px[int(round(x)),int(round(y))]
        if v < 60: c='black'
        elif v < 150: c='dark'
        elif v < 215: c='light'
        else: c='white'
        cls.append(c)
    from collections import Counter
    cnt = Counter(cls)
    print(name, 'center',(round(cx),round(cy)),'r',round(r), {k: round(v/36,1) for k,v in cnt.items()})
