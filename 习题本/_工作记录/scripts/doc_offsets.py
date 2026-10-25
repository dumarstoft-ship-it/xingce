"""Measure, per source PDF, the vertical offset between pdfplumber line boxes and the rendered ink
(some PDFs have font metrics that put every line box ~6 pt below the real glyphs, which made crops cut the
first line in half and pick up the next line). Writes db/doc_offsets.json {stem: offset_pt} (ink - box)."""
import json, os, glob, subprocess, statistics, sys
import numpy as np
from PIL import Image
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce'
DPI = 100

def ink_runs(a, ink=150):
    rows = (a < ink).sum(axis=1) > 0
    out = []; y = 0; h = len(rows)
    while y < h:
        if rows[y]:
            s = y
            while y < h and rows[y]: y += 1
            out.append((s, y))
        else:
            y += 1
    return out

def page_offset(stem, pg):
    W, H = pg['width'], pg['height']
    out = f"{S}/offset_pages/{stem}__p{pg['page']}"
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-f', str(pg['page']), '-l', str(pg['page']), '-r', str(DPI), '-gray', '-png', '-singlefile',
                        os.path.join(SRC, stem + '.pdf'), out], check=True, capture_output=True)
    a = np.asarray(Image.open(out + '.png').convert('L'))
    sc = a.shape[0] / H
    runs = [((s + e) / 2 / sc, (e - s) / sc) for s, e in ink_runs(a)]
    ds = []
    for L in pg['lines']:
        if len(L['text'].strip()) < 6: continue
        c = (L['top'] + L['bottom']) / 2; hgt = L['bottom'] - L['top']
        near = [rc for rc, rh in runs if abs(rc - c) < 1.2 * hgt and 0.5 * hgt < rh < 1.8 * hgt]
        if near: ds.append(min(near, key=lambda rc: abs(rc - c)) - c)
    return ds

def main(stems):
    res = json.load(open(S + '/db/doc_offsets.json')) if os.path.exists(S + '/db/doc_offsets.json') else {}
    for stem in stems:
        d = json.load(open(f'{S}/lines/{stem}.json'))
        if d.get('ocr'): res[stem] = 0.0; continue
        pages = [p for p in d['pages'] if len(p['lines']) > 10]
        pick = pages[len(pages) // 4: len(pages) // 4 + 1] + pages[len(pages) // 2: len(pages) // 2 + 1] + pages[3 * len(pages) // 4: 3 * len(pages) // 4 + 1]
        ds = []
        for pg in pick:
            try: ds += page_offset(stem, pg)
            except Exception as e: print('ERR', stem, e)
        res[stem] = round(statistics.median(ds), 2) if len(ds) >= 8 else 0.0
        print(f'{res[stem]:6.2f}  n={len(ds):3d}  {stem}')
    json.dump(res, open(S + '/db/doc_offsets.json', 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    sys.path.insert(0, S + '/scripts')
    from papers import PAPERS
    stems = sorted({x for _, _, qf, jf in PAPERS for x in (qf, jf) if x})
    main(sys.argv[1:] or stems)
