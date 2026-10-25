"""Recompute each crop's display scale from the ink height of its text lines (the line-box heights from OCR'd
papers overestimate the font size, which made some scans print too small)."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from est_font import est_pt
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
TARGET = {'q': 10.0, 's': 10.0, 'j': 9.6}

def main():
    n = 0
    for d in ('crops/real2', 'crops/real2_nonum'):
        for p in glob.glob(f'{S}/{d}/*_[qsj].png'):
            kind = p[-5]
            js = json.load(open(p + '.json')) if os.path.exists(p + '.json') else {}
            e = est_pt(p)
            f = js.get('font_pt') or 10.5
            if not e: continue
            js['font_pt_ink'] = round(e, 2)
            # the ink estimate (plain text lines) is more reliable than the layout line boxes, which formulas
            # and OCR padding inflate; fall back to the layout value only when the ink value is implausible
            use = e if 6 <= e <= 16 else (f if 6 <= f <= 16 else None)
            if use is None: continue
            js['scale'] = round(max(0.7, min(1.4, TARGET[kind] / use)), 3)
            json.dump(js, open(p + '.json', 'w'))
            n += 1
    print('rescaled', n)

if __name__ == '__main__':
    main()
