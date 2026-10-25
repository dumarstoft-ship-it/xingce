"""Re-crop every question / 解析 / material crop that comes from a PDF with a line-box offset (db/doc_offsets.json),
then redo the follow-up steps (number masking, display scale) for those crops."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop, doc_offset
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def main():
    raw = json.load(open(S + '/db/real_raw.json'))
    fix = json.load(open(S + '/db/answer_fixes.json'))
    done_q, n = [], 0
    for r in raw:
        if r['kind'] not in ('数学运算', '逻辑'): continue
        i = r['id']
        if doc_offset(r['qfile']):
            crop(r['qfile'], r['regions'], f'{S}/crops/real2/{i}_q.png'); done_q.append(i); n += 1
            if r.get('stem_regions'): crop(r['qfile'], r['stem_regions'], f'{S}/crops/real2/{i}_s.png'); n += 1
        if r.get('jfile') and doc_offset(r['jfile']):
            regs = (fix.get(i) or {}).get('jiexi_regions') or r['jiexi_regions']
            if regs: crop(r['jfile'], regs, f'{S}/crops/real2/{i}_j.png'); n += 1
    json.dump(done_q, open(S + '/db/recrop_offset_q.json', 'w'))
    print('recropped', n, 'q crops', len(done_q))

if __name__ == '__main__':
    main()
