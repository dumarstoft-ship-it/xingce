import sys, os, json, subprocess, tempfile, glob
from rapidocr_onnxruntime import RapidOCR
pdf, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
eng = RapidOCR()
tmp = tempfile.mkdtemp(dir=outdir)
subprocess.run(['pdftoppm', '-r', '300', '-png', pdf, os.path.join(tmp, 'p')], check=True)
pages = sorted(glob.glob(os.path.join(tmp, 'p-*.png')))
res = []
for i, p in enumerate(pages):
    r, _ = eng(p)
    items = [{'box': b, 'text': t, 'conf': float(c)} for b, t, c in (r or [])]
    res.append({'page': i + 1, 'image': p, 'items': items})
    # reconstruct lines: sort by y then x
    print(f'page {i+1}/{len(pages)} items={len(items)}', flush=True)
json.dump(res, open(os.path.join(outdir, 'ocr.json'), 'w'), ensure_ascii=False)
# text by lines
lines = []
for pg in res:
    its = sorted(pg['items'], key=lambda it: (min(pt[1] for pt in it['box']), min(pt[0] for pt in it['box'])))
    rows = []
    for it in its:
        y0 = min(pt[1] for pt in it['box']); y1 = max(pt[1] for pt in it['box']); x0 = min(pt[0] for pt in it['box'])
        if rows and abs(((y0 + y1) / 2) - rows[-1]['yc']) < (y1 - y0) * 0.5:
            rows[-1]['its'].append((x0, it['text']))
        else:
            rows.append({'yc': (y0 + y1) / 2, 'its': [(x0, it['text'])]})
    lines.append(f'=====PAGE {pg["page"]}=====')
    for r in rows:
        lines.append('  '.join(t for x, t in sorted(r['its'])))
open(os.path.join(outdir, 'ocr.txt'), 'w').write('\n'.join(lines))
