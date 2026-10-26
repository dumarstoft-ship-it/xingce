"""Teacher's 刷题课 (数量全真模拟套题 1–28): the 板书 PDFs embed each question as a clean screenshot (the red
handwriting is vector ink on top). Extract the images (pdfimages, ke/raw/Lnn), OCR them, drop the teacher's
logo header and duplicates, white out the question number and the source tag "（2020 福建）" (the workbook shows
neither on the question page), and record answers from the 答案 PDF. Writes ke/bank.json + ke/crops/Knn-q.png."""
import glob, json, os, re, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glyph_size import digit_height
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce/数量关系刷题课'
TAG = re.compile(r'^\s*(?:(\d{1,2})\s*[\.．、]\s*)?[（(]\s*(\d{4})\s*([^）)]{0,14})[）)]')
_eng = None

def ocr(path):
    global _eng
    if _eng is None:
        from rapidocr_onnxruntime import RapidOCR
        _eng = RapidOCR()
    r, _ = _eng(path)
    out = []
    for b, t, c in (r or []):
        xs = [p[0] for p in b]; ys = [p[1] for p in b]
        out.append({'x0': min(xs), 'x1': max(xs), 'top': min(ys), 'bottom': max(ys), 'text': t, 'conf': float(c)})
    out.sort(key=lambda b: ((b['top'] + b['bottom']) / 2, b['x0']))
    return out

def answers(lec):
    a = glob.glob(f'{SRC}/第{lec:02d}讲/*答案.pdf')[0]
    txt = subprocess.run(['pdftotext', a, '-'], capture_output=True, text=True).stdout
    return {int(n): x for n, x in re.findall(r'(\d{1,2})\s*[\.．、]\s*([A-D])', txt)}

def wcount(s):  # display width: CJK/fullwidth ~1 em, ASCII ~0.55 em
    return sum(1.0 if ord(ch) > 0x2E80 else 0.55 for ch in s)

def ink_cols(a, y0, y1):
    return (a[int(y0):int(y1) + 1] < 160).any(axis=0)

def norm(t): return re.sub(r'[\s，,。.：:、]', '', t or '')

def ocr_arr(arr):
    global _eng
    if _eng is None:
        from rapidocr_onnxruntime import RapidOCR
        _eng = RapidOCR()
    r, _ = _eng(np.stack([arr] * 3, axis=-1))
    return ''.join(t for _, t, _ in sorted(r or [], key=lambda x: min(p[0] for p in x[0])))

def find_cut(a, first, m):
    """x where the stem text starts after the number + source tag: candidate blank columns near the width
    estimate, accepted when OCR of the remainder starts with the stem's first characters."""
    y0, y1 = int(first['top']) - 3, int(first['bottom']) + 3
    frac = wcount(first['text'][:m.end()]) / max(1e-6, wcount(first['text']))
    est = first['x0'] + frac * (first['x1'] - first['x0'])
    cols = ink_cols(a, y0, y1)
    gaps = [c for c in range(int(first['x0']) + 5, int(min(len(cols) - 1, est + 120))) if not cols[c] and cols[c + 1]]
    want = norm(first['text'][m.end():])[:3]
    for c in sorted(gaps, key=lambda c: abs(c - est))[:12]:
        t = norm(ocr_arr(a[y0:y1 + 1, c - 1:min(a.shape[1], c + 260)]))
        if t[:3] == want or (len(want) >= 2 and t[:2] == want[:2] and not t.startswith(('）', ')'))):
            return c, True
    return int(est), False

def clean(img_path, boxes, first):
    """Crop below the logo header, white out number + source tag on the first stem line and pull the rest of
    that line left to the margin."""
    im = Image.open(img_path).convert('L'); a = np.asarray(im).copy()
    m = TAG.match(first['text'])
    y0, y1 = int(first['top']) - 3, int(first['bottom']) + 3
    ok = True
    if m:
        cut, ok = find_cut(a, first, m)
        x0 = int(first['x0'])
        line = a[y0:y1 + 1, cut:].copy()
        a[y0:y1 + 1, x0:] = 255
        a[y0:y1 + 1, x0:x0 + line.shape[1]] = line
    top = max(0, y0 - 6)
    a = a[top:]
    bb = Image.fromarray(255 - a).getbbox()
    out = Image.fromarray(a).crop((max(0, bb[0] - 6), max(0, bb[1] - 6), min(a.shape[1], bb[2] + 6), min(a.shape[0], bb[3] + 6)))
    return out, ((m.group(2) + ' ' + m.group(3).strip()) if m else None), ok

def first_line(p, boxes):
    """The stem's first line; when OCR missed it, OCR the first ink band under the logo header on its own."""
    f = next((b for b in boxes if TAG.match(b['text'])), None)
    if f: return f
    a = np.asarray(Image.open(p).convert('L'))
    head = max([b['bottom'] for b in boxes if re.search(r'牛牛|bili|小红书|抖音', b['text'])] or [0])
    rows = (a[int(head) + 4:] < 160).any(axis=1); y = 0
    while y < len(rows) and not rows[y]: y += 1
    y0 = y
    while y < len(rows) and rows[y]: y += 1
    y0 += int(head) + 4; y1 = y + int(head) + 4
    cols = (a[y0:y1] < 160).any(axis=0); xs = np.where(cols)[0]
    if not len(xs): return None
    t = ocr_arr(a[max(0, y0 - 2):y1 + 2])
    return {'x0': float(xs[0]), 'x1': float(xs[-1]), 'top': float(y0), 'bottom': float(y1), 'text': t} if TAG.match(t) else None

def main():
    bank = []
    for lec in range(1, 29):
        ans = answers(lec)
        imgs = sorted(glob.glob(f'{S}/ke/raw/L{lec:02d}/i-*.png'))
        seen = {}
        order = 0
        for p in imgs:
            boxes = ocr(p)
            # first stem line: numbered "2.（2020 福建）" (lectures 3+) or bare "（2019 安徽）" (lectures 1–2)
            first = first_line(p, boxes)
            if first is None:
                print('no stem start', p); continue
            m = TAG.match(first['text'])
            if m.group(1): num = int(m.group(1))
            else: order += 1; num = order
            if num in seen: continue
            crop, src, cut_ok = clean(p, boxes, first)
            out = f'{S}/ke/crops/K{lec:02d}-{num:02d}.png'
            crop.save(out)
            h = digit_height(out)
            scale = round(max(0.7, min(1.4, 10.5 / (h / 0.72 * 72 / 150))), 3) if h else 1.0
            # the renderer sizes crops as px / 200 dpi * scale: these screenshots are 150 dpi
            json.dump({'scale': round(scale * 200 / 150, 3), 'dpi': 150}, open(out + '.json', 'w'))
            text = '\n'.join(b['text'] for b in boxes if b['top'] >= first['top'] - 3)
            seen[num] = 1
            bank.append({'kid': f'K{lec:02d}-{num:02d}', 'lecture': lec, 'num': num, 'source': src, 'answer': ans.get(num),
                         'img': out, 'raw': p, 'text': text, 'cut_checked': cut_ok})
        missing = sorted(set(range(1, 11)) - set(seen))
        print(f'L{lec:02d}: {len(seen)} questions', 'missing', missing if missing else '', flush=True)
    json.dump(bank, open(S + '/ke/bank.json', 'w'), ensure_ascii=False, indent=1)
    print('total', len(bank))

if __name__ == '__main__':
    main()
