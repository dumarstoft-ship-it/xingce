"""Render source-page context around a question/jiexi region: ctx.py ID q|j [above_pt] [below_pt]"""
import json, sys, os
from PIL import Image
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/tu/zoom_3'
i, kind = sys.argv[1], sys.argv[2]
above = float(sys.argv[3]) if len(sys.argv) > 3 else 60
below = float(sys.argv[4]) if len(sys.argv) > 4 else 120
raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
r = raw[i]
f = r['qfile'] if kind == 'q' else r['jfile']
regs = r['regions'] if kind == 'q' else r['jiexi_regions']
outs = []
for pg, (t, b) in regs.items():
    p = f'{S}/pagecache/{f}__p{pg}_200.png'
    if not os.path.exists(p):
        print('missing', p); continue
    im = Image.open(p)
    sc = 200 / 72
    y0 = max(0, int((t - above) * sc)); y1 = min(im.height, int((b + below) * sc))
    c = im.crop((0, y0, im.width, y1))
    o = f'{OUT}/{i}_{kind}_ctx_p{pg}.png'
    c.save(o); outs.append(o)
    print(o, im.size, (t, b), 'crop y', y0, y1)
