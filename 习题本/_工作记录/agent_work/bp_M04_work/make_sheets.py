import json, sys
from PIL import Image, ImageDraw, ImageFont
base = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
d = json.load(open(base + 'tasks_in/M04.json'))
kind = sys.argv[1]  # q or j
per = int(sys.argv[2])
items = []
for q in d['real']:
    p = q[kind + '_crop']
    if p: items.append((q['id'], p))
W = 1500
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
except Exception:
    font = ImageFont.load_default()
for s in range(0, len(items), per):
    chunk = items[s:s+per]
    ims = []
    for qid, p in chunk:
        im = Image.open(p).convert('RGB')
        if im.width > W:
            im = im.resize((W, int(im.height * W / im.width)))
        ims.append((qid, im))
    H = sum(im.height + 40 for _, im in ims)
    sheet = Image.new('RGB', (W, H), 'white')
    y = 0
    dr = ImageDraw.Draw(sheet)
    for qid, im in ims:
        dr.rectangle([0, y, W, y + 36], fill=(255, 230, 150))
        dr.text((8, y + 2), qid, fill='black', font=font)
        y += 40
        sheet.paste(im, (0, y))
        y += im.height
    out = base + f'bp_M04_work/sheets/{kind}_{s//per:02d}.png'
    sheet.save(out)
    print(out, sheet.size, [c[0] for c in chunk])
