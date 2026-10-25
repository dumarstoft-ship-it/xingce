# OCR fallback: read answer letter from 解析 crop images when text extraction found none
import json, os, re, sys
os.environ.setdefault('ORT_THREADS', '2')
from rapidocr_onnxruntime import RapidOCR
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
db = json.load(open(S + '/db/real_raw.json'))
eng = RapidOCR()
pat = [re.compile(r'正确答案\s*(?:为|是)?\s*[：:]?\s*([A-D])'), re.compile(r'答案\s*(?:为|是)\s*([A-D])'), re.compile(r'选择?\s*([A-D])\s*选?项'), re.compile(r'【\s*答案\s*】\s*([A-D])')]
out = {}
for r in db:
    if r['kind'] not in ('数学运算', '逻辑') or r['answer_official']: continue
    jp = f"{S}/crops/real2/{r['id']}_j.png"
    if not os.path.exists(jp): continue
    res, _ = eng(jp)
    txt = '\n'.join(t for _, t, _ in (res or []))
    ans = None
    for pt in pat:
        ms = pt.findall(txt)
        if ms: ans = ms[-1]; break
    out[r['id']] = {'answer': ans, 'ocr_tail': txt[-120:]}
    print(r['id'], ans, flush=True)
json.dump(out, open(S + '/db/ocr_answers.json', 'w'), ensure_ascii=False, indent=1)
print('done', len(out), sum(1 for v in out.values() if v['answer']))
