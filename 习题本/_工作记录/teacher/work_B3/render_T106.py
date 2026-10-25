# 用与SVG相同的几何参数栅格化，检查阴影是否恰为三者公共部分
import sys
from PIL import Image, ImageDraw
S = 3
W, H = 200, 215
RECT = (15, 18, 115, 115)
TRI = [(50, 78), (147, 25), (148, 135)]
CIR = (117, 135, 67)

def in_rect(x, y):
    return RECT[0] <= x <= RECT[2] and RECT[1] <= y <= RECT[3]

def in_tri(x, y):
    (x1, y1), (x2, y2), (x3, y3) = TRI
    def s(ax, ay, bx, by):
        return (bx - ax) * (y - ay) - (by - ay) * (x - ax)
    d1, d2, d3 = s(x1, y1, x2, y2), s(x2, y2, x3, y3), s(x3, y3, x1, y1)
    return (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0)

def in_cir(x, y):
    cx, cy, r = CIR
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

img = Image.new('RGB', (W * S, H * S), 'white')
px = img.load()
regions = {}
for X in range(W * S):
    for Y in range(H * S):
        x, y = (X + .5) / S, (Y + .5) / S
        key = (in_rect(x, y), in_tri(x, y), in_cir(x, y))
        regions[key] = regions.get(key, 0) + 1
        if all(key):
            px[X, Y] = (189, 189, 189)
d = ImageDraw.Draw(img)
d.rectangle([c * S for c in RECT], outline='black', width=4)
d.polygon([(a * S, b * S) for a, b in TRI], outline='black', width=4)
cx, cy, r = CIR
d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], outline='black', width=4)
for t, (x, y) in {'B': (22, 22), 'A': (129, 40), 'C': (112, 180)}.items():
    d.text((x * S, y * S), t, fill='black', font_size=36)
img.save(sys.argv[1])
names = {(1, 0, 0): 'B only', (0, 1, 0): 'A only', (0, 0, 1): 'C only', (1, 1, 0): 'A&B only',
         (1, 0, 1): 'B&C only', (0, 1, 1): 'A&C only', (1, 1, 1): 'A&B&C (shaded)'}
for k, n in names.items():
    print(n, regions.get(tuple(bool(v) for v in k), 0) / S / S)
