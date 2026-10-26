"""Per-question / per-material difficulty features for 资料分析, and a ridge model of 粉笔 全站正确率 fitted on the
papers whose 解析 print it (2015–2021). Writes db/zl_difficulty.json (material -> score)."""
import json, re, sys, os, math
import numpy as np
from collections import defaultdict
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
NUM = re.compile(r'(\d+(?:\.\d+)?)')
def options(text):
    t = text.replace('\n', '  ')
    parts = re.split(r'(?:^|\s)([A-D])\s*[\.．、:：]\s*', t)
    opts = {}
    for k in range(1, len(parts) - 1, 2):
        opts[parts[k]] = parts[k + 1].strip()
    return opts
def opt_close(opts):
    vals = []
    for k in 'ABCD':
        v = opts.get(k, '')
        m = NUM.findall(v)
        if len(m) == 1 and len(v) < 18: vals.append(float(m[0]))
        else: return None
    if len(vals) < 4 or max(vals) <= 0: return None
    gaps = [abs(a - b) / max(abs(a), abs(b), 1e-9) for i, a in enumerate(vals) for b in vals[i + 1:]]
    return min(gaps)
TYPES = {
 'zonghe': r'(?:能够|可以|不能|无法)(?:从上述资料中)?推出|说法(?:正确|错误)|正确的是|错误的是|不正确的是|表述(?:正确|错误)',
 'count': r'有几[个项年]|多少个|几个|有[多几]少',
 'chart': r'(?:折线|柱状|示意|饼|条形)?图[中]?.{0,6}(?:能够|最能|准确|正确)?反映|下列(?:哪个|哪幅)?图|示意图',
 'sort': r'排序|从高到低|从大到小|从低到高|从小到大|排列',
 'avg': r'年均|平均每|人均|均值|平均',
 'interval': r'间隔|比20\d\d年(?:同期)?(?:增长|上升|提高|下降)',
 'share': r'比重|占比|所占|份额|占.{0,12}的',
 'pp': r'百分点',
 'base': r'上年|去年|基期|20\d\d年(?:同期)?(?:约)?为',
 'times': r'倍',
 'range': r'之间|范围|以上|以下|不到|超过',
 'growth': r'增长率|增速|增幅|增长了|同比',
 'calc_expr': r'计算式|表示为|关系式',
}
TRE = {k: re.compile(v) for k, v in TYPES.items()}
def qfeat(r, jh):
    t = r['text']; stem = t.split('\n')[0]
    o = options(t)
    oc = opt_close(o)
    f = {
        'jx_len': len(re.sub(r'\s+', '', r.get('jiexi_raw') or '')),
        'jx_h': jh,
        'oc': -math.log10(oc + 1e-3) if oc is not None else 0.0,
        'oc_na': 1.0 if oc is None else 0.0,
        'q_len': len(re.sub(r'\s+', '', t)),
    }
    for k, rx in TRE.items(): f['t_' + k] = 1.0 if rx.search(t if k in ('zonghe', 'chart') else stem) else 0.0
    return f
def jx_height(r):
    return sum(b - a for a, b in (r.get('jiexi_regions') or {}).values())
def matfeat(recs):
    st = recs[0]['stem_text'] or ''
    nums = len(NUM.findall(st))
    h = sum(b - a for a, b in (recs[0].get('stem_regions') or {}).values())
    return {'m_len': len(re.sub(r'\s+', '', st)), 'm_nums': nums, 'm_h': h, 'm_textonly': 1.0 if len(st) > 300 and h < 260 else 0.0}

def build():
    raw = json.load(open(S + '/db/zl_raw.json'))
    by_paper = defaultdict(list)
    for r in raw: by_paper[r['paper']].append(r)
    rows = []
    for paper, rs in by_paper.items():
        jh = [jx_height(r) for r in rs]; jl = [len(re.sub(r'\s+', '', r.get('jiexi_raw') or '')) for r in rs]
        mh, ml = np.median(jh) or 1, np.median(jl) or 1
        mats = defaultdict(list)
        for r in rs: mats[r['mat']].append(r)
        for m, mr in mats.items():
            mf = matfeat(mr)
            for r in mr:
                f = qfeat(r, jx_height(r))
                f['jx_h_rel'] = f['jx_h'] / mh; f['jx_len_rel'] = f['jx_len'] / ml
                f.update(mf)
                rows.append((r, f))
    return rows

if __name__ == '__main__':
    rows = build()
    keys = sorted(rows[0][1])
    X = np.array([[f[k] for k in keys] for _, f in rows]); y = np.array([r.get('acc') if r.get('acc') is not None else np.nan for r, _ in rows])
    papers = np.array([r['paper'] for r, _ in rows]); mats = np.array([r['mat'] for r, _ in rows])
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = (X - mu) / sd
    lab = ~np.isnan(y)
    def fit(Zt, yt, lam=8.0):
        A = np.hstack([Zt, np.ones((len(Zt), 1))])
        I = np.eye(A.shape[1]); I[-1, -1] = 0
        return np.linalg.solve(A.T @ A + lam * I, A.T @ yt)
    def pred(w, Zt): return np.hstack([Zt, np.ones((len(Zt), 1))]) @ w
    def rank(a): return np.argsort(np.argsort(a)).astype(float)
    def spear(a, b): return float(np.corrcoef(rank(a), rank(b))[0, 1])
    cvp = np.full(len(y), np.nan)
    for pp in sorted(set(papers[lab])):
        tr = lab & (papers != pp); te = lab & (papers == pp)
        w = fit(Z[tr], y[tr]); cvp[te] = pred(w, Z[te])
    print('question-level CV spearman', round(spear(cvp[lab], y[lab]), 3), 'n', lab.sum())
    # material level
    M = defaultdict(list)
    for i in np.where(lab)[0]: M[mats[i]].append(i)
    ma = np.array([np.mean(y[v]) for v in M.values()]); mp = np.array([np.mean(cvp[v]) for v in M.values()])
    print('material-level CV spearman', round(spear(mp, ma), 3), 'n', len(M))
    w = fit(Z[lab], y[lab])
    for k, c in sorted(zip(keys, w[:-1]), key=lambda x: x[1]): print('  ', k.ljust(12), round(c, 2))
    allp = pred(w, Z)
    out = defaultdict(lambda: {'pred': [], 'acc': []})
    for i, (r, f) in enumerate(rows):
        out[r['mat']]['pred'].append(float(allp[i]))
        if r.get('acc') is not None: out[r['mat']]['acc'].append(r['acc'])
    res = {}
    for m, v in out.items():
        res[m] = {'pred': round(float(np.mean(v['pred'])), 1), 'acc': round(float(np.mean(v['acc'])), 1) if len(v['acc']) == len(v['pred']) else None}
    json.dump(res, open(S + '/db/zl_difficulty.json', 'w'), ensure_ascii=False, indent=0)
