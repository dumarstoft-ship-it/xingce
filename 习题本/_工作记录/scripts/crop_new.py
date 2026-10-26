"""Crops for the papers added on 2026-10-26: question, shared-material and 解析 crops for 数学运算 / 数字推理 / 逻辑,
then the question-number mask (no shift for number series) and display scale."""
import json, os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop
import mask_qnum
from rescale_crops import rescale_one
from glyph_size import font_pt
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/crops/real2'
KINDS = ('数学运算', '数字推理', '逻辑')

if __name__ == '__main__':
    new_ids = {r['id'] for r in json.load(open(S + '/db/real_raw_new.json'))}
    db = [r for r in json.load(open(S + '/db/real_raw.json')) if r['id'] in new_ids and r['kind'] in KINDS]
    ov = json.load(open(S + '/db/overrides.json'))
    n = 0
    for r in db:
        i = r['id']; qp, jp, sp = f'{OUT}/{i}_q.png', f'{OUT}/{i}_j.png', f'{OUT}/{i}_s.png'
        try:
            if r['regions'] and not os.path.exists(qp): crop(r['qfile'], r['regions'], qp)
            if r.get('stem_regions') and not os.path.exists(sp): crop(r['qfile'], r['stem_regions'], sp)
            if r.get('jiexi_regions') and not os.path.exists(jp): crop(r['jfile'], r['jiexi_regions'], jp)
        except Exception as e:
            print('ERR', i, repr(e)[:100]); continue
        if os.path.exists(qp):
            res = mask_qnum.mask(i, r.get('text'), shift=(r['kind'] != '数字推理'))
            if res != 'ok':
                shutil.copy(qp, f'{OUT}_nonum/{i}_q.png'); shutil.copy(qp + '.json', f'{OUT}_nonum/{i}_q.png.json')
                r['_mask'] = res
            if r['kind'] == '数字推理':
                f = font_pt(f'{OUT}_nonum/{i}_q.png')
                if f: ov.setdefault(i, {})['q_scale'] = round(max(0.8, min(1.3, 10.5 / f)), 3)
        if os.path.exists(sp): mask_qnum.mask_stem_header(i, r.get('stem_text'))
        n += 1
        if n % 100 == 0: print(n, flush=True)
    json.dump(ov, open(S + '/db/overrides.json', 'w'), ensure_ascii=False, indent=1)
    import rescale_crops; rescale_crops._OV = None
    for r in db:
        for d in (OUT, OUT + '_nonum'):
            for k in 'qsj':
                p = f"{d}/{r['id']}_{k}.png"
                if os.path.exists(p): rescale_one(p)
    print('done', n, 'mask failures:', sum(1 for r in db if r.get('_mask')))
