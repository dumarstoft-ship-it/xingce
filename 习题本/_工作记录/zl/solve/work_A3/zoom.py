import sys
from PIL import Image
# usage: zoom.py in out x0 y0 x1 y1 scale
src, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(int, sys.argv[3:7])
s = float(sys.argv[7]) if len(sys.argv) > 7 else 2
im = Image.open(src)
print(im.size)
c = im.crop((x0, y0, x1, y1))
c = c.resize((int(c.width*s), int(c.height*s)), Image.LANCZOS)
c.save(out)
