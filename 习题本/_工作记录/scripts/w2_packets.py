"""Week-2 math planning packets: for each day 8–14, the module's unused real questions (old + newly classified) and
the teacher's questions, with labelled contact sheets of the question crops. Writes w2/D{dd}_packet.json + sheets."""
import json, glob, os, re, sys
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
CR = S + '/crops/real2'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # labels are ASCII (POOL <id>)

def load_cls():
    cls = {}
    for f in glob.glob(S + '/cls/out_*.jsonl') + glob.glob(S + '/cls2/out_math_new_*.jsonl'):
        for l in open(f):
            l = l.strip()
            if l:
                d = json.loads(l); cls[d['id']] = d
    return cls

def used_ids():
    used = set()
    for d in range(1, 8):
        for pt in json.load(open(f'{S}/out/final/D{d}.json'))['parts']:
            for it in pt['items']:
                used.add(it.get('id') or it.get('tid') or it.get('vid'))
    return used

def sheet(items, path, per_row=1, width=1100):
    """stack question crops with a label bar each"""
    try: font = ImageFont.truetype(FONT, 26)
    except Exception: font = ImageFont.load_default()
    ims = []
    for label, p in items:
        im = Image.open(p).convert('L')
        if im.width > width: im = im.resize((width, int(im.height * width / im.width)))
        bar = Image.new('L', (width, 36), 230); ImageDraw.Draw(bar).text((8, 3), label, fill=0, font=font)
        ims += [bar, im]
    H = sum(i.height for i in ims) + 6 * len(ims)
    c = Image.new('L', (width, H), 255); y = 0
    for i in ims: c.paste(i, (0, y)); y += i.height + 6
    c.save(path)

def main(days):
    cls = load_cls(); used = used_ids()
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    fix = json.load(open(S + '/db/answer_fixes.json'))
    bank = [b for f in sorted(glob.glob(S + '/teacher/bank_B*.json')) for b in json.load(open(f)) if b.get('keep')]
    ex = {e['tid']: e for e in json.load(open(S + '/teacher/examples.json'))}
    sched = json.load(open(S + '/db/schedule.json'))
    for day in days:
        m = sched['schedule'][day - 1]['math']
        cands = []
        for i, c in cls.items():
            if c.get('module') != m or c.get('incomplete') or i in used or i not in raw: continue
            r = raw[i]
            ans = r.get('answer_official') or (fix.get(i) or {}).get('answer') or c.get('answer_check')
            q = f'{CR}_nonum/{i}_q.png' if os.path.exists(f'{CR}_nonum/{i}_q.png') else f'{CR}/{i}_q.png'
            if not os.path.exists(q): continue
            cands.append({'id': i, 'paper': r['paper_name'], 'answer': ans, 'answer_source': 'official' if r.get('answer_official') else ('fix' if fix.get(i) else 'classifier'),
                          'difficulty': c.get('difficulty'), 'kaofa': c.get('kaofa'), 'technique': c.get('technique'), 'point': c.get('point'),
                          'giveaway': c.get('giveaway'), 'note': c.get('note'), 'has_official_jiexi': os.path.exists(f'{CR}/{i}_j.png'),
                          'q_img': q, 'j_img': f'{CR}/{i}_j.png' if os.path.exists(f'{CR}/{i}_j.png') else None,
                          'stem_img': f'{CR}/{i}_s.png' if os.path.exists(f'{CR}/{i}_s.png') else None, 'text': (r.get('text') or '')[:300]})
        cands.sort(key=lambda c: (c['kaofa'] or '', c['id']))
        teacher = []
        for b in bank:
            if b.get('module') != m or b['tid'] in used: continue
            e = ex.get(re.sub(r'x\d+$', '', b['tid'])) or {}
            teacher.append({'tid': b['tid'], 'source': b.get('source'), 'db_match': b.get('db_match'), 'level': b.get('level'), 'method': b.get('method'),
                            'kaofa': b.get('kaofa'), 'learn': b.get('learn'), 'stem': b.get('stem'), 'options': b.get('options'), 'answer': b.get('answer'),
                            'jiexi': b.get('jiexi'), 'has_figure': bool(b.get('figure')), 'review_crop': e.get('review_crop'), 'section': e.get('section')})
        sheets = []
        for k in range(0, len(cands), 8):
            p = f'{S}/w2/D{day:02d}_pool_{k // 8 + 1:02d}.png'
            sheet([(f"POOL {c['id']}", c['q_img']) for c in cands[k:k + 8]], p); sheets.append(p)
        later = [x['day'] for x in sched['schedule'] if x['math'] == m and x['day'] > day]
        pk = {'day': day, 'module': m, 'module_name': sched['names'][m], 'later_days': later, 'candidate_real': cands, 'teacher': teacher, 'sheets_pool': sheets}
        json.dump(pk, open(f'{S}/w2/D{day:02d}_packet.json', 'w'), ensure_ascii=False, indent=1)
        print(day, m, 'cands', len(cands), 'teacher', len(teacher), 'sheets', len(sheets),
              'giveaway', sum(1 for c in cands if c.get('giveaway')), 'no_jiexi', sum(1 for c in cands if not c['has_official_jiexi']))

if __name__ == '__main__':
    main([int(x) for x in sys.argv[1:]] or list(range(8, 15)))
