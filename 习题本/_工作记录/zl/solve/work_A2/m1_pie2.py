from PIL import Image
import numpy as np, math
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2740X-Z115_q.png').convert('L')).astype(float)
pies = {'A':(256.0,323.0,141.0),'B':(253.5,647.5,141.5),'C':(254.0,974.0,142.0),'D':(255.5,1280.5,141.5)}
def val(x,y):
    # bilinear
    x0=int(math.floor(x)); y0=int(math.floor(y)); dx=x-x0; dy=y-y0
    return (im[y0,x0]*(1-dx)*(1-dy)+im[y0,x0+1]*dx*(1-dy)+im[y0+1,x0]*(1-dx)*dy+im[y0+1,x0+1]*dx*dy)
exp = [96.84,170.01,62.39,30.76]
for k,(cx,cy,R) in pies.items():
    res = {}
    for r in range(40,126,5):
        angs = np.arange(0,360,0.1)
        v = np.array([val(cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a))) for a in angs])
        dark = v < 70
        # find runs of dark
        runs=[]; inrun=False
        for i,d in enumerate(dark):
            if d and not inrun: s=i; inrun=True
            if not d and inrun: runs.append((angs[s],angs[i-1])); inrun=False
        if inrun: runs.append((angs[s],angs[-1]))
        res[r]=[(round(a,1),round(b,1)) for a,b in runs]
    print(k)
    for r in res: print('  ',r,res[r])
