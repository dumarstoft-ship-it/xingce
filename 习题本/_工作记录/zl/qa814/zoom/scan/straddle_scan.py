import json, re, sys
sys.path.insert(0, '/home/user/xingce/习题本/_工作记录/scripts')
from split_q import load
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json')); by = {r['id']: r for r in raw}
H = open(S + '/zl/out/zl_d8-14.html').read()
qids = re.findall(r'crops/zl/([^"/]+)_q\.png', H)
mids = sorted(set(re.sub(r'_p\d+(_t)?$', '', m) for m in re.findall(r'crops/zl/([^"/]+_p\d+(?:_t)?)\.png', H)))
items = [(i, 'q', by[i]['regions']) for i in qids] + [(i, 'mat', by[i]['stem_regions']) for i in mids]
n = 0
for i, kind, regs in items:
    d = load(by[i]['qfile'])
    for p, (t, b) in regs.items():
        pg = d['pages'][int(p) - 1]
        W, Hh = pg['width'], pg['height']
        boxes = [('img', im['top'], im['bottom'], im['x0'], im['x1']) for im in pg.get('images', [])]
        for v in pg.get('vec', []):
            if len(v) >= 4:
                x0, top, x1, bot = v[0], v[1], v[2], v[3]
                boxes.append(('vec', top, bot, x0, x1))
        for kind2, top, bot, x0, x1 in boxes:
            if x1 - x0 > 0.95 * W or bot - top > 0.9 * Hh: continue  # page frames / backgrounds
            if bot - top < 1.0: continue  # hairlines
            if kind2 == "vec" and (x1 - x0) < 16 and (bot - top) < 12: continue  # watermark glyph pieces
            if kind2 == "vec" and (x1 - x0) > 0.85 * W: continue  # full-width row frames
            if bot > t and top < b and (top < t - 1.0 or bot > b + 1.0):
                cut_top = max(0, t - top); cut_bot = max(0, bot - b)
                print(f'{kind:3s} {i:14s} p{p} region[{t:.1f},{b:.1f}] {kind2} [{top:.1f},{bot:.1f}] x[{x0:.0f},{x1:.0f}] cut_top={cut_top:.1f} cut_bot={cut_bot:.1f}')
                n += 1
print('straddles', n)
