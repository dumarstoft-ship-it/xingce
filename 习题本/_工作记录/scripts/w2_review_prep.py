"""Blind review of week-2 math variants (briefs/review.md).
  prep <tag> <day>...  writes review/w2_<tag>_questions.json (stem + options only) and review/w2_<tag>_key.json
                       (answer, 解析, verify script) for the variants in gen/D{dd}_math_w2.json of those days
  split <tag>          copies the reviewer's verdicts (review/w2_<tag>_review.json) to review/D{dd}_math_w2_review.json,
                       which assemble_day.py reads (verdict 'drop' leaves the variant out)"""
import json, os, sys, glob
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def prep(tag, days):
    qs, ks = [], []
    for day in days:
        for f in sorted(glob.glob(f'{S}/gen/D{day:02d}_math_w2*.json')):
            for v in json.load(open(f)):
                qs.append({'vid': v['vid'], 'group': v.get('group'), 'stem': v['stem'], 'options': v['options'], 'figure_svg': v.get('figure_svg')})
                ks.append({k: v.get(k) for k in ('vid', 'group', 'kaofa', 'technique', 'difficulty', 'answer', 'jiexi', 'verify', 'verify_script', 'distractors')})
    json.dump(qs, open(f'{S}/review/w2_{tag}_questions.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(ks, open(f'{S}/review/w2_{tag}_key.json', 'w'), ensure_ascii=False, indent=1)
    print(tag, len(qs), 'variants')

def split(tag):
    rv = json.load(open(f'{S}/review/w2_{tag}_review.json'))
    by = {}
    for it in rv['items']:
        by.setdefault(it['vid'][:3], []).append(it)
    for d, items in by.items():
        p = f'{S}/review/{d}_math_w2_review.json'
        old = json.load(open(p))['items'] if os.path.exists(p) else []
        keep = {it['vid']: it for it in old}
        keep.update({it['vid']: it for it in items})
        json.dump({'items': list(keep.values()), 'overall': rv.get('overall')}, open(p, 'w'), ensure_ascii=False, indent=1)
        print(p, [(it['vid'], it['verdict']) for it in items])

if __name__ == '__main__':
    if sys.argv[1] == 'prep': prep(sys.argv[2], [int(x) for x in sys.argv[3:]])
    else: split(sys.argv[2])
