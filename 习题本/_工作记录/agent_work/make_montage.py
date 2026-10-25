import json, os, sys
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(S, 'cls/new_batch.jsonl'))]
out = os.path.join(S, 'montage')
MAXH = 1450
groups, cur, curh = [], [], 0
for i, r in enumerate(rows):
    im = Image.open(os.path.join(S, r['q_crop'])).convert('RGB')
    h = im.size[1] + 40
    if cur and curh + h > MAXH:
        groups.append(cur); cur, curh = [], 0
    cur.append((i, r['id'], im)); curh += h
if cur: groups.append(cur)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except Exception:
    font = ImageFont.load_default()
for gi, g in enumerate(groups):
    W = max(im.size[0] for _, _, im in g)
    H = sum(im.size[1] + 40 for _, _, im in g)
    canvas = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(canvas)
    y = 0
    for i, rid, im in g:
        d.rectangle([0, y, W, y + 36], fill=(255, 220, 220))
        d.text((8, y + 4), f'#{i}  {rid}', fill=(180, 0, 0), font=font)
        y += 40
        canvas.paste(im, (0, y)); y += im.size[1]
    fn = os.path.join(out, f'g{gi:02d}_{g[0][0]:03d}-{g[-1][0]:03d}.png')
    canvas.save(fn)
    print(fn, canvas.size, [x[0] for x in g])
