"""Crops for 资料分析 sets: colour material crops (charts keep their series colours), question crops with the original
number whited out, grayscale 解析 crops. Output: crops/zl/<id>_{s,q,j}.png (+ .json with display scale)."""
import json, os, re, sys, subprocess
from PIL import Image, ImageDraw
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop as gcrop, strip_slivers, doc_offset, JUNK, SRC
import mask_qnum as M
from split_q import load
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/crops/zl'
CACHE = S + '/pagecache_rgb'
_docs = {}
def doc(stem):
    if stem not in _docs: _docs[stem] = load(stem)
    return _docs[stem]

def page_png(stem, page, dpi=200):
    W = doc(stem)['pages'][page - 1]['width']
    if W > 700: dpi = max(60, int(dpi * 595 / W))
    out = os.path.join(CACHE, f'{stem}__p{page}_{dpi}')
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-png', '-singlefile', os.path.join(SRC, stem + '.pdf'), out], check=True)
    return out + '.png'

def whiten(im, thr=226):
    a = np.asarray(im.convert('RGB')).copy()
    m = (a > thr).all(axis=2)
    a[m] = 255
    return Image.fromarray(a)

def sliver_cut(g, thin=9, gap=3, ink=200):
    """rows to keep after dropping a thin band of ink at the very top/bottom (a neighbouring line's fragment)"""
    h = g.shape[0]
    if h < 27: return 0, h
    rows = (g[:, ::2] < ink).any(axis=1)
    idx = np.flatnonzero(np.diff(np.concatenate([[0], rows.astype(np.int8), [0]])))
    bands = list(zip(idx[0::2], idx[1::2]))
    top, bot = 0, h
    if len(bands) >= 2:
        s_, e_ = bands[-1]
        if e_ - s_ <= thin and s_ - bands[-2][1] >= gap and e_ >= h - 2: bot = bands[-2][1] + 2
        s_, e_ = bands[0]
        if e_ - s_ <= thin and bands[1][0] - e_ >= gap and s_ <= 2: top = bands[1][0] - 2
    return int(top), int(min(h, bot))

def zcrop(stem, regions, outpath, xr, pad_top=0):
    """regions: page -> [top, bottom] (pt); xr: (x0, x1) in pt. Stacks the page pieces vertically (colour)."""
    parts = []
    dy = doc_offset(stem)
    d = doc(stem)
    for p in sorted(regions, key=int):
        top, bot = regions[p]; top += dy; bot += dy
        pg = d['pages'][int(p) - 1]
        W, H = pg['width'], pg['height']
        img = Image.open(page_png(stem, int(p))).convert('RGB')
        sc = img.width / W
        dr = ImageDraw.Draw(img)
        for L in pg['lines']:
            if JUNK.search(L['text']) and L['bottom'] > top and L['top'] < bot:
                dr.rectangle([0, (L['top'] - 2) * sc, img.width, (L['bottom'] + 2) * sc], fill=(255, 255, 255))
        x0 = max(0, xr[0]); x1 = min(W, xr[1])
        c = img.crop((int(x0 * sc), int(max(0, top) * sc), int(x1 * sc), int(min(H, bot) * sc)))
        c = whiten(c)
        t0, t1 = sliver_cut(np.asarray(c.convert('L')))
        if (t0, t1) != (0, c.height): c = c.crop((0, t0, c.width, t1))
        bbox = Image.eval(c.convert('L'), lambda v: 255 - v).getbbox()
        if bbox:
            c = c.crop((0, max(0, bbox[1] - 6), c.width, min(c.height, bbox[3] + 6)))
            parts.append(c)
    if not parts: return None
    Wt = max(c.width for c in parts)
    Ht = sum(c.height for c in parts) + 8 * (len(parts) - 1)
    canvas = Image.new('RGB', (Wt, Ht), (255, 255, 255))
    y = 0
    for c in parts:
        canvas.paste(c, (0, y)); y += c.height + 8
    canvas.save(outpath + '.tmp.png', optimize=True)
    os.replace(outpath + '.tmp.png', outpath)
    return outpath

def mask_number(path, text):
    """white the leading question number out of a colour question crop and pull the rest of the first line left"""
    m = M.PREFIX.match(text or '')
    if not m: return 'nomatch'
    nd, punct = len(m.group(1)), m.group(2)
    im = Image.open(path).convert('RGB'); g = im.convert('L'); w, h = g.size; px = g.load()
    band = M.first_band(px, w, h)
    if not band: return 'noband'
    y0, y1 = band; bh = y1 - y0 + 1
    if bh < 12 or bh > 120: return 'band?'
    cl = M.clusters(px, w, y0, y1)
    if not cl or cl[0][0] > 4 * bh: return 'indent'
    k = M.find_prefix(cl, bh, nd, punct)
    if k is None: return 'wide'
    end, nxt = cl[k][1], cl[k + 1][0]
    out = im.copy(); dr = ImageDraw.Draw(out)
    line = out.crop((nxt, max(0, y0 - 3), w, min(h, y1 + 4)))
    dr.rectangle([cl[0][0], max(0, y0 - 3), w - 1, min(h - 1, y1 + 3)], fill=(255, 255, 255))
    out.paste(line, (cl[0][0], max(0, y0 - 3)))
    out.save(path)
    return 'ok'

def build(recs, force=False):
    from zl_build import xextent
    stats = {}
    for r in recs:
        i = r['id']; qp, sp, jp = f'{OUT}/{i}_q.png', f'{OUT}/{i}_s.png', f'{OUT}/{i}_j.png'
        d = doc(r['qfile'])
        if r['pos'] == 1 and r['stem_regions'] and (force or not os.path.exists(sp)):
            xr = xextent(d, r['stem_regions'])
            zcrop(r['qfile'], r['stem_regions'], sp, xr)
        if force or not os.path.exists(qp):
            xr = xextent(d, r['regions'])
            zcrop(r['qfile'], r['regions'], qp, xr)
            st = mask_number(qp, r['text'])
            stats[st] = stats.get(st, 0) + 1
            if st != 'ok': r['_mask'] = st
        if r.get('jiexi_regions') and (force or not os.path.exists(jp)):
            try:
                gcrop(r['jfile'], r['jiexi_regions'], jp)
            except Exception as e:
                print('JERR', i, repr(e)[:80])
    return stats

# ---------------------------------------------------------------- print chunks
def page_units(d, p, top, bot):
    """vertical units on one page piece: text lines outside figures, and figure zones (images / vector art plus the
    text lines inside them, e.g. table cells and axis labels). Cutting is allowed only between units."""
    from zl_build import page_items
    pg = d['pages'][int(p) - 1]
    items = [b for b in page_items(d, pg) if b[3] > top and b[1] < bot]
    texts = []
    for L in pg['lines']:
        if L['bottom'] > top and L['top'] < bot and L['text'].strip() and not JUNK.search(L['text']):
            texts.append((L['top'], L['bottom']))
    figs = sorted((b[1], b[3]) for b in items if (b[1], b[3]) not in set(texts) and not any(abs(b[1] - t) < 0.2 and abs(b[3] - u) < 0.2 for t, u in texts))
    zones = []
    for a, b in figs:
        if zones and a <= zones[-1][1] + 6: zones[-1][1] = max(zones[-1][1], b)
        else: zones.append([a, b])
    changed = True
    while changed:  # pull in text lines that overlap a zone (table cells, chart labels, captions touching the art)
        changed = False
        for t, u in texts:
            for z in zones:
                if u > z[0] - 1.5 and t < z[1] + 1.5 and (t < z[0] or u > z[1]):
                    z[0] = min(z[0], t); z[1] = max(z[1], u); changed = True
        zs = sorted(zones); zones = []
        for a, b in zs:
            if zones and a <= zones[-1][1] + 1: zones[-1][1] = max(zones[-1][1], b)
            else: zones.append([a, b])
    units = [(a, b) for a, b in zones]
    for t, u in texts:
        if not any(t >= z[0] - 0.5 and u <= z[1] + 0.5 for z in zones): units.append((t, u))
    units.sort()
    return [(max(a, top), min(b, bot)) for a, b in units if b > top and a < bot]

def chunk_regions(d, regions, maxh=250.0):
    """split a material's regions into print chunks (each within one page) at gaps between units"""
    out = []
    for p in sorted(regions, key=int):
        top, bot = regions[p]
        us = page_units(d, p, top, bot)
        if not us:
            out.append((p, top, bot)); continue
        cur0 = top; last_end = None
        cuts = []
        for k in range(1, len(us)):
            gap_mid = (us[k - 1][1] + us[k][0]) / 2
            if us[k][0] >= us[k - 1][1]: cuts.append(gap_mid)
        start = top
        while bot - start > maxh:
            cand = [c for c in cuts if start + 40 < c <= start + maxh]
            if not cand: break
            c = cand[-1]
            out.append((p, start, c)); start = c
        out.append((p, start, bot))
    return out

def paper_scale(code, recs):
    from statistics import median
    d = doc(recs[0]['qfile'])
    hs = []
    for r in recs:
        for regs in (r['regions'], r['stem_regions']):
            for p, (t, b) in regs.items():
                for L in d['pages'][int(p) - 1]['lines']:
                    if L['top'] >= t and L['bottom'] <= b and len(L['text'].strip()) >= 12 and not JUNK.search(L['text']):
                        hs.append(L['bottom'] - L['top'])
    f = median(hs) if hs else 10.5
    return f, round(max(0.92, min(1.2, 10.5 / f)), 3)

def build_print(recs):
    """per paper: shared x-range, stem chunks <id>_p<k>.png, question crops <id>_q.png (number masked), scale"""
    from zl_build import page_items
    by = {}
    for r in recs: by.setdefault(r['paper'], []).append(r)
    meta = {}
    for code, rs in by.items():
        d = doc(rs[0]['qfile'])
        from zl_build import doc_frame
        tx0, tx1 = doc_frame(d)[5:7]
        x0, x1 = 1e9, -1e9
        for r in rs:
            for regs in (r['regions'], r['stem_regions']):
                for p, (t, b) in regs.items():
                    for (a, tt, c, bb) in page_items(d, d['pages'][int(p) - 1]):
                        if bb > t and tt < b: x0 = min(x0, a); x1 = max(x1, c)
        x0, x1 = max(x0, tx0 - 30), min(x1, tx1 + 30)
        xr = (x0 - 4, x1 + 4)
        f, sc = paper_scale(code, rs)
        W = (xr[1] - xr[0]) / 72 * 25.4 * sc
        if W > 182: sc = round(sc * 182 / W, 3)
        meta[code] = {'xr': xr, 'font': round(f, 2), 'scale': sc}
        for r in rs:
            i = r['id']
            if r['pos'] == 1:
                for old in [x for x in os.listdir(OUT) if x.startswith(i + '_p')]: os.remove(os.path.join(OUT, old))
                k = 0
                for (p, t, b) in chunk_regions(d, r['stem_regions']):
                    if zcrop(r['qfile'], {p: [t, b]}, f'{OUT}/{i}_p{k + 1}.png', xr): k += 1  # blank pieces write nothing
                r['n_chunks'] = k
            qp = f'{OUT}/{i}_q.png'
            zcrop(r['qfile'], r['regions'], qp, xr)
            st = mask_number(qp, r['text'])
            if st != 'ok': r['_mask'] = st
    return meta

def build_jiexi(recs, force=False):
    n = 0
    for r in recs:
        jp = f"{OUT}/{r['id']}_j.png"
        if not r.get('jiexi_regions') or (os.path.exists(jp) and not force): continue
        try:
            gcrop(r['jfile'], r['jiexi_regions'], jp); n += 1
        except Exception as e:
            print('JERR', r['id'], repr(e)[:100], flush=True)
    return n

def chunk_files(first_id):
    """material chunk crops of a passage in order"""
    import glob as _g, re as _re
    fs = [f for f in _g.glob(f'{OUT}/{first_id}_p*.png') if _re.search(r'_p\d+\.png$', f)]
    return sorted(fs, key=lambda f: int(_re.search(r'_p(\d+)\.png$', f).group(1)))
