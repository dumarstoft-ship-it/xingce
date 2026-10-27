from PIL import Image
import numpy as np
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L'))
y0 = 377; ytop = 64; unit = (y0-ytop)/3
bars = {"2020":(166,233),"2021":(303,371),"2022":(439,507),"2023":(575,643),"2024":(713,781)}
for k,(a,b) in bars.items():
    cand = []
    for y in range(60, 377):
        frac = (im[y, a+1:b] < 140).mean()
        if frac > 0.7: cand.append((y, round(frac,2)))
    print(k, cand[:3], "-> value", [(y0-c[0])/unit for c in cand[:1]])
