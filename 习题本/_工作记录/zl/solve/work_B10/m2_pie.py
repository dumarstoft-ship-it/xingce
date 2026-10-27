# Measure pie sector boundary angles for MK2711X Q4 options
from PIL import Image
import numpy as np, math
im = Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2711X-Z114_q.png').convert('L')
a = np.array(im).astype(float)
boxes={'A':(100,95,370,360),'B':(100,375,370,640),'C':(100,655,370,920),'D':(100,935,370,1196)}
for k,(x0,y0,x1,y1) in boxes.items():
    sub = a[y0:y1, x0:x1]
    dark = sub < 128
    ys, xs = np.nonzero(dark)
    # circle bbox from outline extremes
    cx = (xs.min()+xs.max())/2; cy = (ys.min()+ys.max())/2
    R = ((xs.max()-xs.min())+(ys.max()-ys.min()))/4
    # refine center: the vertical radius line from top at 12 o'clock -> x of center
    # find convergence: column with most dark pixels in upper half near cx
    # radial scan
    res = []
    for t10 in range(0, 3600):
        th = math.radians(t10/10)  # angle clockwise from 12 o'clock
        cnt = 0; tot = 0
        for r in np.linspace(0.25*R, 0.92*R, 60):
            x = cx + r*math.sin(th); y = cy - r*math.cos(th)
            xi, yi = int(round(x)), int(round(y))
            if 0<=yi<sub.shape[0] and 0<=xi<sub.shape[1]:
                tot += 1; cnt += sub[yi,xi] < 140
        res.append(cnt/tot)
    res = np.array(res)
    # print peaks (boundaries) where fraction > 0.6
    peaks = []
    for i in range(3600):
        if res[i] > 0.55 and res[i] >= res[i-1] and res[i] >= res[(i+1)%3600]:
            peaks.append((i/10, round(res[i],2)))
    print(k, 'center', (cx+x0, cy+y0), 'R', R)
    print('  peaks', peaks)
