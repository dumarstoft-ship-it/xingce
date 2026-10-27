import json, re, sys
sys.path.insert(0, '/home/user/xingce/习题本/_工作记录/scripts')
from split_q import load
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json')); by = {r['id']: r for r in raw}
H = open(S + '/zl/out/zl_d8-14.html').read()
toks = re.findall(r'(<span class="t">[^<]+</span>|<div class="mat-h">[^<]+</div>|src="file://[^"]+/([^/"]+)_q\.png")', H)
st = None; mat = None; passages = []
for t in toks:
    s = t[0]
    if s.startswith('<span class="t">'): st = re.sub('<[^>]+>', '', s).strip()
    elif s.startswith('<div class="mat-h">'): mat = re.sub('<[^>]+>', '', s)[:3]; passages.append((st, mat, []))
    elif t[1]: passages[-1][2].append(t[1])
HF = re.compile(r'本试卷由粉笔用户|粉笔|第\s*\d+\s*[页⻚]|^\s*\d+\s*/\s*\d+\s*$|共\s*\d+\s*页|模考大赛|^\s*[-—]?\s*\d+\s*[-—]?\s*$')
def segs(regions):
    return [(int(p), t, b) for p, (t, b) in sorted(regions.items(), key=lambda x: int(x[0]))]
for st, mat, ids in passages:
    rs = [by[i] for i in ids]
    d = load(rs[0]['qfile'])
    order = [('stem', segs(rs[0]['stem_regions']))] + [(f"q{k+1}", segs(r['regions'])) for k, r in enumerate(rs)]
    # flatten into (page, top, bottom, label)
    flat = [(p, t, b, lab) for lab, ss in order for p, t, b in ss]
    pages = sorted({p for p, _, _, _ in flat})
    issues = []
    # lines on these pages between first and last covered positions that are not covered by any region
    first = min((p, t) for p, t, b, _ in flat); last = max((p, b) for p, t, b, _ in flat)
    for p in pages:
        pg = d['pages'][p - 1]
        for L in pg['lines']:
            if not L['text'].strip(): continue
            mid = (L['top'] + L['bottom']) / 2
            if (p, mid) < first or (p, mid) > last: continue
            if any(pp == p and t - 0.5 <= mid <= b + 0.5 for pp, t, b, _ in flat): continue
            if HF.search(L['text']): continue
            issues.append(f"   p{p}@{L['top']:.0f}: {L['text'][:80]}")
    # also: lines just after the last question (next 30pt) and just before the stem (previous 60pt)
    pre = []
    p0, t0 = first
    for L in d['pages'][p0 - 1]['lines']:
        if t0 - 70 < L['bottom'] <= t0 + 0.5 and L['text'].strip() and not HF.search(L['text']): pre.append(f"   pre p{p0}@{L['top']:.0f}: {L['text'][:80]}")
    if issues or pre:
        print(st, mat, ids[0], rs[0]['qfile'].split('/')[-1][:40])
        for x in pre: print(x)
        for x in issues: print(x)
