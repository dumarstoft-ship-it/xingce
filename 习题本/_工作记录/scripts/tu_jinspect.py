"""Show where a question's 解析 (or question) region sits on its source pages, to pick new region bounds by eye:
renders each page of the region widened by a margin, draws the current region in red and a y-ruler (line-box
coordinates, the ones real_raw.json / fix_crops use) every 10pt. Usage: tu_jinspect.py <id> [j|q] [margin_pt]"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crop
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

def inspect(qid, kind='j', margin=120, extra_pages=()):
    r = {x['id']: x for x in json.load(open(S + '/db/real_raw.json'))}[qid]
    stem = r['jfile'] if kind == 'j' else r['qfile']
    regs = dict(r['jiexi_regions'] if kind == 'j' else r['regions'])
    for p in extra_pages: regs.setdefault(str(p), None)
    dy = crop.doc_offset(stem)
    outs = []
    for pk in sorted(regs, key=int):
        P = crop.page_lines(stem, int(pk)); W, H = P['width'], P['height']
        t, b = regs[pk] if regs[pk] else (0, H)
        y0, y1 = max(0, t - margin), min(H, b + margin)
        img = Image.open(crop.page_png(stem, int(pk))).convert('RGB'); sc = img.width / W
        # the page image shows ink at line coordinates + dy, so show (y + dy) to read off line-box coordinates
        c = img.crop((0, int((y0 + dy) * sc), img.width, int((y1 + dy) * sc)))
        canvas = Image.new('RGB', (c.width + 70, c.height), 'white'); canvas.paste(c, (70, 0))
        d = ImageDraw.Draw(canvas)
        for y in range(int(y0 // 10 * 10), int(y1) + 1, 10):
            yy = (y - y0) * sc
            d.line([(55, yy), (70 if y % 50 else 75, yy)], fill='blue', width=1)
            if y % 20 == 0: d.text((2, yy - 8), str(y), fill='blue', font=FONT)
        if regs[pk]:
            for y in (t, b): d.line([(70, (y - y0) * sc), (canvas.width, (y - y0) * sc)], fill='red', width=2)
        d.text((80, 2), f'{qid} {kind} p{pk} region {regs[pk]}', fill='red', font=FONT)
        out = f'{S}/tu/insp/{qid}_{kind}_p{pk}.png'; os.makedirs(os.path.dirname(out), exist_ok=True)
        canvas.save(out); outs.append(out)
        for L in P['lines']:
            if L['bottom'] > y0 and L['top'] < y1: print(f"  p{pk} {L['top']:6.1f}-{L['bottom']:6.1f} x{L['x0']:5.0f}-{L['x1']:5.0f} {L['text'][:50]}")
        for im in P['images']:
            if im['bottom'] - dy > y0 and im['top'] - dy < y1:
                print(f"  p{pk} IMG {im['top'] - dy:6.1f}-{im['bottom'] - dy:6.1f} x{im['x0']:5.0f}-{im['x1']:5.0f}")
    return outs

if __name__ == '__main__':
    a = sys.argv[1:]
    print(inspect(a[0], a[1] if len(a) > 1 else 'j', float(a[2]) if len(a) > 2 else 120,
                  [int(x) for x in a[3].split(',')] if len(a) > 3 else ()))
