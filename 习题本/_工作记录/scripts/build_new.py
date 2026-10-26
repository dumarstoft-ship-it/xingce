"""Build records for the papers added on 2026-10-26 (papers_new.py) into db/real_raw_new.json, without touching
db/real_raw.json; merge_new.py dedupes them against the existing bank and appends."""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answers as A
from build_db import build_paper
from papers_new import PAPERS_NEW
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

if __name__ == '__main__':
    only = set(sys.argv[1:])
    out = []
    for code, disp, qf, jf in PAPERS_NEW:
        if only and code not in only: continue
        A.LINES = {}; A.STARTS = []
        try:
            recs, st = build_paper(code, disp, qf, jf)
        except Exception as e:
            print(code.ljust(8), 'ERROR', repr(e)[:120]); continue
        out.extend(recs)
        c = Counter(r['kind'] for r in recs)
        na = sum(1 for r in recs if r['kind'] in ('数学运算', '数字推理', '逻辑') and r['answer_official'] is None)
        nj = sum(1 for r in recs if r['kind'] in ('数学运算', '数字推理', '逻辑') and not r.get('jiexi_regions'))
        print(code.ljust(8), st, dict(c), 'noans', na, 'nojiexi', nj, flush=True)
    json.dump(out, open(S + '/db/real_raw_new.json', 'w'), ensure_ascii=False, indent=0)
    print('TOTAL', len(out), Counter(r['kind'] for r in out))
