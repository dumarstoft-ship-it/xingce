import json, re, sys, os
sys.path.insert(0, '/home/user/xingce/习题本/_工作记录/scripts')
from split_q import load
from crop import doc_offset
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json')); by = {r['id']: r for r in raw}
H = open(S + '/zl/out/zl_d8-14.html').read()
toks = re.findall(r'(<span class="t">[^<]+</span>|<div class="mat-h">[^<]+</div>|<span class="no">\d+</span>|src="file://[^"]+/([^/"]+)\.png")', H)
st = None; mat = None; q = None; order = []
for t in toks:
    s = t[0]
    if s.startswith('<span class="t">'): st = re.sub('<[^>]+>', '', s).strip()
    elif s.startswith('<div class="mat-h">'): mat = re.sub('<[^>]+>', '', s)[:3]
    elif s.startswith('<span class="no">'): q = int(re.sub('<[^>]+>', '', s))
    else:
        b = t[1]
        if b.endswith('_q'): order.append((st, mat, f'Q{q}', b[:-2], 'q'))
        elif re.search(r'_p\d+$', b) and not b.endswith('_t'): order.append((st, mat, 'mat', re.sub(r'_p\d+$', '', b), b))
        elif b.endswith('_t'): order.append((st, mat, 'mat', re.sub(r'_p\d+_t$', '', b), b))
SUS = re.compile(r'粉笔|模考|大赛|行测|试卷|试题|真题|第\s*\d+\s*[页⻚]|共\s*\d+\s*页|^\s*\d+\s*/\s*\d+\s*$|资料分析|第[一二三四五六七八]部分|根据(?:以下|下列|下面|所给)?(?:资料|材料)[，,]?\s*回答|回答\s*\d+\s*[~～\-－—至]\s*\d+|参考答案|答案|解析|【|故正确|故选|正确答案|^\s*[（(]\s*[一二三四五六七八]\s*[)）]\s*$|本试卷|用户|淘宝|公众号|微信')
seen_mat = set()
def lines_in(stem, regions):
    d = load(stem); dy = 0  # line boxes are in pdf coords; regions are in the same coords
    out = []
    for p in sorted(regions, key=int):
        t0, b0 = regions[p]
        pg = d['pages'][int(p) - 1]
        for L in pg['lines']:
            mid = (L['top'] + L['bottom']) / 2
            if t0 <= mid <= b0: out.append((int(p), round(L['top'], 1), L['text']))
    return out
for st, mat, kind, rid, f in order:
    r = by[rid]
    if kind == 'mat':
        if rid in seen_mat: continue
        seen_mat.add(rid)
        ls = lines_in(r['qfile'], r['stem_regions'])
        tag = f'{st} {mat} material'
    else:
        ls = lines_in(r['qfile'], r['regions'])
        tag = f'{st} {kind}'
        txt = ' '.join(x[2] for x in ls)
        # option checks
        opts = {k: len(re.findall(k + r'\s*[\.．、:：]', txt)) for k in 'ABCD'}
        nums = re.findall(r'(?:^|\s)(\d{2,3})\s*[\.．、]', txt)
        lead = [x[2] for x in ls if re.match(r'^\s*\d{1,3}\s*[\.．、]', x[2])]
        if any(v != 1 for v in opts.values()):
            print('OPTS', tag, rid, opts)
        if len(lead) > 1:
            print('MULTI-NUM', tag, rid, lead)
    for p, top, t in ls:
        if SUS.search(t):
            print('SUS', tag, rid, f'p{p}@{top}', t[:90])
print('checked', len(order))
