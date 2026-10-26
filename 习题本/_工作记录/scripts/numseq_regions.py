"""Number series put fractions/radicals in as formula images centred on the text line, so the numerator half
sits above the line box: the split gave it to the previous question (its crop shows stray numerators at the
bottom, this one loses them). Extend each 数量关系 question's top to the formula images on its first line and cut
the previous question's region just above. Writes cropfix/spec_numseq.json for fix_crops.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import page_lines, doc_offset
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

if __name__ == '__main__':
    raw = json.load(open(S + '/db/real_raw.json'))
    by_paper = {}
    for r in raw:
        if r.get('section') == '数量关系' and r['kind'] in ('数字推理', '数学运算') and r.get('regions'):
            by_paper.setdefault(r['paper'], []).append(r)
    spec = {}
    for paper, rs in by_paper.items():
        if not any(r['kind'] == '数字推理' for r in rs): continue
        rs.sort(key=lambda r: r['num'])
        for prev, cur in zip(rs, rs[1:]):
            if cur['num'] != prev['num'] + 1: continue
            pk = min(cur['regions'], key=int); top, bot = cur['regions'][pk]
            pl = page_lines(cur['qfile'], int(pk))
            first = min((L for L in pl['lines'] if L['top'] >= top - 1), key=lambda L: L['top'], default=None)
            if not first: continue
            imgs = [im for im in pl['images'] if im['top'] < first['top'] and im['bottom'] > first['top'] + 2 and im['top'] > first['top'] - 30]
            if not imgs: continue
            new_top = round(min(im['top'] for im in imgs) - 1.0, 1)
            if new_top >= top - 0.5: continue
            spec.setdefault(cur['id'], {'regions': dict(cur['regions'])})['regions'][pk] = [new_top, bot]
            if pk in prev['regions'] and prev['regions'][pk][1] > new_top - 0.5:
                pt, pb = (spec.get(prev['id']) or {'regions': dict(prev['regions'])})['regions'][pk]
                spec.setdefault(prev['id'], {'regions': dict(prev['regions'])})['regions'][pk] = [pt, round(new_top - 0.5, 1)]
    json.dump(spec, open(S + '/cropfix/spec_numseq.json', 'w'), ensure_ascii=False, indent=1)
    print('questions to re-crop:', len(spec))
