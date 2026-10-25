"""Apply hand-trimmed regions for a few crops: record them in db/overrides.json and db/real_raw.json, re-crop,
then redo the post-processing for just those crops (JS highlight, question-number mask, stem header, rescale).
Usage: python3 fix_crops.py spec.json   with spec = {id: {"regions"|"jiexi_regions"|"stem_regions": {page: [top, bottom]},
"j_full_width": bool}} (points, line-box coordinates as in real_raw.json)."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop
import mask_qnum
from fix_js_highlight import clean as clean_js
from rescale_crops import rescale_one
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
CR = S + '/crops/real2'

def main(spec):
    ovp, rawp, fixp = S + '/db/overrides.json', S + '/db/real_raw.json', S + '/db/answer_fixes.json'
    ov, raw, fix = json.load(open(ovp)), json.load(open(rawp)), json.load(open(fixp))
    by = {r['id']: r for r in raw}
    for qid, o in spec.items():
        r = by[qid]
        ov.setdefault(qid, {}).update(o)
        if 'regions' in o:
            r['regions'] = o['regions']
            out = f'{CR}/{qid}_q.png'
            crop(r['qfile'], o['regions'], out)
            if qid.startswith('2026JS'): clean_js(out)
            res = mask_qnum.mask(qid, r.get('text'))
            if res != 'ok':  # no number to mask: the plain crop must replace any stale masked copy
                shutil.copy(out, f'{CR}_nonum/{qid}_q.png')
                if os.path.exists(out + '.json'): shutil.copy(out + '.json', f'{CR}_nonum/{qid}_q.png.json')
            for p in (out, f'{CR}_nonum/{qid}_q.png'): rescale_one(p)
            print(qid, 'q', res)
        if 'stem_regions' in o:
            r['stem_regions'] = o['stem_regions']
            out = f'{CR}/{qid}_s.png'
            crop(r['qfile'], o['stem_regions'], out)
            res = mask_qnum.mask_stem_header(qid, r.get('stem_text'))
            if res != 'ok' and os.path.exists(f'{CR}_nonum/{qid}_s.png'):
                shutil.copy(out, f'{CR}_nonum/{qid}_s.png')
                if os.path.exists(out + '.json'): shutil.copy(out + '.json', f'{CR}_nonum/{qid}_s.png.json')
            for p in (out, f'{CR}_nonum/{qid}_s.png'):
                if os.path.exists(p): rescale_one(p)
            print(qid, 's', res)
        if 'jiexi_regions' in o:
            r['jiexi_regions'] = o['jiexi_regions']
            if (fix.get(qid) or {}).get('jiexi_regions'): fix[qid]['jiexi_regions'] = o['jiexi_regions']
            out = f'{CR}/{qid}_j.png'
            crop(r['jfile'], o['jiexi_regions'], out, full_width=bool(o.get('j_full_width') or ov[qid].get('j_full_width')))
            rescale_one(out)
            print(qid, 'j')
    json.dump(ov, open(ovp, 'w'), ensure_ascii=False, indent=1)
    json.dump(raw, open(rawp, 'w'), ensure_ascii=False)
    json.dump(fix, open(fixp, 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(json.load(open(sys.argv[1])))
