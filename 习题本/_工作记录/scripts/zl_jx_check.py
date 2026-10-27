"""OCR each selected 资料 question's 解析 crop: the crop must start at the right question and its answer sentence must
match the answer we print. Writes zl/jx_check.json."""
import json, os, re, sys
from rapidocr_onnxruntime import RapidOCR
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = {r['id']: r for r in json.load(open(S + '/db/zl_raw.json'))}
fix = json.load(open(S + '/db/zl_fixes.json'))
sets = json.load(open(S + '/db/zl_sets.json'))
by = {}
for r in raw.values(): by.setdefault(r['mat'], []).append(r)
ocr = RapidOCR()
out = []
for st in sets:
    for m in st['mats']:
        for r in sorted(by[m], key=lambda r: r['pos']):
            ans = r['answer_official'] or (fix.get(r['id']) or {}).get('answer')
            res, _ = ocr(f"{S}/crops/zl/{r['id']}_j.png")
            txt = '\n'.join(x[1] for x in (res or []))
            found = re.findall(r'(?:正确答案|故选|选择|答案)\s*(?:为|是|选)?\s*[:：]?\s*【?\s*([A-D])', txt)
            nums = [int(x) for x in re.findall(r'(\d{2,3})', txt[:40])]
            out.append({'id': r['id'], 'set': st['set'], 'ans': ans, 'ocr_ans': found[-1] if found else None, 'num_ok': r['num'] in nums,
                        'head': txt[:50], 'tail': txt[-60:]})
            print(r['id'], ans, found[-1] if found else None, r['num'] in nums, flush=True)
json.dump(out, open(S + '/zl/jx_check.json', 'w'), ensure_ascii=False, indent=1)
bad = [e for e in out if not e['num_ok'] or (e['ocr_ans'] and e['ocr_ans'] != e['ans']) or not e['ans']]
print('checked', len(out), 'flagged', len(bad))
for e in bad: print('FLAG', e['id'], e['ans'], e['ocr_ans'], e['num_ok'], e['head'][:30].replace('\n', ' '))
