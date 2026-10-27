"""资料分析 sets: split each paper's 资料分析 section into materials (shared stem) + questions, with 解析 regions.
Writes db/zl_raw.json (one record per question, grouped by 'mat' = <code>-M<k>)."""
import json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from split_q import load, flat_lines, is_heading, JUNKRE
import answers as A
from build_db import decor_images, hf_texts
from papers import PAPERS
from papers_new import PAPERS_NEW
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

QSTART = re.compile(r'^\s*(\d{1,3})\s*(?:[\.．、](?!\d{1,2}(?:\D|$)(?<!年))|[\.．、](?=(?:19|20)\d\d)|\s{1,}(?=\S)|(?=[一-龥（(“]))')
MATHEAD = re.compile(r'^\s*[（(]\s*(?:材料)?\s*[一二三四五六七八]\s*[)）]\s*$|^\s*[（(]\s*材料\s*[0-9一二三四五六七八]?\s*[)）]\s*$|^\s*[一二三四五六七八]\s*[、\.．]\s*(?:根据|阅读)|^\s*(?:材料|资料)\s*[一二三四五六七八]\s*$'
                     r'|根据(?:以下|下列|下面|如下|所给|给出的)?(?:材料|资料|图表|表格|统计|文字|图|表)\S{0,12}回答|回答\s*\d+\s*[~～\-－—至]\s*\d+\s*题|^\s*[（(]\s*[一二三四五六七八]\s*[)）]\s*(?:根据|阅读)')
OPT_D = re.compile(r'(?:^|\s)D\s*[\.．、:：]')

def all_papers():
    out = {c: (d, q, j) for c, d, q, j in PAPERS + PAPERS_NEW}
    mf = S + '/db/mock_papers.json'  # 粉笔 模考大赛 (absolute stems under scratchpad/mock)
    if os.path.exists(mf):
        for c, d, q, j in json.load(open(mf)): out[c] = (d, q, j)
    return out

def section_lines(qf):
    import unicodedata
    doc = load(qf)
    # some PDFs encode 行/比/文… as Kangxi radicals (⾏ ⽐ ⽂): normalise so the instruction / header patterns match
    lines = [dict(L, text=unicodedata.normalize('NFKC', L['text'])) for L in flat_lines(doc)]
    heads = [(i, is_heading(L['text'])) for i, L in enumerate(lines)]
    heads = [(i, h) for i, h in heads if h]
    zl = [i for i, h in heads if h == '资料分析']
    if not zl: return doc, [], None
    i0 = zl[-1]
    nxt = [i for i, h in heads if i > i0 and h != '资料分析']
    i1 = nxt[0] if nxt else len(lines)
    return doc, lines[i0 + 1:i1], lines[i0]

def q_chain(ls):
    """longest run of consecutive question numbers appearing in reading order"""
    cands = []
    for i, L in enumerate(ls):
        m = QSTART.match(L['text'])
        if m:
            n = int(m.group(1))
            if 1 <= n <= 200: cands.append((i, n))
    best = {}  # cand index -> (len, prev)
    for k, (i, n) in enumerate(cands):
        b = (1, None)
        for k2 in range(k - 1, -1, -1):
            i2, n2 = cands[k2]
            if n2 == n - 1 and best[k2][0] + 1 > b[0]:
                b = (best[k2][0] + 1, k2)
        best[k] = b
    if not best: return []
    k = max(best, key=lambda x: (best[x][0], -x))
    out = []
    while k is not None:
        out.append(cands[k]); k = best[k][1]
    return out[::-1]

def build_section(code):
    disp, qf, jf = all_papers()[code]
    doc, ls, hline = section_lines(qf)
    if not ls: return None, 'no-section'
    chain = q_chain(ls)
    if len(chain) < 5: return None, f'chain={len(chain)}'
    qidx = [i for i, _ in chain]
    nums = [n for _, n in chain]
    heads = [i for i, L in enumerate(ls) if MATHEAD.search(L['text']) and i < qidx[-1] and not QSTART.match(L['text'])]
    # groups: by headers when they split the chain sensibly, else by 5
    groups = []
    if heads:
        for h_k, h in enumerate(heads):
            hn = heads[h_k + 1] if h_k + 1 < len(heads) else len(ls)
            qs = [k for k, i in enumerate(qidx) if h < i < hn]
            if qs: groups.append((h, qs))
        # drop headers that are followed directly by another header (e.g. "（一）" then "根据以下资料…")
    covered = sum(len(q) for _, q in groups)
    if not groups or covered != len(chain) or any(len(q) < 3 for _, q in groups):
        groups = []
        for g0 in range(0, len(chain), 5):
            qs = list(range(g0, min(g0 + 5, len(chain))))
            if g0 == 0:
                start = -1  # material begins right after the section heading/instructions
            else:
                # material begins after the previous question's D option line
                pi = qidx[g0 - 1]
                dl = [j for j in range(pi, qidx[g0]) if OPT_D.search(ls[j]['text'])]
                start = dl[0] if dl else pi
            groups.append((start, qs))
        mode = 'by5'
    else:
        mode = 'heads'
    return dict(code=code, disp=disp, qf=qf, jf=jf, doc=doc, ls=ls, hline=hline, chain=chain, groups=groups, mode=mode), 'ok'

if __name__ == '__main__':
    P = all_papers()
    codes = sys.argv[1:] or list(P)
    for code in codes:
        if P[code][1].startswith('OCR:') or not os.path.exists(S + '/lines/' + P[code][1] + '.json'): continue
        sec, st = build_section(code)
        if not sec: print(code.ljust(9), st); continue
        nums = [n for _, n in sec['chain']]
        print(code.ljust(9), f"{nums[0]}-{nums[-1]} n={len(nums)}", sec['mode'], [len(q) for _, q in sec['groups']])

# ---------------------------------------------------------------- regions
INSTR = re.compile(r'所给出的|所给的|根据资料提供的信息|资料提供的信息|分析、比较|分析、计算|计算、处理|参考时限|共\s*\d+\s*题|每道题|作答|选出一[项个]|正确答案|最恰当|资料均有|若干个问题|文字、表[情格]|图形资料')

def decor_vec(doc):
    c = Counter()
    for pg in doc['pages']:
        for v in pg.get('vec', []):
            c[tuple(round(x) for x in v)] += 1
    n = len([pg for pg in doc['pages'] if pg['lines'] or pg['images']])
    return {k for k, v in c.items() if v >= max(3, n * 0.3)}

def _live(doc):
    """pages that were actually extracted (mock papers keep only the 资料 pages; the rest are empty placeholders)"""
    return [pg for pg in doc['pages'] if pg['lines'] or pg['images']]

def decor_images_zl(doc):
    c = Counter()
    pages = _live(doc)
    for pg in pages:
        for im in pg['images']:
            c[(round(im['x0']), round(im['top']), round(im['x1']), round(im['bottom']))] += 1
    return {k for k, v in c.items() if v >= max(3, len(pages) * 0.3)}

def hf_texts_zl(doc):
    """header/footer texts: normalized lines near top/bottom repeating on >=30% of the extracted pages"""
    c = Counter()
    pages = _live(doc)
    for pg in pages:
        H = pg['height']; seen = set()
        for L in pg['lines']:
            if L['top'] < 0.09 * H or L['top'] > 0.88 * H:
                t = re.sub(r'\d+|\s+', '', L['text'])
                if t and t not in seen: seen.add(t); c[t] += 1
    return {t for t, v in c.items() if v >= max(3, 0.3 * len(pages))}

_DV = {}
def doc_frame(doc):
    """per document: (decor images, decor vectors, header/footer texts, content top, content bottom, text x0, text x1)
    from the text lines that are not page furniture"""
    key = doc['name']
    if key in _DV: return _DV[key]
    deco, dvec, hf = decor_images_zl(doc), decor_vec(doc), hf_texts_zl(doc)
    tops, bots, xs0, xs1 = [], [], [], []
    for pg in doc['pages']:
        H = pg['height']
        ls = [L for L in pg['lines'] if L['text'].strip() and not JUNKRE.search(L['text'])
              and not ((L['top'] < 0.09 * H or L['top'] > 0.88 * H) and re.sub(r'\d+|\s+', '', L['text']) in hf)
              and not (L['top'] > 0.9 * H and re.match(r'^\s*[-—第]?\s*\d+\s*[-—页⻚]?\s*(?:/\s*\d+)?\s*$', L['text']))]
        if len(ls) < 3: continue
        tops.append(min(L['top'] for L in ls)); bots.append(max(L['bottom'] for L in ls))
        xs0 += [L['x0'] for L in ls if len(L['text'].strip()) > 15]; xs1 += [L['x1'] for L in ls if len(L['text'].strip()) > 15]
    def pct(a, q): a = sorted(a); return a[min(len(a) - 1, max(0, int(q * len(a))))] if a else None
    H = doc['pages'][0]['height']
    fr = (deco, dvec, hf, (pct(tops, 0.05) or 0.08 * H), (pct(bots, 0.95) or 0.92 * H), pct(xs0, 0.03) or 0, pct(xs1, 0.97) or 1e9)
    _DV[key] = fr
    return fr

def page_items(doc, pg):
    """content boxes on a page: text lines (not header/footer/junk), non-decor images and vector graphics, inside the
    document's content frame (header logos, footer boxes, margin watermarks and page-sized clip paths are dropped)"""
    deco, dvec, hf, ctop, cbot, tx0, tx1 = doc_frame(doc)
    H, W = pg['height'], pg['width']
    lo, hi = ctop - 6, cbot + 6
    out = []
    for L in pg['lines']:
        t = L['text']
        if not t.strip() or JUNKRE.search(t): continue
        if (L['top'] < 0.09 * H or L['top'] > 0.88 * H) and re.sub(r'\d+|\s+', '', t) in hf: continue
        if L['top'] > 0.9 * H and re.match(r'^\s*[-—第]?\s*\d+\s*[-—页⻚]?\s*(?:/\s*\d+)?\s*$', t): continue
        if L['bottom'] < lo or L['top'] > hi: continue
        out.append((L['x0'], L['top'], L['x1'], L['bottom']))
    for im in pg['images']:
        k = (round(im['x0']), round(im['top']), round(im['x1']), round(im['bottom']))
        if k in deco or (im['x1'] - im['x0']) > 0.97 * W: continue
        if im['bottom'] < lo or im['top'] > hi: continue
        out.append((im['x0'], im['top'], im['x1'], im['bottom']))
    for v in pg.get('vec', []):
        if tuple(round(x) for x in v) in dvec: continue
        if v[1] < 0 or v[3] > H or (v[2] - v[0]) > 0.97 * W: continue
        if v[3] < lo or v[1] > hi: continue
        if v[2] < tx0 - 8 or v[0] > tx1 + 8: continue  # margin ornaments / watermark pieces
        out.append(tuple(v))
    return out

def span(doc, p0, t0, p1, t1):
    """regions page -> [top, bottom] from (p0, t0) to (p1, t1) (exclusive), with content-aware page breaks"""
    pages = {pg['page']: pg for pg in doc['pages']}
    regs = {}
    for p in range(p0, p1 + 1):
        pg = pages[p]
        items = page_items(doc, pg)
        top = t0 - 2 if p == p0 else min([b[1] for b in items] + [0.9 * pg['height']]) - 2
        if p == p1:
            bot = t1 - 0.5
        else:
            bs = [b[3] for b in items if b[1] >= top - 1]
            bot = max(bs + [top]) + 2
        if bot - top > 4:
            regs[str(p)] = [round(top, 1), round(bot, 1)]
    return regs

def xextent(doc, regs, pad=4):
    pages = {pg['page']: pg for pg in doc['pages']}
    x0, x1 = 1e9, -1e9
    for p, (t, b) in regs.items():
        for (a, tt, c, bb) in page_items(doc, pages[int(p)]):
            if bb > t and tt < b:
                x0 = min(x0, a); x1 = max(x1, c)
    return (round(x0 - pad, 1), round(x1 + pad, 1)) if x1 > x0 else None

JCUT = re.compile(r'根据(?:以下|下列|下面|如下|所给)(?:材料|资料|图表|表格|文字)|回答\s*\d+\s*[~～\-－—至]\s*\d+\s*题|^\s*[（(]\s*[一二三四五六七八]\s*[)）]\s*$|^\s*第[一二三四五六七八]部分|^\s*[一二三四五六七八]\s*[、\.．]\s*资料分析|^\s*资料分析\s*$|^\s*[（(]\s*材料\s*[0-9一二三四五六七八]?\s*[)）]\s*$')
def cut_jiexi(jdoc, regs):
    """a 解析 region may run into the next passage's material (some 解析 files reprint it) or a section heading"""
    if not regs: return regs
    pages = {pg['page']: pg for pg in jdoc['pages']}
    keys = sorted(regs, key=int)
    first = True
    for k in keys:
        t, b = regs[k]
        for L in sorted(pages[int(k)]['lines'], key=lambda L: L['top']):
            if L['top'] < t + (6 if first else 0) or L['top'] > b: continue
            if JCUT.search(L['text']):
                out = {kk: regs[kk] for kk in keys if int(kk) < int(k)}
                if L['top'] - 1 - t > 4: out[k] = [t, round(L['top'] - 1, 1)]
                return out or regs
        first = False
    return regs

def records(code):
    sec, st = build_section(code)
    if not sec: return [], st
    doc, ls, chain, groups = sec['doc'], sec['ls'], sec['chain'], sec['groups']
    qidx = [i for i, _ in chain]
    nums = [n for _, n in chain]
    answers, segs, jstart = {}, {}, {}
    jdoc = None
    if sec['jf']:
        A.LINES = {}; A.STARTS = []
        answers, segs = A.parse_answers(sec['jf'])
        starts = list(A.STARTS); jlines = dict(A.LINES)
        jdoc = load(sec['jf'])
        jstart = {n: (p, t) for n, p, t in starts}
        jorder = [n for n, _, _ in starts]
    recs = []
    # where each material begins (just below its header / the instructions / the previous question's D line),
    # and where the previous group's last question ends; materials can be a bare chart image without text lines
    mbeg, pend, mstart = [], [], []
    for g, (h, qs) in enumerate(groups):
        f = qidx[qs[0]]
        if sec['mode'] == 'heads':
            s0 = h; inline = False
            hl = ls[h]['text']; m = MATHEAD.search(hl)
            if m and len(hl.strip()) - m.end() > 12 and not re.search(r'题[。.．:：]?\s*$', hl): inline = True
            pend.append((ls[h]['page'], ls[h]['top']))
        else:
            if g == 0:
                s0 = -1
            else:
                pi = qidx[qs[0] - 1]
                dl = [j for j in range(pi, f) if OPT_D.search(ls[j]['text'])]
                s0 = dl[0] if dl else pi
                pend.append((ls[s0]['page'], ls[s0]['bottom'] + 2.5))
            inline = False
        a = s0  # anchor: last line that is not material
        while a + 1 < f and not QSTART.match(ls[a + 1]['text']) and (MATHEAD.search(ls[a + 1]['text']) or (g == 0 and INSTR.search(ls[a + 1]['text']))):
            a += 1
        if inline:
            mbeg.append((ls[h]['page'], ls[h]['top'])); mstart.append(h)
        elif a >= 0:
            mbeg.append((ls[a]['page'], ls[a]['bottom'] + 0.5)); mstart.append(a + 1)
        else:
            H = sec['hline']; mbeg.append((H['page'], H['bottom'] + 0.5)); mstart.append(0)
    for g, (h, qs) in enumerate(groups):
        mat = f'{code}-M{g + 1}'
        s = mstart[g]; f = qidx[qs[0]]
        Lf = ls[f]
        stem_regs = span(doc, mbeg[g][0], mbeg[g][1], Lf['page'], Lf['top'])
        stem_text = '\n'.join(L['text'] for L in ls[s:f])
        head_text = ls[h]['text'] if (sec['mode'] == 'heads' and h >= 0) else None
        for j, k in enumerate(qs):
            i = qidx[k]; L = ls[i]
            if j + 1 < len(qs):
                E = ls[qidx[qs[j + 1]]]; end = (E['page'], E['top'])
            elif g + 1 < len(groups):
                end = pend[g + 1] if sec['mode'] == 'heads' else pend[g]
            else:
                dl = [x for x in range(i, len(ls)) if OPT_D.search(ls[x]['text'])]
                E = ls[dl[0]] if dl else ls[-1]
                end = (E['page'], E['bottom'] + 2.5)
            regs = span(doc, L['page'], L['top'], end[0], end[1])
            n = nums[k]
            text = '\n'.join(x['text'] for x in ls[i:(qidx[qs[j + 1]] if j + 1 < len(qs) else i + 8)])
            jregs = {}
            if jdoc is not None and n in jstart:
                p0, t0 = jstart[n]
                pos = jorder.index(n)
                if pos + 1 < len(jorder):
                    p1, t1 = jstart[jorder[pos + 1]]
                    if p1 - p0 <= 3: jregs = span(jdoc, p0, t0, p1, t1)
                if not jregs:
                    from build_db import lines_regions
                    jregs = lines_regions([dict(page=p, top=t, bottom=b) for (p, t, b) in jlines.get(n, [])])
                jregs = cut_jiexi(jdoc, jregs)
            recs.append({'id': f'{code}-Z{n}', 'paper': code, 'paper_name': sec['disp'], 'qfile': sec['qf'], 'jfile': sec['jf'], 'num': n,
                         'mat': mat, 'mat_idx': g + 1, 'pos': j + 1, 'mode': sec['mode'], 'head_text': head_text,
                         'text': text, 'stem_text': stem_text, 'stem_regions': stem_regs, 'regions': regs,
                         'answer_official': answers.get(n), 'jiexi_raw': segs.get(n), 'jiexi_regions': jregs})
    return recs, 'ok'
