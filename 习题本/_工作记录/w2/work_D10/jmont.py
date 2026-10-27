import json, os, sys
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
d = json.load(open(os.path.join(S, 'w2/D10_packet.json')))
ids = sys.argv[1].split(',')
tag = sys.argv[2]
kind = sys.argv[3] if len(sys.argv) > 3 else 'j'
byid = {q['id']: q for q in d['candidate_real']}
MAXH = 1900
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except Exception:
    font = ImageFont.load_default()
groups, cur, curh = [], [], 0
for i in ids:
    q = byid[i]
    p = q['j_img'] if kind == 'j' else q['q_img']
    if not p or not os.path.exists(p):
        print('missing', i, p); continue
    im = Image.open(p).convert('RGB')
    if im.size[0] > 1400:
        r = 1400 / im.size[0]
        im = im.resize((1400, int(im.size[1] * r)))
    h = im.size[1] + 40
    if cur and curh + h > MAXH:
        groups.append(cur); cur, curh = [], 0
    cur.append((i, im)); curh += h
if cur: groups.append(cur)
for gi, g in enumerate(groups):
    W = max(im.size[0] for _, im in g)
    H = sum(im.size[1] + 40 for _, im in g)
    canvas = Image.new('RGB', (W, H), 'white')
    dr = ImageDraw.Draw(canvas)
    y = 0
    for rid, im in g:
        dr.rectangle([0, y, W, y + 36], fill=(220, 230, 255))
        dr.text((8, y + 4), rid, fill=(0, 0, 160), font=font)
        y += 40
        canvas.paste(im, (0, y)); y += im.size[1]
    fn = os.path.join(S, 'w2/work_D10', f'{tag}_{gi:02d}.png')
    canvas.save(fn)
    print(fn, canvas.size, [x[0] for x in g])
