"""Match the teacher's examples to questions already in the real-question DB (same question, maybe different
wording/OCR). Adds 'db_match' (id) and 'db_score' to teacher/examples.json."""
import json, re, difflib
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def norm(s):
    s = re.sub(r'^[（(]\s*\d{4}[^）)]{0,14}[）)]', '', s.strip())
    s = re.sub(r'^\s*\d{1,3}\s*[\.．、]', '', s)
    s = s.split('\nA')[0]
    return re.sub(r'[\s，。,\.、：:；;？?！!（）()“”"\'‘’《》\[\]【】\-—]', '', s)

def main():
    raw = [r for r in json.load(open(S + '/db/real_raw.json')) if r['kind'] == '数学运算']
    rn = [(r['id'], norm(r.get('text') or '')) for r in raw]
    exs = json.load(open(S + '/teacher/examples.json'))
    grams = {}
    for i, t in rn:
        for k in range(0, max(1, len(t) - 8), 4):
            grams.setdefault(t[k:k + 8], set()).add(i)
    rmap = dict(rn)
    hit = 0
    for e in exs:
        q = norm(e['question'])
        cands = {}
        for k in range(0, max(1, len(q) - 8), 2):
            for i in grams.get(q[k:k + 8], ()):
                cands[i] = cands.get(i, 0) + 1
        best = None
        for i, _ in sorted(cands.items(), key=lambda x: -x[1])[:5]:
            sc = difflib.SequenceMatcher(None, q[:120], rmap[i][:120]).ratio()
            if not best or sc > best[1]: best = (i, sc)
        e['db_match'], e['db_score'] = (best[0], round(best[1], 2)) if best and best[1] >= 0.6 else (None, round(best[1], 2) if best else 0)
        hit += bool(e['db_match'])
    json.dump(exs, open(S + '/teacher/examples.json', 'w'), ensure_ascii=False, indent=1)
    print('examples', len(exs), 'matched to DB', hit)

if __name__ == '__main__':
    main()
