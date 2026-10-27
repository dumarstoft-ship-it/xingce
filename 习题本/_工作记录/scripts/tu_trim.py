"""图推专项本: drop the "A.A  B.B  C.C  D.D" (or "A.如上图所示 …") line(s) that the exported papers print under figure-option questions (the
option letters are already in the figure). Builds a fix_crops spec (recorded in db/overrides.json) for every candidate
whose question region ends with such lines, then re-crops through fix_crops. Usage: tu_trim.py [--dry]"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crop
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
LETTERS = re.compile(r'^\s*([A-D]\s*[\.．、]\s*([A-D]|如上图所示)\s*)+$')
MANUAL = {'2025GKD-81': {'14': [602.0, 751.1]}}  # page 15 of the region holds only a blank image

def trimmed(r):
    """the question regions without the trailing option-letter lines (which can run over a page break), or None when
    there is nothing to trim"""
    regs = r.get('regions') or {}
    if not regs: return None
    stem = r['qfile']; dy = crop.doc_offset(stem)
    nr = dict(regs); changed = False
    for pk in sorted(regs, key=int, reverse=True):
        top, bot = nr[pk]
        P = crop.page_lines(stem, int(pk))
        lines = sorted([L for L in P['lines'] if L['bottom'] > top and L['top'] < bot and not crop.JUNK.search(L['text'])],
                       key=lambda L: L['top'])
        cut = None
        while lines and LETTERS.match(lines[-1]['text']):
            cut = lines.pop()['top']
        if cut is None: break
        if any(im['top'] - dy >= cut - 1 and im['top'] - dy < bot for im in P['images']): break  # a figure below the letters
        changed = True
        if lines or any(im['bottom'] - dy > top and im['top'] - dy < cut for im in P['images']):
            nr[pk] = [top, round(cut - 1.0, 1)]; break
        del nr[pk]  # the letters were all this page held: go on to the page before
    return nr if changed and nr else None

PREFIX = ['2022GKX-75', '2022GKX-76', '2022GKX-77']  # stems printed as "（单选题）…"

def strip_prefix(path, n=5, ink=160):
    """remove the "（单选题）" prefix (the first n glyph clusters of the first text line) from a question crop and move
    the rest of the line left; does nothing when the line no longer starts with a narrow "（" """
    import numpy as np
    from PIL import Image
    im = Image.open(path); a = np.asarray(im.convert('L'))
    rows = (a < ink).any(axis=1)
    y0 = int(np.argmax(rows)); y1 = y0
    while y1 < len(rows) and rows[y1]: y1 += 1
    y2 = y1
    while y2 < len(rows) and not rows[y2]: y2 += 1  # first ink row below the line
    cols = (a[y0:y1] < ink).any(axis=0); cl = []; x = 0
    while x < len(cols):
        if cols[x]:
            s0 = x
            while x < len(cols) and cols[x]: x += 1
            cl.append((s0, x))
        else: x += 1
    h = y1 - y0
    if len(cl) <= n or cl[0][1] - cl[0][0] > 0.5 * h or cl[n - 1][1] - cl[n - 1][0] > 0.5 * h: return False
    top, bot = max(0, y0 - 3), min(y2 - 1, y1 + 3)
    line = im.crop((cl[n][0], top, im.width, bot + 1))
    from PIL import ImageDraw
    ImageDraw.Draw(im).rectangle([cl[0][0], top, im.width - 1, bot], fill=255 if im.mode == 'L' else (255,) * len(im.mode))
    im.paste(line, (cl[0][0], top)); im.save(path)
    return True

if __name__ == '__main__':
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    cands = json.load(open(S + '/tu/candidates.json'))
    spec = {}
    for c in cands:
        nr = MANUAL.get(c['id']) or trimmed(raw[c['id']])
        if nr: spec[c['id']] = {'regions': nr}
    print('trim', len(spec))
    json.dump(spec, open(S + '/tu/trim_spec.json', 'w'), ensure_ascii=False, indent=1)
    if '--dry' not in sys.argv:
        import fix_crops
        fix_crops.main(spec)
    for i in PREFIX:
        print(i, 'prefix removed' if strip_prefix(f'{S}/crops/real2_nonum/{i}_q.png') else 'prefix already gone')
