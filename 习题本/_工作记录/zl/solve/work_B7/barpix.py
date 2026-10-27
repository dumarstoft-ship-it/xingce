import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('L')
W,H = im.size
print(W,H)
x0,x1,y0,y1 = map(int, sys.argv[2:6])
# for each column, find dark pixel rows
for x in range(x0,x1, int(sys.argv[6]) if len(sys.argv)>6 else 5):
    dark = [y for y in range(y0,y1) if im.getpixel((x,y))<128]
    if dark:
        print(x, dark[0], dark[-1], len(dark))
