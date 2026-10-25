"""Cut inline 【答案】 lines out of question regions (2026CQ / 2026GZ papers print the answer under each question), then re-crop."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop import crop
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
PAT = re.compile(r'[【\[]\s*答\s*案\s*[】\]]')

def main():
    raw = json.load(open(S + '/db/real_raw.json'))
    ov = json.load(open(S + '/db/overrides.json'))
    lines_cache = {}
    fixed = []
    for r in raw:
        if not PAT.search(r.get('text') or ''): continue
        if r['qfile'] not in lines_cache:
            lines_cache[r['qfile']] = {pg['page']: pg for pg in json.load(open(f"{S}/lines/{r['qfile']}.json"))['pages']}
        pages = lines_cache[r['qfile']]
        for pk in sorted(r['regions'], key=int):
            t, b = r['regions'][pk]
            hit = [L for L in pages[int(pk)]['lines'] if PAT.search(L['text']) and t <= L['top'] <= b]
            if hit:
                r['regions'][pk] = [t, round(hit[0]['top'] - 0.5, 1)]
                for later in [k for k in r['regions'] if int(k) > int(pk)]: del r['regions'][later]
                r['text'] = PAT.split(r['text'])[0].rstrip()
                ov.setdefault(r['id'], {})['cut_before_re'] = PAT.pattern
                fixed.append(r['id'])
                break
    json.dump(raw, open(S + '/db/real_raw.json', 'w'), ensure_ascii=False)
    json.dump(ov, open(S + '/db/overrides.json', 'w'), ensure_ascii=False, indent=1)
    by = {r['id']: r for r in raw}
    for i in fixed:
        r = by[i]
        crop(r['qfile'], r['regions'], f'{S}/crops/real2/{i}_q.png')
    print('fixed', len(fixed), fixed)

if __name__ == '__main__':
    main()
