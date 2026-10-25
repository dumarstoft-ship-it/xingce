import sys
from PIL import Image, ImageDraw
names = sys.argv[2:]
out = sys.argv[1]
ims = [Image.open(f"fig/{n}.png").convert("RGB") for n in names]
cols = 2
cw = max(i.width for i in ims); ch = max(i.height for i in ims) + 30
rows = (len(ims) + cols - 1) // cols
M = Image.new("RGB", (cw * cols, ch * rows), "white")
d = ImageDraw.Draw(M)
for k, (n, im) in enumerate(zip(names, ims)):
    x, y = (k % cols) * cw, (k // cols) * ch
    M.paste(im, (x, y + 30))
    d.text((x + 10, y + 8), n, fill="red")
    d.rectangle([x, y, x + cw - 1, y + ch - 1], outline="#ccc")
M.save(out)
print(M.size)
