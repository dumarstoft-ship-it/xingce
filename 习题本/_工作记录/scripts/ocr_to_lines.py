"""Convert page-level OCR results (ocr2/<stem>/res/p-XX.json, 300dpi pixels) into lines JSON (PDF points)."""
import json, os, glob, sys, subprocess
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce'
SC = 72.0 / 300.0

def page_sizes(pdf):
    """MediaBox sizes (pdftoppm renders the MediaBox by default)."""
    out = subprocess.run(['pdfinfo', '-box', '-f', '1', '-l', '999', pdf], capture_output=True, text=True).stdout
    sizes = {}
    for l in out.split('\n'):
        if l.startswith('Page') and 'MediaBox:' in l:
            parts = l.split()
            n = int(parts[1]); x0, y0, x1, y1 = map(float, parts[3:7])
            sizes[n] = (x1 - x0, y1 - y0)
    return sizes

def convert(stem):
    d = f'{S}/ocr3/{stem}' if os.path.exists(f'{S}/ocr3/{stem}') else f'{S}/ocr2/{stem}'
    res = sorted(glob.glob(d + '/res/p-*.json'))
    sizes = page_sizes(os.path.join(SRC, stem + '.pdf'))
    pages = []
    for f in res:
        pno = int(os.path.basename(f)[2:-5])
        items = json.load(open(f))
        from PIL import Image
        imgf = f.replace('/res/', '/img/')[:-5] + '.png'
        w0, h0 = sizes.get(pno, (595.0, 842.0))
        SC = w0 / Image.open(imgf).size[0] if os.path.exists(imgf) else 72.0 / 300.0
        boxes = []
        for it in items:
            xs = [p[0] for p in it['box']]; ys = [p[1] for p in it['box']]
            boxes.append({'x0': min(xs) * SC, 'x1': max(xs) * SC, 'top': min(ys) * SC, 'bottom': max(ys) * SC, 'text': it['text'], 'conf': it['conf']})
        boxes.sort(key=lambda b: ((b['top'] + b['bottom']) / 2, b['x0']))
        rows = []
        for b in boxes:
            placed = False
            for r in rows[-3:][::-1]:
                ov = min(r['bottom'], b['bottom']) - max(r['top'], b['top'])
                h = min(r['bottom'] - r['top'], b['bottom'] - b['top'])
                if h > 0 and ov >= 0.5 * h:
                    r['items'].append(b); r['top'] = min(r['top'], b['top']); r['bottom'] = max(r['bottom'], b['bottom']); placed = True; break
            if not placed:
                rows.append({'top': b['top'], 'bottom': b['bottom'], 'items': [b]})
        lines = []
        for r in sorted(rows, key=lambda r: r['top']):
            its = sorted(r['items'], key=lambda b: b['x0'])
            text = ''; x1 = None
            for b in its:
                if x1 is not None and b['x0'] - x1 > 4: text += ' ' * max(1, int((b['x0'] - x1) / 6))
                text += b['text']; x1 = b['x1']
            lines.append({'top': round(r['top'], 1), 'bottom': round(r['bottom'], 1), 'x0': round(its[0]['x0'], 1), 'x1': round(max(b['x1'] for b in its), 1), 'text': text})
        w, h = sizes.get(pno, (595.0, 842.0))
        pages.append({'page': pno, 'width': w, 'height': h, 'lines': lines, 'images': [], 'vec': []})
    pages.sort(key=lambda p: p['page'])
    json.dump({'name': stem, 'pages': pages, 'ocr': True}, open(f'{S}/lines/{stem}.json', 'w'), ensure_ascii=False)
    print('ok', stem, len(pages), sum(len(p['lines']) for p in pages))

if __name__ == '__main__':
    for st in sys.argv[1:]:
        convert(st)
