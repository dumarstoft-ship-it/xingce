import json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from split_q import load, flat_lines, split
import answers as A
from papers import PAPERS
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
PLACEHOLDER = re.compile(r'题目正在全力以赴征集|正在征集|暂缺|题目缺失')

def kind_judge(t):
    s = re.sub(r'\s+', '', t)
    if re.search(r'图形|所给图|折叠|拼接|拼合|视图|截面|立体图|展开图|问号处|呈现一定的规律|规律性|左边给定|外表面|分为两类|一类图形|下图|如图', s) and not re.search(r'定义', s) and len(re.sub(r'[A-D][\.、．]\s*[A-D]', '', s)) < 160:
        return '图推'
    if re.search(r'(根据|按照)(上述|以上|题干)?.{0,8}定义|符合.{0,12}定义|不符合.{0,10}定义', s):
        return '定义'
    if re.search(r'逻辑关系最为?(相似|贴近|接近|一致)|依次填入[划画]横线|相当于', s) and not re.search(r'推理|论证|结构|论点', s[:120]):
        return '类比'
    if re.match(r'^\d+[\.、．]?[一-龥]{1,8}[：:][一-龥]{1,8}', s) and len(s) < 120:
        return '类比'
    return '逻辑'

def is_numseq(t):
    first = t.split('\n')[0]
    body = re.sub(r'^\s*\d{1,3}\s*[\.、．]?', '', first)
    han = len(re.findall(r'[一-龥]', body))
    digits = len(re.findall(r'\d', body))
    return (han <= 2 and digits >= 4) or ('数列' in t and han < 30)

def decor_images(doc):
    c = Counter()
    for pg in doc['pages']:
        for im in pg['images']:
            c[(round(im['x0']), round(im['top']), round(im['x1']), round(im['bottom']))] += 1
    n = len(doc['pages'])
    return {k for k, v in c.items() if v >= max(3, n * 0.3)}

JUNKL = re.compile(r'认准淘宝|通关达人|本试卷由粉笔|微信|公众号|免费获取|考公资料|^\s*[-—]?\s*\d+\s*[-—]?\s*$|^\s*\d+\s*/\s*\d+\s*$|第\s*\d+\s*[页⻚]')
_HF = {}
def hf_texts(doc):
    """header/footer texts: normalized lines near top/bottom repeating on >=30% of pages"""
    key = doc.get('name')
    if key in _HF: return _HF[key]
    c = Counter()
    for pg in doc['pages']:
        H = pg['height']; seen = set()
        for L in pg['lines']:
            if L['top'] < 0.09 * H or L['top'] > 0.88 * H:
                t = re.sub(r'\d+|\s+', '', L['text'])
                if t and t not in seen: seen.add(t); c[t] += 1
    n = len(doc['pages'])
    _HF[key] = {t for t, v in c.items() if v >= max(3, 0.3 * n)}
    return _HF[key]
def _is_content(L, pg, hf):
    t = L['text']
    if not t.strip() or JUNKL.search(t): return False
    H = pg['height']
    if (L['top'] < 0.09 * H or L['top'] > 0.88 * H) and re.sub(r'\d+|\s+', '', t) in hf: return False
    return True
def _okimg(im, pg, deco):
    H = pg['height']
    key = (round(im['x0']), round(im['top']), round(im['x1']), round(im['bottom']))
    return key not in deco and im['top'] > 0.035 * H and im['bottom'] < 0.97 * H and (im['x1'] - im['x0']) < 0.97 * pg['width']
def content_bottom(pg, deco=frozenset(), hf=frozenset()):
    H = pg['height']
    ls = [L['bottom'] for L in pg['lines'] if _is_content(L, pg, hf)]
    ims = [im['bottom'] for im in pg['images'] if _okimg(im, pg, deco)]
    return max(ls + ims + [0.1 * H])

def content_top(pg, deco=frozenset(), hf=frozenset()):
    H = pg['height']
    ls = [L['top'] for L in pg['lines'] if _is_content(L, pg, hf)]
    ims = [im['top'] for im in pg['images'] if _okimg(im, pg, deco)]
    return min(ls + ims + [0.9 * H])

def span_regions(doc, p0, t0, p1, t1, deco=frozenset()):
    """regions from (p0,t0) to (p1,t1) exclusive end."""
    pages = {pg['page']: pg for pg in doc['pages']}
    hf = hf_texts(doc)
    regs = {}
    for p in range(p0, p1 + 1):
        pg = pages[p]
        top = t0 - 2 if p == p0 else content_top(pg, deco, hf) - 2
        bot = t1 - 0.5 if p == p1 else content_bottom(pg, deco, hf) + 2
        if bot - top > 4:
            regs[str(p)] = [round(top, 1), round(bot, 1)]
    return regs

def lines_regions(lines):
    regs = {}
    for L in lines:
        r = regs.setdefault(str(L['page']), [L['top'] - 2, L['bottom'] + 2])
        r[0] = min(r[0], L['top'] - 2); r[1] = max(r[1], L['bottom'] + 2)
    return {k: [round(v[0], 1), round(v[1], 1)] for k, v in regs.items()}

def imgs_in(doc, regs, deco):
    pages = {pg['page']: pg for pg in doc['pages']}
    out = []
    for p, (t, b) in regs.items():
        for im in pages[int(p)]['images']:
            key = (round(im['x0']), round(im['top']), round(im['x1']), round(im['bottom']))
            if key in deco: continue
            if im['bottom'] > t and im['top'] < b: out.append(dict(im, page=int(p)))
    return out

def build_paper(code, disp, qfile, jfile):
    out = []
    if qfile.startswith('OCR:'): return out, 'ocr-pending'
    doc = load(qfile)
    res, heads, lines = split(qfile)
    deco = decor_images(doc)
    answers, segs, starts, jdoc, jdeco = {}, {}, [], None, set()
    if jfile and not jfile.startswith('OCR:'):
        answers, segs = A.parse_answers(jfile)
        starts = list(A.STARTS)
        jdoc = load(jfile); jdeco = decor_images(jdoc)
    jpos = {n: (p, t) for n, p, t in starts}
    jnext = {}
    for k, (n, p, t) in enumerate(starts):
        if k + 1 < len(starts): jnext[n] = (starts[k + 1][1], starts[k + 1][2])
    for idx, q in enumerate(res):
        same_next = idx + 1 < len(res) and res[idx + 1]['section'] == q['section'] and 'stem_lines' not in res[idx + 1] and not q.get('closed')
        if same_next:
            nf = res[idx + 1]['lines'][0]
            regs = span_regions(doc, q['lines'][0]['page'], q['lines'][0]['top'], nf['page'], nf['top'], deco)
        else:
            regs = lines_regions(q['lines'])
        stem_regs = lines_regions(q['stem_lines']) if q.get('stem_lines') else {}
        text = q['text']
        if q['section'] == '数量关系':
            kind = '数字推理' if is_numseq(text) else '数学运算'
        else:
            kind = kind_judge(text)
        if PLACEHOLDER.search(text): kind = '缺题'
        jregs = {}
        if q['num'] in jpos:
            p0, t0 = jpos[q['num']]
            if q['num'] in jnext:
                p1, t1 = jnext[q['num']]
                if p1 - p0 <= 3:
                    jregs = span_regions(jdoc, p0, t0, p1, t1, jdeco)
            if not jregs:
                jregs = lines_regions([dict(page=p, top=t, bottom=b) for (p, t, b) in A.LINES.get(q['num'], [])]) if hasattr(A, 'LINES') else {}
        rec = {'id': f'{code}-{q["num"]}', 'paper': code, 'paper_name': disp, 'qfile': qfile, 'num': q['num'], 'section': q['section'], 'kind': kind,
               'text': text, 'stem_text': '\n'.join(L['text'] for L in q.get('stem_lines', [])) or None,
               'regions': regs, 'stem_regions': stem_regs, 'images': imgs_in(doc, regs, deco),
               'answer_official': answers.get(q['num']), 'jfile': jfile, 'jiexi_raw': segs.get(q['num']),
               'jiexi_regions': jregs, 'jiexi_images': imgs_in(jdoc, jregs, jdeco) if jdoc and jregs else []}
        out.append(rec)
    return out, 'ok'

def apply_overrides(allq):
    p = S + '/db/overrides.json'
    if not os.path.exists(p): return
    ov = json.load(open(p))
    by = {r['id']: r for r in allq}
    for qid, o in ov.items():
        r = by.get(qid)
        if not r: continue
        if 'regions' in o:  # hand-trimmed question regions (next question's material removed)
            r['regions'] = o['regions']
        if 'jiexi_regions' in o:  # hand-trimmed 解析 regions (next question's 解析 / unrelated material removed)
            r['jiexi_regions'] = o['jiexi_regions']
        if 'cut_before_re' in o:  # inline answer lines printed under the question (2026CQ / 2026GZ)
            pat = re.compile(o['cut_before_re'])
            doc = load(r['qfile'])
            pages = {pg['page']: pg for pg in doc['pages']}
            for pk in sorted(r['regions'], key=int):
                t, b = r['regions'][pk]
                hit = [L for L in pages[int(pk)]['lines'] if pat.search(L['text']) and t <= L['top'] <= b]
                if hit:
                    r['regions'][pk] = [t, round(hit[0]['top'] - 0.5, 1)]
                    for later in [k for k in r['regions'] if int(k) > int(pk)]: del r['regions'][later]
                    r['text'] = pat.split(r['text'])[0].rstrip()
                    break
        if 'cut_before' in o:
            doc = load(r['qfile'])
            pages = {pg['page']: pg for pg in doc['pages']}
            for pk in sorted(r['regions'], key=int):
                t, b = r['regions'][pk]
                hit = [L for L in pages[int(pk)]['lines'] if o['cut_before'] in L['text'] and t <= L['top'] <= b]
                if hit:
                    r['regions'][pk] = [t, round(hit[0]['top'] - 0.5, 1)]
                    for later in [k for k in r['regions'] if int(k) > int(pk)]: del r['regions'][later]
                    r['text'] = r['text'].split(o['cut_before'])[0]
                    break


if __name__ == '__main__':
    allq = []
    for code, disp, qf, jf in PAPERS:
        A.LINES = {}; A.STARTS = []
        recs, st = build_paper(code, disp, qf, jf)
        allq.extend(recs)
        c = Counter(r['kind'] for r in recs)
        na = sum(1 for r in recs if r['kind'] in ('数学运算', '逻辑') and r['answer_official'] is None)
        print(code.ljust(11), st, dict(c), 'noans:', na)
    apply_overrides(allq)
    json.dump(allq, open(S + '/db/real_raw.json', 'w'), ensure_ascii=False, indent=0)
    print('TOTAL', Counter(r['kind'] for r in allq))
