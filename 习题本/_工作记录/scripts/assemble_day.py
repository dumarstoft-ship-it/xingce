"""Assemble one day's workbook JSON from blueprints + generated variants + real-question DB, then render PDF."""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
CR = S + '/crops/real2'
PART_TITLE = {'ns': '数字推理', 'math': '数学运算', 'logic': '逻辑判断', 'zh': '综合推理'}
TIME_MIN = {'ns': 10, 'math': 60, 'logic': 20, 'zh': 10}
NS_PLAN = S + '/db/ns_plan.json'  # 数字推理 (number series): real questions, reused in rotation when they run out
ZL_PLAN = S + '/db/zl_plan.json'  # 资料分析: two sets a day, questions printed in the separate booklet (scripts/zl_render.py)
ZL_FIX = S + '/db/zl_fixes.json'  # answers / 解析 for 资料 questions whose 解析 file lacks them

def zl_note(items):
    from render_day import zl_kind
    kind = zl_kind(items)
    note = f'资料分析每天两套，题目在单独的打印册里，都是按篇挑出的高难度{kind}'
    return note + ('。' if kind == '真题' else '（模考题没有官方答案，答案和解析由两人分别独立求解、核对一致后写成）。')

def zl_part(day):
    plan = json.load(open(ZL_PLAN)).get(str(day)) if os.path.exists(ZL_PLAN) else None
    if not plan: return None
    raw = json.load(open(S + '/db/zl_raw.json'))
    fix = json.load(open(ZL_FIX)) if os.path.exists(ZL_FIX) else {}
    by = {}
    for r in raw: by.setdefault(r['mat'], []).append(r)
    items = []
    for st in plan:
        k = 0
        for m in st['mats']:
            for r in sorted(by[m], key=lambda r: r['pos']):
                k += 1
                f = fix.get(r['id']) or {}
                ans = f['answer'] if f.get('override') else (r['answer_official'] or f.get('answer'))  # override: the official key is misprinted
                it = {'type': 'real', 'id': r['id'], 'src_label': f"{r['paper_name']} 第{r['num']}题", 'answer': ans,
                      'set': st['set'], 'zl_no': k, 'mock': r['paper'].startswith('MK')}
                jp = f"{S}/crops/zl/{r['id']}_j.png"
                if f.get('jiexi'): it['jiexi_text'] = f['jiexi']
                elif os.path.exists(jp): it['jiexi_img'] = jp
                else: it['jiexi_text'] = r.get('jiexi_raw') or '（本题无解析）'
                if f.get('extra'): it['extra'] = f['extra']
                if (f.get('source') or '').startswith('自解'):
                    it['src_label'] += '（无官方答案，答案与解析为自解）'
                items.append(it)
    sets = '、'.join(f"第 {st['set']} 套" for st in plan)
    return {'title': '资料分析', 'module': f'打印册{sets}', 'time_min': 30 * len(plan), 'print_only': True, 'items': items,
            'note': f'今天的资料分析在打印册{sets}（每套 4 篇 20 题），按考场节奏整套做完再对答案；答案和解析在本册最后。'}

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
NO_JIEXI_PAPERS = ('2026GZ', '2026CQ', '2026HB')  # originals print only the answer (or nothing): 解析 is written by us
REALONLY = S + '/db/realonly_plan.json'             # logic / 综合推理 use real questions only (user decision)

PLACEHOLDER = re.compile(r'待定|无法判断|题目缺失')
def clean_tag(v):
    """classifier tags shown in the 解析 header: drop placeholders ("待定") and notes about the crop ("多项为公式图片")"""
    if not v: return v
    v = re.sub(r'[（(][^()（）]*公式图片[)）]', '', v).strip()
    return None if not v or PLACEHOLDER.search(v) else v

def src_label(r):
    return f"{r['paper_name']} 第{r['num']}题"

def real_item(qid, db, fix, cls):
    r = db[qid]
    f = fix.get(qid) or {}
    ans = r['answer_official'] or f.get('answer')
    official = bool(r['answer_official']) or (f.get('source', '').startswith('官方'))
    it = {'type': 'real', 'id': qid, 'src_label': src_label(r), 'q_img': f'{CR}_nonum/{qid}_q.png' if os.path.exists(f'{CR}_nonum/{qid}_q.png') else f'{CR}/{qid}_q.png', 'answer': ans,
          'kaofa': clean_tag((cls.get(qid) or {}).get('kaofa')), 'technique': clean_tag((cls.get(qid) or {}).get('technique'))}
    if os.path.exists(f'{CR}/{qid}_s.png'):
        it['stem_img'] = f'{CR}_nonum/{qid}_s.png' if os.path.exists(f'{CR}_nonum/{qid}_s.png') else f'{CR}/{qid}_s.png'
        it['stem_key'] = f"{r['paper']}|{(r.get('stem_text') or '').strip()[:40]}"  # 一拖n: print the material once
    jp = f'{CR}/{qid}_j.png'
    if r['paper'] in NO_JIEXI_PAPERS:
        if r['answer_official'] and f.get('answer') and f['answer'] != r['answer_official']:
            print('WARNING answer mismatch', qid, 'paper', r['answer_official'], 'self', f['answer'])
        it['jiexi_text'] = f.get('jiexi') or '（本题无解析）'
        it['src_label'] += '（原卷只附答案，解析为本册补写）' if r['answer_official'] else '（无官方答案，答案与解析为自解）'
        official = True  # label already set
    elif official and os.path.exists(jp):
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
    if ov.get('answer'): it['answer'] = ov['answer']  # the paper's printed key is wrong (its own 解析 says otherwise)
    return it

def load_cls():
    cls = {}
    for f in sorted(glob.glob(S + '/cls/out_*.jsonl')) + sorted(glob.glob(S + '/cls2/out_*.jsonl')):  # cls2: papers added later
        for l in open(f):
            l = l.strip()
            if l:
                d = json.loads(l); cls[d['id']] = d
    return cls

HARDEN = S + '/db/math_harden.json'  # per-day "去水" decisions: easy questions removed, harder real questions added
_TBANK = None
def teacher_bank():
    """Questions from the teacher's notes (忧郁牛牛 数量关系笔记), cleaned and verified: teacher/bank_B*.json."""
    global _TBANK
    if _TBANK is None:
        _TBANK = {b['tid']: b for f in sorted(glob.glob(S + '/teacher/bank_B*.json')) for b in json.load(open(f))}
    return _TBANK

def teacher_item(tid):
    b = teacher_bank()[tid]
    src = b.get('source')
    jx = b['jiexi'] + ('（原题没有选项，选项为本册补设。）' if b.get('options_added') else '')
    fig = (b.get('figure') or {}).get('svg') if isinstance(b.get('figure'), dict) else None
    return {'type': 'teacher', 'tid': tid, 'src_label': f'老师笔记精选 · {src}' if src else '老师笔记精选', 'stem': b['stem'], 'options': b['options'],
            'answer': b['answer'], 'jiexi': jx, 'kaofa': b.get('kaofa'), 'technique': b.get('method'), 'figure': fig}

def part_items(day, part, module, db, fix, cls):
    bp_key = 'C' if part == 'zh' else module
    bp = json.load(open(f'{S}/blueprints/{bp_key}.json'))
    dayplan = next(d for d in bp['days'] if d['day'] == day)
    hd = (json.load(open(HARDEN)).get(str(day)) if part == 'math' and os.path.exists(HARDEN) else None) or {}
    removed = {r['key'] for r in hd.get('remove', [])}
    added = {}
    for a in hd.get('add_real', []) + hd.get('add_teacher', []):
        added.setdefault(a['group'], []).append(a)
    variants = []
    for f in sorted(glob.glob(f'{S}/gen/D{day:02d}_{part}_*.json')):
        variants += json.load(open(f))
    review = {}
    for f in glob.glob(f'{S}/review/D{day:02d}_{part}_review*.json'):
        for it in json.load(open(f)).get('items', []):
            review[it['vid']] = it
    by_group = {}
    for v in variants:
        if review.get(v['vid'], {}).get('verdict') == 'drop' or v['vid'] in removed: continue
        by_group.setdefault(v.get('group'), []).append(v)
    items = []
    titles = [g['title'] for g in dayplan['groups']]
    for gname in list(added):
        if gname not in titles:  # unknown group title: append to the last group
            added.setdefault(titles[-1], []).extend(added.pop(gname))
    for g in dayplan['groups']:
        for qid in g['real']:
            if qid in removed: continue
            it = real_item(qid, db, fix, cls); it['group'] = g['title']; items.append(it)
        for a in added.get(g['title'], []):
            if a.get('tid'):
                it = teacher_item(a['tid'])
            else:
                it = real_item(a['id'], db, fix, cls)
                if a.get('jiexi_note'):
                    if not it.get('jiexi_img') and len(a['jiexi_note']) > 60:  # no official 解析: the reviewer's full 解析
                        it['jiexi_text'] = a['jiexi_note']
                    else:
                        it['extra'] = ((it.get('extra') or '') + ' 补充：' + a['jiexi_note']).strip()
            it['group'] = g['title']
            items.append(it)
        for v in by_group.pop(g['title'], []):
            items.append({'type': 'variant', 'vid': v['vid'], 'group': g['title'], 'difficulty': v.get('difficulty'), 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'],
                          'jiexi': v['jiexi'] + (f"（参考用时 {v['time_s']} 秒）" if v.get('time_s') and part == 'math' and '参考用时' not in v['jiexi'] and '用时' not in v['jiexi'][-30:] else ''),
                          'kaofa': v.get('kaofa'), 'technique': v.get('technique'), 'figure': v.get('figure_svg'), 'shared_stem_text': v.get('shared_stem')})
    if hd:  # after 去水 the groups mix kept, added and new questions: order each group easy -> hard
        LV = {'基础': 1, '中等': 2, '难': 3, '很难': 4}
        def level(it):
            if it['type'] == 'teacher': return LV.get(teacher_bank()[it['tid']].get('level'), 2)
            if it['type'] == 'real': return (cls.get(it['id']) or {}).get('difficulty') or 2
            return it.get('difficulty') or 2
        order = {g['title']: k for k, g in enumerate(dayplan['groups'])}
        items = sorted(items, key=lambda it: (order.get(it['group'], 99), level(it)))
        if hd.get('order'):  # the reviewer's own sequence for the day; new variants are referenced by position
            flat = []
            for o in hd['order']:
                if isinstance(o, dict) and 'seq' in o: flat += o['seq']
                else: flat.append(o['key'] if isinstance(o, dict) else o)
            pos = {}
            for k, key in enumerate(flat):
                m = re.match(r'(?:NEW-|新改编#|NV)(\d+)$', key)
                m0 = re.match(r'new_variants\[(\d+)\]$', key)
                if m: key = f'D{day:02d}-math-h-v{int(m.group(1)):02d}'
                elif m0: key = f'D{day:02d}-math-h-v{int(m0.group(1)) + 1:02d}'
                pos[key] = k
            items = sorted(items, key=lambda it: pos.get(it.get('id') or it.get('tid') or it.get('vid'), 999))
    for gname, vs in by_group.items():  # variants whose group title didn't match exactly
        for v in vs:
            items.append({'type': 'variant', 'vid': v['vid'], 'group': gname, 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'],
                          'jiexi': v['jiexi'], 'kaofa': v.get('kaofa'), 'technique': v.get('technique'), 'figure': v.get('figure_svg'), 'shared_stem_text': v.get('shared_stem')})
    if hd.get('round1'):  # 30 a day: this week's share of the day's questions (scripts/split_round1.py); the rest wait for the next round
        keep = set(hd['round1'])
        items = [it for it in items if (it.get('id') or it.get('tid') or it.get('vid')) in keep]
    return items

W2_DECISION = S + '/w2/D{:02d}_decision.json'  # week 2 on: the planner's 30 math questions, grouped and ordered

def w2_math_items(day, db, fix, cls):
    p = W2_DECISION.format(day)
    if not os.path.exists(p): return None
    d = json.load(open(p))
    notes, checks = d.get('jiexi_notes') or {}, d.get('answer_checks') or {}
    variants, review = {}, {}
    for f in sorted(glob.glob(f'{S}/gen/D{day:02d}_math_w2*.json')):
        for v in json.load(open(f)): variants[v['vid']] = v
    for f in glob.glob(f'{S}/review/D{day:02d}_math_w2_review*.json'):
        for it in json.load(open(f)).get('items', []): review[it['vid']] = it
    items = []
    for g in d['groups']:
        for e in g['items']:
            if 'real' in e:
                q = e['real']; it = real_item(q, db, fix, cls)
                chk = (checks.get(q) or {}).get('answer')
                if not it['answer']: it['answer'] = chk
                elif chk and chk != it['answer']: print('WARNING planner answer differs', q, it['answer'], chk)
                note = None if (OVR.get(q) or {}).get('jiexi_text') else notes.get(q)  # an override's 解析 already covers it
                if note:
                    if it.get('jiexi_img') or not (it.get('jiexi_text') or '').startswith('（本题无'):
                        it['extra'] = ((it.get('extra') or '') + ('' if note.startswith(('补充', '易错', '注')) else ' 补充：') + note).strip()
                    else:  # no official 解析: the planner's full 解析
                        it['jiexi_text'] = note
            elif 'teacher' in e:
                it = teacher_item(e['teacher'])
                if notes.get(e['teacher']): it['jiexi'] += ' 补充：' + notes[e['teacher']]
            else:
                vid = f"D{day:02d}-math-w2-v{e['variant']:02d}"; v = variants.get(vid)
                if not v or review.get(vid, {}).get('verdict') == 'drop':
                    print('WARNING variant missing or dropped', vid); continue
                it = {'type': 'variant', 'vid': vid, 'difficulty': v.get('difficulty'), 'stem': v['stem'], 'options': v['options'], 'answer': v['answer'],
                      'jiexi': v['jiexi'], 'kaofa': v.get('kaofa'), 'technique': v.get('technique'), 'figure': v.get('figure_svg'), 'shared_stem_text': v.get('shared_stem')}
            it['group'] = g['title']
            items.append(it)
    return items

def realonly_items(day, part, db, fix, cls):
    if not os.path.exists(REALONLY): return None
    ids = json.load(open(REALONLY)).get(str(day), {}).get(part)
    if ids is None: return None
    return [real_item(i, db, fix, cls) for i in ids]

def assemble(day):
    sched = json.load(open(S + '/db/schedule.json'))
    s = sched['schedule'][day - 1]; names = sched['names']
    db, fix = load_db(); cls = load_cls()
    parts = []; missing = []
    ns = (json.load(open(NS_PLAN)).get(str(day)) if os.path.exists(NS_PLAN) else None) or []
    if ns:
        parts.append({'title': PART_TITLE['ns'], 'module': '数列与数阵规律', 'time_min': TIME_MIN['ns'], 'items': [real_item(i, db, fix, cls) for i in ns]})
    for part in ('math', 'logic', 'zh'):
        m = s[part]
        label = names[m].replace('综合推理·', '')
        if part in ('logic', 'zh'):
            items = realonly_items(day, part, db, fix, cls)
            if items is not None:
                if items:
                    mods = list(dict.fromkeys((cls.get(it['id']) or {}).get('module') for it in items))  # the modules actually used
                    if mods and None not in mods and mods != [m]:
                        label = ' + '.join(names[x].replace('综合推理·', '') for x in mods)
                    parts.append({'title': PART_TITLE[part], 'module': label, 'time_min': TIME_MIN[part], 'items': items})
                else:
                    missing.append(PART_TITLE[part])
                continue
        if part == 'math':
            items = w2_math_items(day, db, fix, cls)
            if items is not None:
                parts.append({'title': PART_TITLE[part], 'module': label, 'time_min': TIME_MIN[part], 'items': items})
                continue
        bp_key = 'C' if part == 'zh' else m
        if not os.path.exists(f'{S}/blueprints/{bp_key}.json') or not glob.glob(f'{S}/gen/D{day:02d}_{part}_*.json'):
            print('skip part (not ready):', part, m); missing.append(PART_TITLE[part]); continue
        parts.append({'title': PART_TITLE[part], 'module': label, 'time_min': TIME_MIN[part], 'items': part_items(day, part, m, db, fix, cls)})
    zl = zl_part(day)
    if zl: parts.append(zl)
    note = ('题目页只有题号，不标题型、考法和出处，请自己判断。数字推理用历年真题，题不够时轮换重做。数学运算由历年真题（直接截取原卷）、老师笔记精选和依据真题考法改编、经程序验算的新题组成，送分题已去掉，每道题都有一个要想清楚的地方；'
            '逻辑判断和综合推理全部是真题。' + (zl_note(zl['items']) if zl else '')
            + '每道题的出处都写在本册最后的解析里，多数题还注明了考法和技巧。建议严格计时，做完再对答案。')
    if missing:
        note += '今天的' + '、'.join(missing) + '真题暂缺，等补充新卷子后补发。'
    for pt in parts:  # last pass over the student-facing text: no internal ids, no doubled labels
        for it in pt['items']:
            for f in ('extra', 'jiexi', 'jiexi_text'):
                if isinstance(it.get(f), str):
                    t = re.sub(r'(老师笔记)\s*T\d{3}(?:x\d+)?', r'\1', it[f])
                    it[f] = re.sub(r'补充[：:]\s*补充[：:]?', '补充：', t)
    return {'day': day, 'subtitle': '广东省考 42 天专项训练 · 数量关系 + 判断推理' + (' + 资料分析' if zl else ''), 'note': note, 'parts': parts}

if __name__ == '__main__':
    from render_day import render_day, to_pdf
    day = int(sys.argv[1]); out = sys.argv[2]
    d = assemble(day)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(d, open(out[:-4] + '.json', 'w'), ensure_ascii=False, indent=1)
    hp = out[:-4] + '.html'
    render_day(d, hp); to_pdf(hp, out)
    from shrink_pdf import shrink  # crops are embedded as RGB by Chromium: re-encode as 4-bit gray
    shrink(out, out + '.tmp'); os.replace(out + '.tmp', out)
    print('ok', out, [len(p['items']) for p in d['parts']])
