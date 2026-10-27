"""Plan the 逻辑判断 / 综合推理 parts from real questions only (no variants): 20 logic + 5 综合推理 per day (day 1 had 10),
module of the day from db/schedule.json. Days are filled in order; when the day's module runs out, the day is
topped up from related modules. Days already delivered can be frozen (db/realonly_frozen.json) so that newly
added papers only fill later days. Writes db/realonly_plan.json."""
import json, os, re, glob, collections
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
PER_DAY = {'logic': 20, 'zh': 5}
EXCLUDE = {'2020SZ1-40'}                                    # L03 blueprint: official key indefensible
LATE = {'2021SD-74', '2025GK-111', '2020HB-109', '2020SD-75'}  # disputed keys: keep for late "讲评" days
TOPUP = {'L01': ['L02', 'L07', 'L05'], 'L02': ['L01', 'L07', 'L03'], 'L03': ['L05', 'L04'], 'L04': ['L06', 'L03'],
         'L05': ['L03', 'L04'], 'L06': ['L04', 'L03'], 'L07': ['L01', 'L02', 'L03'],
         'C01': ['C03', 'C02', 'C05', 'C04'], 'C02': ['C01', 'C03', 'C05', 'C04'], 'C03': ['C01', 'C02', 'C05', 'C04'],
         'C04': ['C05', 'C02', 'C01', 'C03'], 'C05': ['C04', 'C02', 'C01', 'C03']}
NO_JIEXI_PAPERS = ('2026GZ', '2026CQ', '2026HB')          # answers only (or none): 解析 must be written

def load_pool():
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    fix = json.load(open(S + '/db/answer_fixes.json'))
    items = {}
    for f in glob.glob(S + '/tasks_in/*.json'):
        t = json.load(open(f))
        if not isinstance(t, dict): continue  # other lists kept in tasks_in (not module task files)
        for q in t['real']:
            if q['module'][0] in 'LC':
                items[q['id']] = {'id': q['id'], 'module': q['module'], 'difficulty': q['difficulty'] or 2, 'kaofa': q.get('kaofa') or ''}
    for f in [S + '/cls/out_new_batch.jsonl'] + sorted(glob.glob(S + '/cls2/out_logic_new_*.jsonl')):  # + papers added 2026-10-26
        for l in open(f):
            l = l.strip()
            if not l: continue
            r = json.loads(l); m = str(r.get('module'))
            if r.get('kind', '逻辑') == '逻辑' and m[0] in 'LC' and not r.get('incomplete') and r['id'] not in items:
                items[r['id']] = {'id': r['id'], 'module': m, 'difficulty': r.get('difficulty') or 2, 'kaofa': r.get('kaofa') or '',
                                  'answer_check': r.get('answer_check')}
    for i, it in list(items.items()):
        r = raw[i]
        ans = r.get('answer_official') or (fix.get(i) or {}).get('answer')
        paper = i.rsplit('-', 1)[0]
        has_j = os.path.exists(f'{S}/crops/real2/{i}_j.png')
        if i in EXCLUDE: del items[i]; continue
        # tier: 0 official answer + official 解析; 1 official answer, 解析 text only; 2 needs self-solve; 3 no 解析 at all
        it['tier'] = 3 if paper in NO_JIEXI_PAPERS else (0 if ans and has_j else (1 if ans else 2))
        it['late'] = i in LATE
        it['paper'] = paper
        it['group'] = f"{paper}|{(r.get('stem_text') or '').strip()[:40]}" if (r.get('stem_text') or '').strip() else i
    return items

def units_of(items, module):
    by = collections.OrderedDict()
    for it in items.values():
        if it['module'] == module: by.setdefault(it['group'], []).append(it)
    us = []
    for g, its in by.items():
        its.sort(key=lambda x: int(x['id'].rsplit('-', 1)[1]))
        us.append({'ids': [x['id'] for x in its], 'difficulty': max(x['difficulty'] for x in its), 'tier': max(x['tier'] for x in its),
                   'late': any(x['late'] for x in its), 'kaofa': its[0]['kaofa'], 'module': module})
    us.sort(key=lambda u: (u['late'], u['tier'] >= 3, u['difficulty'], u['tier'], u['kaofa'], u['ids'][0]))
    return us

def plan(frozen=None):
    items = load_pool()
    sched = json.load(open(S + '/db/schedule.json'))['schedule']
    frozen = frozen or {}
    used = {i for d in frozen.values() for part in d.values() for i in part}
    out = {}
    for part, key in (('logic', 'logic'), ('zh', 'zh')):
        mods = sorted({it['module'] for it in items.values() if it['module'][0] == ('L' if part == 'logic' else 'C')})
        pools = {m: [u for u in units_of(items, m) if not set(u['ids']) & used] for m in mods}
        for s in sched:
            d = s['day']
            if str(d) in frozen and part in frozen[str(d)]:
                out.setdefault(d, {})[part] = frozen[str(d)][part]; continue
            need = PER_DAY[part]; chosen = []
            for m in [s[key]] + TOPUP.get(s[key], []):
                pool = pools.get(m, [])
                k = 0
                while k < len(pool) and need > 0:
                    u = pool[k]
                    if len(u['ids']) <= need:
                        chosen.append(u); need -= len(u['ids']); pool.pop(k)
                    else:
                        k += 1
                if need == 0: break
            # order inside the day: the day's own module first, then top-ups; easy -> hard; keep 一拖n groups together
            chosen.sort(key=lambda u: (u['module'] != s[key], u['difficulty'], u['kaofa'], u['ids'][0]))
            out.setdefault(d, {})[part] = [i for u in chosen for i in u['ids']]
    return out, items

if __name__ == '__main__':
    fz = json.load(open(S + '/db/realonly_frozen.json')) if os.path.exists(S + '/db/realonly_frozen.json') else {}
    out, items = plan(fz)
    json.dump({str(d): v for d, v in sorted(out.items())}, open(S + '/db/realonly_plan.json', 'w'), ensure_ascii=False, indent=1)
    sched = json.load(open(S + '/db/schedule.json'))['schedule']
    for s in sched:
        d = s['day']; o = out[d]
        if not o['logic'] and not o['zh']: continue
        lm = collections.Counter(items[i]['module'] for i in o['logic']); zm = collections.Counter(items[i]['module'] for i in o['zh'])
        tiers = collections.Counter(items[i]['tier'] for i in o['logic'] + o['zh'])
        print(f"day {d:2d} logic {s['logic']} {len(o['logic']):2d} {dict(lm)} | zh {s['zh']} {len(o['zh']):2d} {dict(zm)} | tiers {dict(sorted(tiers.items()))}")
