import json, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/scripts')
from crop import crop
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
db = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
rc = json.load(open(S + '/db/recrop.json'))
fix = json.load(open(S + '/db/answer_fixes.json'))
n = 0
for i in rc['q']:
    r = db[i]; crop(r['qfile'], r['regions'], f'{S}/crops/real2/{i}_q.png'); n += 1
for i in rc['j']:
    r = db[i]
    regs = (fix.get(i) or {}).get('jiexi_regions') or r['jiexi_regions']
    if regs: crop(r['jfile'], regs, f'{S}/crops/real2/{i}_j.png'); n += 1
print('recropped', n)
# stems
for i, r in db.items():
    if r['kind'] in ('数学运算', '逻辑') and r.get('stem_regions'):
        crop(r['qfile'], r['stem_regions'], f'{S}/crops/real2/{i}_s.png')
print('stems done')
