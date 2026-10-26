"""White out the original question number ("52." / "61、") at the start of each real-question crop,
so the workbook shows only its own numbering. Writes crops/real2_nonum/<id>_q.png; skips when unsure."""
import json, os, re, sys, shutil
from PIL import Image, ImageDraw
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC_DIR = S + '/crops/real2'
OUT_DIR = S + '/crops/real2_nonum'
PREFIX = re.compile(r'^\s*(\d{1,3})[ \t]*([\.．、,，:：]?)')

def first_band(px, w, h, ink=160):
    rows = [sum(1 for x in range(w) if px[x, y] < ink) for y in range(h)]
    y = 0
    while y < h and rows[y] == 0: y += 1
    if y >= h: return None
    y0 = y; gap = 0
    while y < h:
        if rows[y] == 0:
            gap += 1
            if gap > 2: break
        else:
            gap = 0
        y += 1
    return y0, y - gap

def clusters(px, w, y0, y1, ink=160):
    cols = [any(px[x, y] < ink for y in range(y0, y1 + 1)) for x in range(w)]
    out = []; x = 0
    while x < w:
        if cols[x]:
            s = x
            while x < w and cols[x]: x += 1
            out.append((s, x - 1))
        else:
            x += 1
    return out

def find_prefix(cl, bh, nd, punct):
    """Return index of the last cluster belonging to the number prefix, or None."""
    need = nd + (1 if punct else 0)
    if len(cl) > need and all(b - a + 1 <= 0.72 * bh for a, b in cl[:need]) and cl[need][0] - cl[need - 1][1] >= 2 \
            and all(cl[j + 1][0] - cl[j][1] < 0.5 * bh for j in range(need - 1)):  # digits sit close together
        return need - 1
    # touching digits: grow from the left while the span stays narrow enough for nd digits (+ punctuation)
    max_w = (0.66 * nd + (0.5 if punct else 0.1)) * bh
    k = None
    for j, (a, b) in enumerate(cl):
        if b - cl[0][0] + 1 > max_w: break
        k = j
    if k is None or k + 1 >= len(cl): return None
    if cl[k][1] - cl[0][0] + 1 < 0.3 * nd * bh: return None
    if cl[k + 1][0] - cl[k][1] < 2: return None
    return k

def save(out, qid, src):
    out.save(f'{OUT_DIR}/{qid}_q.png')
    if os.path.exists(src + '.json'): shutil.copy(src + '.json', f'{OUT_DIR}/{qid}_q.png.json')

def mask(qid, text, shift=True):
    """shift=False only whites the number out: number series often start with a row of fraction numerators,
    and moving that row left would detach the numerators from their fraction bars."""
    m = PREFIX.match(text or '')
    src = f'{SRC_DIR}/{qid}_q.png'
    if not m or not os.path.exists(src): return 'nomatch'
    nd, punct = len(m.group(1)), m.group(2)
    own_line = (text[m.end():].lstrip(' \t')[:1] == '\n')
    im = Image.open(src).convert('L'); w, h = im.size; px = im.load()
    band = first_band(px, w, h)
    if not band: return 'noband'
    y0, y1 = band; bh = y1 - y0 + 1
    if bh < 12 or bh > 120: return 'band?'
    cl = clusters(px, w, y0, y1)
    if not cl or cl[0][0] > 4 * bh: return 'indent'
    if own_line:  # the number sits alone on the first line: drop that line
        span = cl[-1][1] - cl[0][0] + 1
        if span > (0.7 * nd + 0.6) * bh: return 'ownline?'
        rest = im.crop((0, y1 + 1, w, h))
        bbox = Image.eval(rest, lambda v: 255 - v).getbbox()
        if not bbox: return 'empty'
        save(rest.crop((0, max(0, bbox[1] - 6), w, rest.height)), qid, src)
        return 'ok'
    k = find_prefix(cl, bh, nd, punct)
    if k is None: return 'wide'
    end, nxt = cl[k][1], cl[k + 1][0]
    out = im.copy(); d = ImageDraw.Draw(out)
    if not shift:
        d.rectangle([cl[0][0], max(0, y0 - 3), end + 1, min(h - 1, y1 + 3)], fill=255)
        save(out, qid, src)
        return 'ok'
    line = out.crop((nxt, max(0, y0 - 3), w, min(h, y1 + 4)))
    d.rectangle([cl[0][0], max(0, y0 - 3), w - 1, min(h - 1, y1 + 3)], fill=255)
    out.paste(line, (cl[0][0], max(0, y0 - 3)))
    save(out, qid, src)
    return 'ok'

if __name__ == '__main__':
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    ids = sys.argv[1:] or [i for i, r in raw.items() if r['kind'] in ('数学运算', '逻辑')]
    from collections import Counter
    res = Counter(); bad = {}
    for i in ids:
        r = mask(i, raw[i].get('text'))
        res[r] += 1
        if r != 'ok': bad.setdefault(r, []).append(i)
    print(dict(res))
    for k, v in bad.items(): print(k, v[:12])

HDR = re.compile(r'^\s*(\d+\s*[~～\-—－至到]\s*\d+\s*题|[（(][一二三四五六七八九十]+[）)]\s*$)')

def mask_stem_header(qid, stem_text):
    """Drop a leading "97~98题基于如下题干：" line from a shared-material crop (the workbook prints its own numbers)."""
    src = f'{SRC_DIR}/{qid}_s.png'
    first = (stem_text or '').strip().split('\n')[0]
    if not os.path.exists(src) or not HDR.match(first) or len(first) > 30: return 'skip'
    im = Image.open(src).convert('L'); w, h = im.size; px = im.load()
    band = first_band(px, w, h)
    if not band: return 'noband'
    rest = im.crop((0, band[1] + 1, w, h))
    bbox = Image.eval(rest, lambda v: 255 - v).getbbox()
    if not bbox: return 'empty'
    rest.crop((0, max(0, bbox[1] - 6), w, rest.height)).save(f'{OUT_DIR}/{qid}_s.png')
    if os.path.exists(src + '.json'): shutil.copy(src + '.json', f'{OUT_DIR}/{qid}_s.png.json')
    return 'ok'
