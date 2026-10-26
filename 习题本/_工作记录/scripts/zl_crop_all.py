import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zl_crop as C
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json'))
papers = sys.argv[1:] or sorted({r['paper'] for r in raw})
MF = S + '/db/zl_meta' + os.environ.get('ZLPART', '') + '.json'
meta = json.load(open(MF)) if os.path.exists(MF) else {}
for code in papers:
    rs = [r for r in raw if r['paper'] == code]
    try:
        m = C.build_print(rs)
    except Exception as e:
        print(code, 'ERR', repr(e)[:150], flush=True); continue
    meta.update(m)
    fails = [(r['id'], r['_mask']) for r in rs if r.get('_mask')]
    for r in rs:
        if r['pos'] == 1: meta[code].setdefault('chunks', {})[r['mat']] = r.get('n_chunks', 0)
    meta[code]['mask_fail'] = fails
    json.dump(meta, open(MF, 'w'), ensure_ascii=False, indent=0)
    print(code, m[code]['scale'], 'mask fails', fails, flush=True)
