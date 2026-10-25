import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/crops/real2'
os.makedirs(OUT, exist_ok=True)
db = json.load(open(S + '/db/real_raw.json'))
n = 0
for r in db:
    if r['kind'] not in ('数学运算', '逻辑'): continue
    qp = f"{OUT}/{r['id']}_q.png"; jp = f"{OUT}/{r['id']}_j.png"; sp = f"{OUT}/{r['id']}_s.png"
    try:
        if not os.path.exists(qp) and r['regions']: crop(r['qfile'], r['regions'], qp)
        if not os.path.exists(sp) and r.get('stem_regions'): crop(r['qfile'], r['stem_regions'], sp)
        if not os.path.exists(jp) and r.get('jiexi_regions'): crop(r['jfile'], r['jiexi_regions'], jp)
    except Exception as e:
        print('ERR', r['id'], e)
    n += 1
    if n % 100 == 0: print(n, flush=True)
print('done', n)
