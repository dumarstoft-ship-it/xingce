import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zl_crop as C
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json'))
part, nparts = int(sys.argv[1]), int(sys.argv[2])
papers = sorted({r['paper'] for r in raw})[part::nparts]
for p in papers:
    n = C.build_jiexi([r for r in raw if r['paper'] == p], force=True)
    print(p, n, flush=True)
