import sys
from PIL import Image
src, out, x0, y0, x1, y1, scale = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:8])
im = Image.open(src)
print(im.size)
w, h = im.size
box = (int(x0*w) if x0<=1 else int(x0), int(y0*h) if y0<=1 else int(y0), int(x1*w) if x1<=1 else int(x1), int(y1*h) if y1<=1 else int(y1))
c = im.crop(box)
c = c.resize((int(c.width*scale), int(c.height*scale)), Image.LANCZOS)
c.save(out)
print(box, c.size)
