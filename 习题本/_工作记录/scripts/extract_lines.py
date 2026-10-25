# Extract line-level text with coordinates + images from all text-based PDFs
import pdfplumber, json, os, sys, glob, re, logging
logging.disable(logging.WARNING)
SRC = '/home/user/xingce'
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/lines'
os.makedirs(OUT, exist_ok=True)
def page_lines(p):
    words = p.extract_words(keep_blank_chars=True, x_tolerance=1.5, y_tolerance=2, use_text_flow=False)
    words.sort(key=lambda w: (round(w['top']), w['x0']))
    lines = []
    for w in words:
        if lines and abs(w['top'] - lines[-1]['top']) < 3.5:
            L = lines[-1]
            gap = w['x0'] - L['x1']
            L['text'] += (' ' * max(1, int(gap / 6)) if gap > 3 else '') + w['text']
            L['x1'] = max(L['x1'], w['x1']); L['bottom'] = max(L['bottom'], w['bottom'])
            L['words'].append([round(w['x0'],1), round(w['x1'],1)])
        else:
            lines.append({'top': w['top'], 'bottom': w['bottom'], 'x0': w['x0'], 'x1': w['x1'], 'text': w['text'], 'words': [[round(w['x0'],1), round(w['x1'],1)]]})
    # re-sort words within line by x (they were sorted by rounded top first)
    for L in lines:
        L['top'] = round(L['top'], 1); L['bottom'] = round(L['bottom'], 1); L['x0'] = round(L['x0'], 1); L['x1'] = round(L['x1'], 1)
    return lines
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
for f in sorted(glob.glob(os.path.join(SRC, '*.pdf'))):
    name = os.path.basename(f)[:-4]
    outp = os.path.join(OUT, name + '.json')
    if os.path.exists(outp): continue
    try:
        pdf = pdfplumber.open(f)
    except Exception as e:
        print('ERR', name, e); continue
    pages = []
    for i, p in enumerate(pdf.pages):
        try:
            lines = page_lines_sorted(p)
            imgs = [{'x0': round(im['x0'],1), 'top': round(im['top'],1), 'x1': round(im['x1'],1), 'bottom': round(im['bottom'],1), 'w': im.get('srcsize',[0,0])[0], 'h': im.get('srcsize',[0,0])[1]} for im in p.images]
            curves = [[round(c['x0'],1), round(c['top'],1), round(c['x1'],1), round(c['bottom'],1)] for c in (p.curves + p.lines + p.rects)]
        except Exception as e:
            print('PAGE ERR', name, i, e); lines, imgs, curves = [], [], []
        pages.append({'page': i + 1, 'width': float(p.width), 'height': float(p.height), 'lines': lines, 'images': imgs, 'vec': curves})
    json.dump({'name': name, 'pages': pages}, open(outp, 'w'), ensure_ascii=False)
    print('OK', name, len(pages), sum(len(pg['lines']) for pg in pages), flush=True)
