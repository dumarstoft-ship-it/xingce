"""Mock papers (模考) for 资料分析: fetch the user's uploaded PDFs from a remote branch into scratch/mock, extract
line JSON next to each PDF (absolute stems work with the crop code: os.path.join ignores SRC for absolute paths),
pair question books with their 解析, and register them for zl_build (db/mock_papers.json)."""
import json, os, re, sys, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
REPO = '/home/user/xingce'
MD = S + '/mock'

def fetch(ref, pattern=r'\.pdf$'):
    os.makedirs(MD, exist_ok=True)
    known = set(subprocess.run(['git', '-c', 'core.quotepath=false', '-C', REPO, 'ls-tree', '-r', '--name-only', 'HEAD'], capture_output=True, text=True).stdout.split('\n'))
    files = [f for f in subprocess.run(['git', '-c', 'core.quotepath=false', '-C', REPO, 'ls-tree', '-r', '--name-only', ref], capture_output=True, text=True).stdout.split('\n')
             if f and re.search(pattern, f, re.I) and f not in known]
    out = []
    for f in files:
        dst = os.path.join(MD, f.replace('/', '__'))
        if not os.path.exists(dst):
            data = subprocess.run(['git', '-C', REPO, 'show', f'{ref}:{f}'], capture_output=True).stdout
            open(dst, 'wb').write(data)
        out.append(dst)
    return out

def page_lines_sorted(p):
    words = p.extract_words(keep_blank_chars=True, x_tolerance=1.5, y_tolerance=2, use_text_flow=False)
    words.sort(key=lambda w: ((w['top'] + w['bottom']) / 2, w['x0']))
    rows = []  # each: [top, bottom, words]
    for w in words:
        placed = False
        for r in rows[-3:][::-1]:
            ov = min(r[1], w['bottom']) - max(r[0], w['top'])
            h = min(r[1] - r[0], w['bottom'] - w['top'])
            if h > 0 and ov >= 0.45 * h:
                r[2].append(w); r[0] = min(r[0], w['top']); r[1] = max(r[1], w['bottom']); placed = True; break
        if not placed:
            rows.append([w['top'], w['bottom'], [w]])
    rows.sort(key=lambda r: r[0])
    lines = []
    for top, bottom, ws in rows:
        ws.sort(key=lambda w: w['x0'])
        text = ''; x1 = None
        for w in ws:
            if x1 is not None:
                gap = w['x0'] - x1
                if gap > 3: text += ' ' * max(1, int(gap / 6))
            text += w['text']; x1 = w['x1']
        lines.append({'top': round(top,1), 'bottom': round(bottom,1),
                      'x0': round(ws[0]['x0'],1), 'x1': round(max(w['x1'] for w in ws),1), 'text': text})
    return lines

def extract(pdf):
    import pdfplumber, logging
    logging.disable(logging.WARNING)
    stem = pdf[:-4]
    if os.path.exists(stem + '.json'): return stem
    doc = pdfplumber.open(pdf); pages = []
    for i, p in enumerate(doc.pages):
        try:
            lines = page_lines_sorted(p)
            imgs = [{'x0': round(im['x0'], 1), 'top': round(im['top'], 1), 'x1': round(im['x1'], 1), 'bottom': round(im['bottom'], 1),
                     'w': im.get('srcsize', [0, 0])[0], 'h': im.get('srcsize', [0, 0])[1]} for im in p.images]
            curves = [[round(c['x0'], 1), round(c['top'], 1), round(c['x1'], 1), round(c['bottom'], 1)] for c in (p.curves + p.lines + p.rects)]
        except Exception as e:
            lines, imgs, curves = [], [], []
        pages.append({'page': i + 1, 'width': float(p.width), 'height': float(p.height), 'lines': lines, 'images': imgs, 'vec': curves})
    json.dump({'name': stem, 'pages': pages}, open(stem + '.json', 'w'), ensure_ascii=False)
    return stem

def pair(stems):
    """question book <-> 解析 by name with the 解析/答案 words removed"""
    def key(s):
        b = os.path.basename(s)
        return re.sub(r'[（(]?(?:参考)?(?:答案|解析|及|与|和|\+|【|】|详解|题本|试题|试卷|真题|题)[)）]?|[\s_\-—.]+', '', b)
    J = [s for s in stems if re.search(r'解析|答案|详解', os.path.basename(s))]
    Q = [s for s in stems if s not in J]
    out = []
    for q in Q:
        m = [j for j in J if key(j) == key(q)]
        out.append((q, m[0] if m else None))
    return out

CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
def season(name):
    m = re.search(r'第([一二三四五六七八九十]+)季', name)
    if not m:
        return 0
    s = m.group(1); v = 0
    if s == '十': return 10
    if '十' in s:
        a, b = s.split('十')
        v = (CN[a] if a else 1) * 10 + (CN[b] if b else 0)
    else:
        v = CN[s]
    return v

def extract_from(pdf, first_page):
    """line JSON for pages >= first_page only (the 资料分析 section); earlier pages are kept as empty placeholders"""
    import pdfplumber, logging
    logging.disable(logging.WARNING)
    stem = pdf[:-4]
    if os.path.exists(stem + '.json'): return stem
    doc = pdfplumber.open(pdf); pages = []
    for i, p in enumerate(doc.pages):
        if i + 1 < first_page:
            pages.append({'page': i + 1, 'width': float(p.width), 'height': float(p.height), 'lines': [], 'images': [], 'vec': []}); continue
        try:
            lines = page_lines_sorted(p)
            imgs = [{'x0': round(im['x0'], 1), 'top': round(im['top'], 1), 'x1': round(im['x1'], 1), 'bottom': round(im['bottom'], 1),
                     'w': im.get('srcsize', [0, 0])[0], 'h': im.get('srcsize', [0, 0])[1]} for im in p.images]
            curves = [[round(c['x0'], 1), round(c['top'], 1), round(c['x1'], 1), round(c['bottom'], 1)] for c in (p.curves + p.lines + p.rects)]
        except Exception as e:
            lines, imgs, curves = [], [], []
        pages.append({'page': i + 1, 'width': float(p.width), 'height': float(p.height), 'lines': lines, 'images': imgs, 'vec': curves})
    json.dump({'name': stem, 'pages': pages}, open(stem + '.json', 'w'), ensure_ascii=False)
    return stem

def register():
    reg = []
    for pdf in sorted(glob.glob(MD + '/*.pdf')):
        b = os.path.basename(pdf)
        if '模考' not in b or re.search(r'解析|答案', b): continue
        n = season(b); kind = '副省级' if '副省级' in b else ('地市级' if '地市级' in b else ('行政执法' if '行政执法' in b else ''))
        year = '2026' if b.startswith('国考模考试卷__2026') else '2027'
        code = f"MK{year[2:]}{n:02d}{ {'副省级': 'F', '地市级': 'D', '行政执法': 'X'}.get(kind, '') }" if n else f"MK{year[2:]}Z{ {'副省级': 'F', '地市级': 'D', '行政执法': 'X'}.get(kind, '') }"
        disp = f"{year}国考模考{'第' + str(n) + '季' if n else '终极'}（{kind}）"
        jpdf = [j for j in glob.glob(MD + '/*.pdf') if re.search(r'解析|答案', os.path.basename(j)) and season(os.path.basename(j)) == n and kind in os.path.basename(j) and os.path.basename(j)[:16] == b[:16]]
        reg.append([code, disp, pdf[:-4], jpdf[0][:-4] if jpdf else None])
    json.dump(reg, open(S + '/db/mock_papers.json', 'w'), ensure_ascii=False, indent=1)
    return reg

if __name__ == '__main__':
    import subprocess as sp
    for pdf in sorted(glob.glob(MD + '/*.pdf')):
        n = int(sp.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0])
        first = None
        for i in range(n, 0, -1):
            t = sp.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout
            if '资料分析' in t and re.search(r'资料分析[:：]|[一二三四五六七八]\s*[\.、．]\s*资料分析', t): first = i; break
        extract_from(pdf, max(1, (first or n - 8) - 1))
        print(os.path.basename(pdf), first, flush=True)
    print(len(register()))
