"""Assemble one day's workbook JSON from blueprints + generated variants + real-question DB, then render PDF."""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
CR = S + '/crops/real2'
PART_TITLE = {'math': '数学运算', 'logic': '逻辑判断', 'zh': '综合推理'}
TIME_MIN = {'math': 90, 'logic': 45, 'zh': 30}

def load_db():
    db = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    fix = json.load(open(S + '/db/answer_fixes.json')) if os.path.exists(S + '/db/answer_fixes.json') else {}
    # self-solved answers noted in blueprints (short note), overridden by generation agents' full 解析 below
    for f in sorted(glob.glob(S + '/blueprints/*.json')):
        for e in json.load(open(f)).get('self_solved') or []:
            if e.get('id') and e.get('answer') and e['id'] not in fix:
                fix[e['id']] = {'answer': e['answer'], 'source': '自解', 'jiexi': e.get('jiexi') or e.get('note')}
    # self-solved real questions written by generation agents
    for f in sorted(glob.glob(S + '/gen/real_*.json')):
        for e in json.load(open(f)):
            if e.get('id') and e.get('answer'):
                fix[e['id']] = {'answer': e['answer'], 'source': '自解', 'jiexi': e.get('jiexi')}
    return db, fix

OVR = json.load(open(S + '/db/real_overrides.json')) if os.path.exists(S + '/db/real_overrides.json') else {}

def src_label(r):
    return f"{r['paper_name']} 第{r['num']}题"

def real_item(qid, db, fix, cls):
    r = db[qid]
    f = fix.get(qid) or {}
    ans = r['answer_official'] or f.get('answer')
    official = bool(r['answer_official']) or (f.get('source', '').startswith('官方'))
    it = {'type': 'real', 'id': qid, 'src_label': src_label(r), 'q_img': f'{CR}_nonum/{qid}_q.png' if os.path.exists(f'{CR}_nonum/{qid}_q.png') else f'{CR}/{qid}_q.png', 'answer': ans,
          'kaofa': (cls.get(qid) or {}).get('kaofa'), 'technique': (cls.get(qid) or {}).get('technique')}
    if os.path.exists(f'{CR}/{qid}_s.png'): it['stem_img'] = f'{CR}/{qid}_s.png'
    jp = f'{CR}/{qid}_j.png'
    if official and os.path.exists(jp):
        it['jiexi_img'] = jp
    elif official and r.get('jiexi_raw'):
        it['jiexi_text'] = r['jiexi_raw']
    else:
        it['jiexi_text'] = f.get('jiexi') or '（本题无官方解析）'
    if not official: it['src_label'] += '（无官方答案，答案与解析为自解）'
    ov = OVR.get(qid) or {}
    if ov.get('stem'):  # retyped stem (e.g. masked text in the original paper)
        it['stem'], it['options'] = ov['stem'], ov['options']
    if ov.get('jiexi_text'):
        it.pop('jiexi_img', None); it['jiexi_text'] = ov['jiexi_text']
    if ov.get('extra'): it['extra'] = ov['extra']
    return it

def load_cls():
    cls = {}
    for f in glob.glob(S + '/cls/out_*.jsonl'):
        for l in open(f):
            l = l.strip()
            if l:
                d = json.loads(l); cls[d['id']] = d
    return cls

def part_items(day, part, module, db, fix, cls):
    bp_key = 'C' if part == 'zh' else module
    bp = json.load(open(f'{S}/blueprints/{bp_key}.json'))
    dayplan = next(d for d in bp['days'] if d['day'] == day)
    variants = []
    for f in sorted(glob.glob(f'{S}/gen/D{day:02d}_{part}_*.json')):
        variants += json.load(open(f))
    review = {}
    for f in glob.glob(f'{S}/review/D{day:02d}_{part}_review*.json'):
        for it in json.load(open(f)).get('items', []):
            review[it['vid']] = it
    by_group = {}
    for v in variants:
        if review.get(v['vid'], {}).get('verdict') == 'drop': continue
        by_group.setdefault(v.get('group'), []).append(v)
    items = []
    for g in dayplan['groups']:
        for qid in g['real']:
            it = real_item(qid, db, fix, cls); it['group'] = g['title']; items.append(it)
        for v in by_group.pop(g['title'], []):
            items.append({'type': 'variant', 'vid': v['vid'], 'group': g['title'], 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'],
                          'jiexi': v['jiexi'] + (f"（参考用时 {v['time_s']} 秒）" if v.get('time_s') and part == 'math' and '参考用时' not in v['jiexi'] and '用时' not in v['jiexi'][-30:] else ''),
                          'kaofa': v.get('kaofa'), 'technique': v.get('technique'), 'figure': v.get('figure_svg'), 'shared_stem_text': v.get('shared_stem')})
    for gname, vs in by_group.items():  # variants whose group title didn't match exactly
        for v in vs:
            items.append({'type': 'variant', 'vid': v['vid'], 'group': gname, 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'],
                          'jiexi': v['jiexi'], 'kaofa': v.get('kaofa'), 'technique': v.get('technique'), 'figure': v.get('figure_svg'), 'shared_stem_text': v.get('shared_stem')})
    return items

def assemble(day):
    sched = json.load(open(S + '/db/schedule.json'))
    s = sched['schedule'][day - 1]; names = sched['names']
    db, fix = load_db(); cls = load_cls()
    parts = []
    for part in ('math', 'logic', 'zh'):
        m = s[part]
        bp_key = 'C' if part == 'zh' else m
        if not os.path.exists(f'{S}/blueprints/{bp_key}.json') or not glob.glob(f'{S}/gen/D{day:02d}_{part}_*.json'):
            print('skip part (not ready):', part, m); continue
        parts.append({'title': PART_TITLE[part], 'module': f"{m} {names[m]}", 'time_min': TIME_MIN[part], 'items': part_items(day, part, m, db, fix, cls)})
    note = ('题目页只有题号，不标题型、考法和出处，请自己判断。题目由历年真题（直接截取原卷）和依据真题考法改编的新题组成；'
            '每道题的出处（真题来源与原题号 / 改编）、考法和技巧都写在本册最后的解析里。建议严格计时，做完再对答案。')
    return {'day': day, 'subtitle': '广东省考 42 天专项训练 · 数量关系 + 判断推理', 'note': note, 'parts': parts}

if __name__ == '__main__':
    from render_day import render_day, to_pdf
    day = int(sys.argv[1]); out = sys.argv[2]
    d = assemble(day)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(d, open(out[:-4] + '.json', 'w'), ensure_ascii=False, indent=1)
    hp = out[:-4] + '.html'
    render_day(d, hp); to_pdf(hp, out)
    print('ok', out, [len(p['items']) for p in d['parts']])
