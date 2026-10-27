"""Find question / 解析 regions that lose a figure at a page break:
(a) a later page of the region starts at its first text line, below a figure that sits at the top of that page;
(b) the region's last page ends at the page foot while the next page opens with a figure before any text.
Prints the proposed new regions; with --spec <file> writes them as a fix_crops spec."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crop
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def content(P, dy):
    """text lines (no header/footer junk) and images of a page, all in line-box coordinates"""
    lines = [L for L in P['lines'] if not crop.JUNK.search(L['text']) and L['text'].strip()
             and L['top'] < P['height'] - 45 and not re.fullmatch(r'\s*[-－—]?\s*\d+\s*[-－—]?\s*', L['text'])]  # no footer
    imgs = [dict(im, top=im['top'] - dy, bottom=im['bottom'] - dy) for im in P['images']
            if im['bottom'] - im['top'] > 8 and im['x1'] - im['x0'] < 0.97 * P['width']]
    return lines, imgs

def check(stem, regs):
    """new regions, or None"""
    dy = crop.doc_offset(stem); new = dict(regs); why = []
    pages = sorted(regs, key=int)
    for k, pk in enumerate(pages):
        t, b = regs[pk]
        P = crop.page_lines(stem, int(pk)); lines, imgs = content(P, dy)
        if k > 0:  # (a) a figure above the region's first line, with no text between page top and the region
            above = [im for im in imgs if im['top'] >= 10 and im['top'] < t - 5 and im['bottom'] <= t + 15]  # incl. inline figures
            text_above = [L for L in lines if L['bottom'] <= t + 1]
            if above and not text_above:
                nt = round(min(im['top'] for im in above) - 1.5, 1)
                new[pk] = [nt, b]; why.append(f'p{pk} top {t}->{nt}')
    pk = pages[-1]; t, b = new[pk]
    P = crop.page_lines(stem, int(pk)); lines, imgs = content(P, dy)
    below = [L for L in lines if L['top'] >= b - 1]
    if not below and not [im for im in imgs if im['top'] >= b - 1]:  # (b) nothing after the region on its last page
        nxt = int(pk) + 1
        try: P2 = crop.page_lines(stem, nxt)
        except Exception: P2 = None
        if P2:
            l2, i2 = content(P2, dy)
            first_text = min((L['top'] for L in l2), default=1e9)
            top_imgs = [im for im in i2 if im['bottom'] <= first_text + 3]
            if top_imgs:
                new[str(nxt)] = [round(min(im['top'] for im in top_imgs) - 1.5, 1), round(max(im['bottom'] for im in top_imgs) + 1.5, 1)]
                why.append(f'add p{nxt} {new[str(nxt)]}')
    return (new, why) if why else None

if __name__ == '__main__':
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    ids = [c['id'] for c in json.load(open(S + '/tu/candidates.json'))]
    spec = {}
    for i in ids:
        r = raw[i]
        for kind, stem, key in (('q', r['qfile'], 'regions'), ('j', r.get('jfile'), 'jiexi_regions')):
            if not stem or not r.get(key): continue
            res = check(stem, r[key])
            if res:
                print(i, kind, r[key], '->', res[0], res[1])
                spec.setdefault(i, {})[key] = res[0]
    if '--spec' in sys.argv:
        json.dump(spec, open(sys.argv[sys.argv.index('--spec') + 1], 'w'), ensure_ascii=False, indent=1)
