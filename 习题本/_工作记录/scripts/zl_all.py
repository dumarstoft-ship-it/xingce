"""Build 资料 records for all candidate papers -> db/zl_raw.json; report material overlaps across papers."""
import json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zl_build as Z
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
SKIP = {'2020SZS', '2026JS', '2023SZ', '2023GKD', '2023GKX', '2022SZ', '2026GZ', '2021HB', '2022GKX', '2026HB'}
def shingles(t, k=6):
    t = re.sub(r'[\s\d\.%，。、；：:,;（）()“”"]+', '', t)
    return {t[i:i + k] for i in range(max(0, len(t) - k + 1))}
if __name__ == '__main__':
    P = Z.all_papers()
    allr = []
    for code in P:
        if code in SKIP or P[code][1].startswith('OCR:') or not os.path.exists(os.path.join(S, 'lines', P[code][1] + '.json')): continue
        try:
            recs, st = Z.records(code)
        except Exception as e:
            print(code, 'ERR', repr(e)[:100]); continue
        allr.extend(recs)
    rate = re.compile(r'正确率\s*[:：]?\s*(\d{1,3})\s*%')
    for r in allr:
        mm = rate.search(r.get('jiexi_raw') or '')
        r['acc'] = int(mm.group(1)) if mm else None
    json.dump(allr, open(S + '/db/zl_raw.json', 'w'), ensure_ascii=False, indent=0)
    mats = {}
    for r in allr:
        if r['pos'] == 1: mats[r['mat']] = shingles(r['stem_text'] + ''.join(x['text'] for x in allr if x['mat'] == r['mat'])[:0])
    # add question text to the signature (materials can be charts with little text)
    qtxt = defaultdict(str)
    for r in allr: qtxt[r['mat']] += r['text']
    sig = {m: mats[m] | shingles(qtxt[m]) for m in mats}
    keys = sorted(sig)
    dup = defaultdict(list)
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            A_, B_ = sig[keys[a]], sig[keys[b]]
            if not A_ or not B_: continue
            ov = len(A_ & B_) / min(len(A_), len(B_))
            if ov > 0.5 and keys[a].split('-')[0] != keys[b].split('-')[0]:
                dup[keys[a]].append((keys[b], round(ov, 2))); dup[keys[b]].append((keys[a], round(ov, 2)))
    json.dump(dup, open(S + '/db/zl_dups.json', 'w'), ensure_ascii=False, indent=0)
    print('records', len(allr), 'materials', len(mats))
    for m in keys:
        if dup.get(m): print(m, dup[m])
