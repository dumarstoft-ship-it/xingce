"""Hand-located 解析 for 资料 questions the automatic start detection skipped ("119、2011年…" reads as a number run)."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from split_q import load, flat_lines
import zl_build as Z
import zl_crop as C
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def locate(jf, n):
    lines = flat_lines(load(jf))
    st = [i for i, L in enumerate(lines) if re.match(rf'^\s*{n}\s*[、\.．]', L['text'])]
    nx = [i for i, L in enumerate(lines) if re.match(rf'^\s*{n + 1}\s*[、\.．]', L['text'])]
    if not st: return None
    a = lines[st[0]]
    b = lines[nx[0]] if nx and nx[0] > st[0] else None
    jdoc = load(jf)
    if b: regs = Z.span(jdoc, a['page'], a['top'], b['page'], b['top'])
    else:
        end = min(len(lines), st[0] + 40)
        seg = lines[st[0]:end]
        regs = Z.span(jdoc, a['page'], a['top'], seg[-1]['page'], seg[-1]['bottom'] + 2)
    return Z.cut_jiexi(jdoc, regs)
AD = re.compile(r'考公-考研|资料持续更新|淘宝[:：]|认准淘宝|公众号|资料铺子|Seeyee')

def snap_regions(stem, regs, drop_slivers=False):
    """A formula image straddling a region's top or bottom edge goes with the text line it mostly sits on: the region
    grows to take in our own formula, or shrinks to leave out the neighbouring question's. With drop_slivers, a page
    piece under 12pt with no text line of its own (the top of the next question's formula) is dropped.
    Returns new regions or None."""
    from crop import page_lines, doc_offset
    dy = doc_offset(stem)  # crop() shifts regions by dy to meet the rendered ink; images need no shift, so move them by -dy
    out, changed = {}, False
    for pg, (t, b) in regs.items():
        P = page_lines(stem, int(pg))
        P = dict(P, images=[dict(im, top=im['top'] - dy, bottom=im['bottom'] - dy) for im in P['images']])
        lines = [l for l in P['lines'] if l['bottom'] - l['top'] <= 30]  # taller "lines" are single watermark glyphs
        own = [l for l in lines if t - 0.5 <= l['top'] < b]
        ads = [l for l in own if AD.search(l['text'])]
        own = [l for l in own if l['text'].strip() and l not in ads]
        prev_b = max([l['bottom'] for l in lines if l['bottom'] <= t + 0.5] or [None], key=lambda x: x or -1)
        next_t = min([l['top'] for l in lines if l['top'] >= b - 0.5] or [None], key=lambda x: x or 1e9)
        t2, b2 = t, b
        def ours(im):  # the line the image overlaps most (a fraction sits higher than its line); a free-standing figure by area
            ov = [(min(im['bottom'], l['bottom']) - max(im['top'], l['top']), l) for l in lines]
            best = max(ov, key=lambda x: x[0], default=(0, None))
            if best[0] > 0: return best[1] in own
            return min(im['bottom'], b) - max(im['top'], t) > (im['bottom'] - im['top']) / 2
        for im in P['images']:
            if im['top'] < t < im['bottom']:
                t2 = min(t2, im['top'] - 0.5) if ours(im) else max(t2, im['bottom'] + 0.5)
            if im['top'] < b < im['bottom']:
                b2 = max(b2, im['bottom'] + 0.5) if ours(im) else min(b2, im['top'] - 0.5)
        if prev_b is not None: t2 = max(t2, prev_b + 0.3)
        if next_t is not None: b2 = min(b2, next_t - 0.3)
        if own: t2, b2 = min(t2, min(l['top'] for l in own) - 0.3), max(b2, max(l['bottom'] for l in own) + 0.3)
        for a in ads:  # an ad line (seller's name, 公众号) at the start or end of the region is left out
            if own and a['top'] >= max(l['bottom'] for l in own):
                last = max([l['bottom'] for l in own] + [im['bottom'] for im in P['images'] if t < im['top'] < a['top']])
                b2 = min(b2, last + 2)
            elif own and a['bottom'] <= min(l['top'] for l in own):
                t2 = max(t2, a['bottom'] + 0.5)
        if drop_slivers and len(regs) > 1 and not own and b - t < 12:
            changed = True; continue
        out[pg] = [round(t2, 1), round(b2, 1)]
        changed |= abs(t2 - t) > 0.2 or abs(b2 - b) > 0.2
    return out if changed else None

def snap(r):
    return snap_regions(r['jfile'], r['jiexi_regions'])

def snap_q(r):
    return snap_regions(r['qfile'], r['regions'], drop_slivers=True)

def snap_all(raw, ids=None):
    """after any rebuild of db/zl_raw.json: snap 解析 and question regions, re-crop what changed"""
    n = 0
    for r in raw:
        if ids is not None and r['id'] not in ids: continue
        if r.get('jiexi_regions') and not r['paper'].startswith('MK'):
            new = snap(r)
            if new:
                print('snap j', r['id'], r['jiexi_regions'], '->', new)
                r['jiexi_regions'] = new; C.build_jiexi([r], force=True); n += 1
        if r.get('regions'):
            new = snap_q(r)
            if new:
                print('snap q', r['id'], r['regions'], '->', new)
                r['regions'] = new; C.build([r], force=True); n += 1
    return n

if __name__ == '__main__':
    todo = {'2015GK-Z119': 'C', '2017JSA-Z135': 'C', '2019ZJA-Z126': 'C'}
    raw = json.load(open(S + '/db/zl_raw.json'))
    by = {r['id']: r for r in raw}
    fix = json.load(open(S + '/db/zl_fixes.json'))
    for i, ans in todo.items():
        r = by[i]
        regs = locate(r['jfile'], r['num'])
        r['jiexi_regions'] = regs
        C.build_jiexi([r], force=True)
        fix[i] = {'answer': ans, 'source': '官方解析（手动定位）'}
        print(i, regs)
    # the question before a hand-located one ran on into its 解析: end it where the located question starts
    for i in todo:
        r = by[i]; prev = by.get(f"{r['paper']}-Z{r['num'] - 1}")
        if not prev or not prev.get('jiexi_regions'): continue
        p0 = sorted(r['jiexi_regions'], key=int)[0]; t0 = r['jiexi_regions'][p0][0]
        regs = {k: v for k, v in prev['jiexi_regions'].items() if int(k) <= int(p0)}
        if p0 in regs and regs[p0][0] < t0 < regs[p0][1]:
            regs[p0] = [regs[p0][0], round(t0 - 1, 1)]
            prev['jiexi_regions'] = regs
            C.build_jiexi([prev], force=True)
            print('trimmed', prev['id'], regs)
    # 2024 河北 124: the 解析 heading prints 正确答案D, its own working (1348.0×20.03%×1.0556≈285) and the data give C
    fix['2024HB-Z124'] = {'answer': 'C', 'override': True, 'source': '核算更正',
                          'extra': '原解析标题印的是“正确答案D”，但解析过程算得约 285 万吨，按材料数据核算也是 285 万吨，答案应为 C；D（291）是误用 2022 年总量得到的干扰项。'}
    print('snapped', snap_all(raw))
    json.dump(raw, open(S + '/db/zl_raw.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(fix, open(S + '/db/zl_fixes.json', 'w'), ensure_ascii=False, indent=1)
