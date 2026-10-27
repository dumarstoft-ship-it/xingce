from PIL import Image
import numpy as np
im = np.array(Image.open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/crops/zl/MK2709X-Z111_p2.png').convert('L'))
y0 = 377   # x axis (value 0)
# find axis top precisely
col = np.where(im[:377,131] < 100)[0]
ytop = col.min()
print("axis top y:", ytop)
unit = (y0 - ytop)/3.0
print("px per unit:", unit)
bars = {"2020":(166,233),"2021":(303,371),"2022":(439,507),"2023":(575,643),"2024":(713,781)}
for k,(a,b) in bars.items():
    # top edge: look at a column near left edge+3 and near right edge-3, find first dark row from top
    tops = []
    for x in [a+4, a+10, b-10, b-4]:
        ys = np.where(im[50:377, x] < 120)[0] + 50
        tops.append(ys.min() if len(ys) else None)
    # use left vertical edge: first dark row in edge column
    ys_edge = np.where(im[50:377, a] < 120)[0] + 50
    t = ys_edge.min()
    print(k, "tops in interior cols:", tops, " left edge top:", t, " value ~", (y0 - t)/unit)
