import os, subprocess, json, re, sys
from PIL import Image, ImageDraw
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce'
CACHE = S + '/pagecache'
JUNK = re.compile(r'本试卷由粉笔用户|认准淘宝|通关达人|TB：|TB:|Seeyee|淘宝店铺|获取持续更新|微信|公众号|QQ群|免费获取|考公资料|hijoe|^\s*\d+\s*/\s*\d+\s*$|第\s*\d+\s*[页⻚]')
_lines_cache = {}
def page_png(stem, page, dpi=200):
    W = page_lines(stem, page)['width']
    if W > 700: dpi = max(60, int(dpi * 595 / W))
    out = os.path.join(CACHE, f'{stem}__p{page}_{dpi}')
    png = out + '.png'
    if not os.path.exists(png):
        subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-gray', '-png', '-singlefile', os.path.join(SRC, stem + '.pdf'), out], check=True)
    return png
def page_lines(stem, page):
    if stem not in _lines_cache:
        _lines_cache[stem] = json.load(open(os.path.join(S, 'lines', stem + '.json')))
    return _lines_cache[stem]['pages'][page - 1]
def strip_slivers(c, thin=9, gap=3, ink=200):
    """Remove a thin band of ink at the very top/bottom (fragments of the neighbouring line)."""
    w, h = c.size
    if h < 3 * thin: return c
    px = c.load()
    rows = [any(px[x, y] < ink for x in range(0, w, 2)) for y in range(h)]
    bands = []; y = 0
    while y < h:
        if rows[y]:
            s = y
            while y < h and rows[y]: y += 1
            bands.append((s, y))
        else:
            y += 1
    if len(bands) >= 2:
        s, e = bands[-1]
        if e - s <= thin and s - bands[-2][1] >= gap and e >= h - 2:
            c = c.crop((0, 0, w, bands[-2][1] + 2)); h = c.size[1]
        s, e = bands[0]
        if e - s <= thin and bands[1][0] - e >= gap and s <= 2:
            c = c.crop((0, bands[1][0] - 2, w, h))
    return c

def crop(stem, regions, outpath, dpi=200, mask_junk=True, xpad=4):
    """regions: dict page->[top,bottom] (points). Produces vertically stacked crop."""
    parts = []
    heights = []
    for p in sorted(regions, key=lambda x: int(x)):
        top, bot = regions[p]
        p = int(p)
        pl = page_lines(stem, p)
        W, H = pl['width'], pl['height']
        # horizontal extent: union of content lines + images within region
        xs0 = [L['x0'] for L in pl['lines'] if L['bottom'] > top and L['top'] < bot and not JUNK.search(L['text'])]
        xs1 = [L['x1'] for L in pl['lines'] if L['bottom'] > top and L['top'] < bot and not JUNK.search(L['text'])]
        for im in pl['images']:
            if im['bottom'] > top and im['top'] < bot and im['x1'] - im['x0'] < 0.97 * W:
                xs0.append(im['x0']); xs1.append(im['x1'])
        if not xs0:
            if not any(im['bottom'] > top and im['top'] < bot for im in pl['images']): continue
            xs0, xs1 = [0.05 * W], [0.95 * W]
        heights += [L['bottom'] - L['top'] for L in pl['lines'] if L['bottom'] > top and L['top'] < bot and not JUNK.search(L['text']) and len(L['text'].strip()) >= 6]
        x0 = max(0, min(xs0) - xpad); x1 = min(W, max(xs1) + xpad)
        img = Image.open(page_png(stem, p, dpi)).convert('L')
        sc = img.width / W
        if mask_junk:
            d = ImageDraw.Draw(img)
            for L in pl['lines']:
                if JUNK.search(L['text']) and L['bottom'] > top and L['top'] < bot:
                    d.rectangle([0, (L['top'] - 2) * sc, img.width, (L['bottom'] + 2) * sc], fill=255)
        c = img.crop((int(x0 * sc), int(max(0, top) * sc), int(x1 * sc), int(min(H, bot) * sc)))
        c = strip_slivers(c)
        # trim blank rows at bottom/top
        bbox = Image.eval(c, lambda v: 255 - v).getbbox()
        if bbox:
            c = c.crop((0, max(0, bbox[1] - 6), c.width, min(c.height, bbox[3] + 6)))
            parts.append((c, x0 * sc))
    if not parts: return None
    minx = min(px for _, px in parts)
    Wt = max(int(c.width + px - minx) for c, px in parts)
    Ht = sum(c.height for c, _ in parts) + 8 * (len(parts) - 1)
    canvas = Image.new('L', (Wt, Ht), 255)
    y = 0
    for c, px in parts:
        canvas.paste(c, (int(px - minx), y)); y += c.height + 8
    canvas = canvas.point(lambda v: 255 if v > 228 else int(v * 0.8))
    tmp = outpath + '.tmp.png'
    canvas.save(tmp, optimize=True)
    os.replace(tmp, outpath)
    hs = sorted(heights)
    med = hs[len(hs) // 2] if hs else 10.5
    scale = max(0.3, min(1.12, 10.2 / med)) if med > 0 else 1.0
    json.dump({'scale': round(scale, 3), 'font_pt': round(med, 2)}, open(outpath + '.json', 'w'))
    return outpath
