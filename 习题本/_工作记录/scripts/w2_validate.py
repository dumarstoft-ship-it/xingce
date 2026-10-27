"""Check the week-2 math decisions (w2/D{dd}_decision.json): 30 items, ids from the day's packet, no question twice
(a teacher question's db_match counts as that real question, across days too), variant numbers matching new_variants,
and every real question has an answer (official, fixed, or the planner's check) and a 解析 (official or the planner's note).
Usage: w2_validate.py [first_day last_day]"""
import json, os, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def main(days):
    db = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    ovr = json.load(open(S + '/db/real_overrides.json'))
    fix = json.load(open(S + '/db/answer_fixes.json'))
    seen, bad = {}, 0
    for d in range(1, 8):  # week 1 as delivered
        for pt in json.load(open(f'{S}/out/final/D{d}.json'))['parts']:
            for it in pt['items']: seen[it.get('id') or it.get('tid') or it.get('vid')] = d
    for day in days:
        p = f'{S}/w2/D{day:02d}_decision.json'
        if not os.path.exists(p):
            print(day, 'not ready'); continue
        d = json.load(open(p)); pk = json.load(open(f'{S}/w2/D{day:02d}_packet.json'))
        cand = {c['id']: c for c in pk['candidate_real']}; tea = {t['tid']: t for t in pk['teacher']}
        notes, checks = d.get('jiexi_notes') or {}, d.get('answer_checks') or {}
        items = [e for g in d['groups'] for e in g['items']]
        probs = []
        if len(items) != 30: probs.append(f'{len(items)} items')
        vs = sorted(e['variant'] for e in items if 'variant' in e)
        nv = sorted(v['n'] for v in d.get('new_variants') or [])
        if vs != nv: probs.append(f'variants {vs} != new_variants {nv}')
        for e in items:
            if 'real' in e:
                i = key = e['real']; c = cand.get(i)
                if not c:  # another module's question (e.g. via a teacher question's db_match)
                    if i not in db or not os.path.exists(f'{S}/crops/real2/{i}_q.png'):
                        probs.append(f'{i} not in packet and no crop'); continue
                    r = db[i]
                    c = {'answer': r.get('answer_official') or (fix.get(i) or {}).get('answer'), 'has_official_jiexi': os.path.exists(f'{S}/crops/real2/{i}_j.png'),
                         'answer_source': 'official' if r.get('answer_official') else ('fix' if fix.get(i) else 'classifier')}
                    print('    note:', i, 'is outside the packet')
                ans = (ovr.get(i) or {}).get('answer') or (c['answer'] if c['answer_source'] in ('official', 'fix') else None)
                chk = (checks.get(i) or {}).get('answer')
                if not ans and not chk: probs.append(f'{i} no answer (classifier only)')
                if ans and chk and ans != chk: probs.append(f'{i} planner {chk} != {c["answer_source"]} {ans}')
                if not c['has_official_jiexi'] and i not in notes and not db[i].get('jiexi_raw'): probs.append(f'{i} no 解析')
            elif 'teacher' in e:
                t = tea.get(e['teacher'])
                if not t:
                    probs.append(f'{e["teacher"]} not in packet'); continue
                key = t.get('db_match') or e['teacher']
            else:
                continue
            if key in seen: probs.append(f'{key} also on day {seen[key]}')
            seen[key] = day
        n = {k: sum(1 for e in items if k in e) for k in ('real', 'teacher', 'variant')}
        print(day, d['module'], n, 'reserve', len(d.get('reserve') or []), 'PROBLEMS' if probs else 'ok')
        for x in probs: print('   ', x)
        bad += len(probs)
    return bad

if __name__ == '__main__':
    a = [int(x) for x in sys.argv[1:3]] or [8, 14]
    sys.exit(1 if main(range(a[0], a[1] + 1)) else 0)
