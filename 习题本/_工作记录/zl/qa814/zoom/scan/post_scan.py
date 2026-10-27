import json, re, sys
sys.path.insert(0, '/home/user/xingce/习题本/_工作记录/scripts')
from split_q import load
from crop import JUNK
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json')); by = {r['id']: r for r in raw}
H = open(S + '/zl/out/zl_d8-14.html').read()
ids = re.findall(r'crops/zl/([^"/]+)_q\.png', H)
HF = re.compile(r'本试卷由粉笔用户|第\s*\d+\s*[页⻚]|^\s*\d+\s*/\s*\d+\s*$|共\s*\d+\s*页')
for k, i in enumerate(ids):
    r = by[i]; d = load(r['qfile'])
    # lines right after this question's region
    p, (t, b) = max(r['regions'].items(), key=lambda x: int(x[0]))
    pg = d['pages'][int(p) - 1]
    nxt = []
    for L in sorted(pg['lines'], key=lambda L: L['top']):
        if b - 0.5 < (L['top'] + L['bottom']) / 2 <= b + 40 and L['text'].strip() and not HF.search(L['text']):
            nxt.append(L['text'][:70])
    if nxt:
        first = nxt[0]
        ok = re.match(r'^\s*\d{1,3}\s*[\.．、]', first) or re.match(r'^\s*[（(]\s*[一二三四五六七八]\s*[)）]', first) or re.search(r'资料分析|根据.*回答', first)
        if not ok: print('POST', i, 'pos', r['pos'], '->', nxt[:2])
    # JUNK lines inside regions
    for regs in (r['regions'], r['stem_regions'] if r['pos'] == 1 else {}):
        for pp, (tt, bb) in regs.items():
            pgx = d['pages'][int(pp) - 1]
            js = [L for L in pgx['lines'] if JUNK.search(L['text']) and L['bottom'] > tt and L['top'] < bb]
            for J in js:
                over = [L['text'][:40] for L in pgx['lines'] if L is not J and not JUNK.search(L['text']) and L['bottom'] > J['top'] - 2 and L['top'] < J['bottom'] + 2]
                print('JUNKMASK', i, 'p', pp, repr(J['text'][:50]), 'overlaps content:' if over else '', over[:3])
