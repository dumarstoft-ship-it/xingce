"""Merge the two independent solves of the mock 资料 passages (zl/solve/out_A*.json, out_B*.json): agreed answers
go into db/zl_fixes.json with the clearer 解析; disagreements and low-confidence items are listed for adjudication."""
import json, glob, os, re
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def load(prefix):
    out = {}
    for f in sorted(glob.glob(f'{S}/zl/solve/out_{prefix}*.json')):
        for e in json.load(open(f)):
            for k, q in enumerate(e['q'], 1):
                out[(e['mat'], q.get('n', k))] = q
    return out
if __name__ == '__main__':
    A, B = load('A'), load('B')
    raw = json.load(open(S + '/db/zl_raw.json'))
    rid = {(r['mat'], r['pos']): r['id'] for r in raw}
    adj = json.load(open(S + '/zl/solve/adjudicated.json')) if os.path.exists(S + '/zl/solve/adjudicated.json') else {}
    notes = json.load(open(S + '/zl/solve/notes.json')) if os.path.exists(S + '/zl/solve/notes.json') else {}  # caveats printed under the 解析
    fix = json.load(open(S + '/db/zl_fixes.json'))
    agree, dis, low, missing = 0, [], [], []
    for key in sorted(set(A) | set(B)):
        a, b = A.get(key), B.get(key)
        i = rid[key]
        if i in adj:  # settled by a third solve / by hand
            fix[i] = {'answer': adj[i]['answer'], 'source': '自解（核定）', 'jiexi': adj[i]['jiexi']}
            continue
        if not a or not b: missing.append(i); continue
        if a['answer'] == b['answer']:
            agree += 1
            best = a if (a.get('confidence') != 'low' or b.get('confidence') == 'low') else b
            fix[i] = {'answer': a['answer'], 'source': '自解（两人独立求解一致）', 'jiexi': best['jiexi']}
            if i in notes: fix[i]['extra'] = notes[i]
            if a.get('confidence') == 'low' or b.get('confidence') == 'low':
                low.append((i, a['answer'], a.get('problem'), b.get('problem')))
        else:
            dis.append((i, a['answer'], b['answer'], a.get('confidence'), b.get('confidence')))
            fix.pop(i, None)
    json.dump(fix, open(S + '/db/zl_fixes.json', 'w'), ensure_ascii=False, indent=1)
    json.dump({'disagree': dis, 'low': low, 'missing': missing}, open(S + '/zl/solve/to_adjudicate.json', 'w'), ensure_ascii=False, indent=1)
    print('agree', agree, 'disagree', len(dis), 'low-confidence agreed', len(low), 'missing', len(missing))
    for d in dis: print('DIS', d)
    for l in low: print('LOW', l[0], l[1], (l[2] or '')[:80], '|', (l[3] or '')[:80])
