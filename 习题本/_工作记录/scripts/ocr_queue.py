# Page-level resumable OCR queue. usage: python3 ocr_queue.py <workers> <pdf1> <pdf2> ...
import os, sys, json, subprocess, glob
from multiprocessing import Pool
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SRC = '/home/user/xingce'
OD = S + os.environ.get('OCR_DIR', '/ocr2')
def stem(p): return os.path.basename(p)[:-4]
def render(pdf):
    d = os.path.join(OD, stem(pdf)); os.makedirs(d + '/img', exist_ok=True)
    n = int([l for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.split('\n') if l.startswith('Pages')][0].split()[1])
    have = len(glob.glob(d + '/img/p-*.png'))
    if have < n:
        subprocess.run(['pdftoppm', '-scale-to', '3508', '-gray', '-png', pdf, d + '/img/p'], check=True)
    return [(pdf, p) for p in sorted(glob.glob(d + '/img/p-*.png'))]
_eng = None
def work(job):
    global _eng
    pdf, png = job
    out = png.replace('/img/', '/res/')[:-4] + '.json'
    if os.path.exists(out): return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if _eng is None:
        from rapidocr_onnxruntime import RapidOCR
        _eng = RapidOCR()
    r, _ = _eng(png)
    items = [{'box': [[float(x), float(y)] for x, y in b], 'text': t, 'conf': float(c)} for b, t, c in (r or [])]
    json.dump(items, open(out, 'w'), ensure_ascii=False)
    return out
if __name__ == '__main__':
    nw = int(sys.argv[1]); pdfs = [os.path.join(SRC, p) if not p.startswith('/') else p for p in sys.argv[2:]]
    jobs = []
    for pdf in pdfs: jobs += render(pdf)
    print('pages', len(jobs), flush=True)
    os.environ['ORT_THREADS'] = '1'
    with Pool(nw) as pool:
        for i, o in enumerate(pool.imap_unordered(work, jobs), 1):
            if i % 10 == 0: print('done', i, '/', len(jobs), flush=True)
    print('ALLDONE', flush=True)
