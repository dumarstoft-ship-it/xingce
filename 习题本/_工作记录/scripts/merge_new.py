"""Append the new papers' records (db/real_raw_new.json) to db/real_raw.json, skipping questions that duplicate
one already in the bank (国考 副省级/地市级/行政执法 share many questions). Duplicates -> db/dups_new.json."""
import json, os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
KINDS = ('数学运算', '数字推理', '逻辑')

def norm(t):
    t = re.sub(r'^\s*\d{1,3}\s*[\.、．]?', '', t or '')
    return re.sub(r'[^一-龥A-Za-z0-9]', '', t)

def sh(s, k=6): return {s[i:i + k] for i in range(max(1, len(s) - k + 1))}

if __name__ == '__main__':
    old = json.load(open(S + '/db/real_raw.json')); new = json.load(open(S + '/db/real_raw_new.json'))
    have = {r['id'] for r in old}
    pool = [(r['id'], norm(r['text'])[:160]) for r in old if r['kind'] in KINDS]
    pool = [(i, s, sh(s) if len(s) >= 30 else None) for i, s in pool]
    dups, add = {}, []
    for r in new:
        if r['id'] in have: continue
        if r['kind'] in KINDS:
            s = norm(r['text'])[:160]
            hit = None
            if len(s) >= 30:
                g = sh(s)
                for i, s2, g2 in pool:
                    if g2 and len(g & g2) / max(1, min(len(g), len(g2))) > 0.75: hit = i; break
            elif len(s) >= 8:  # short number series: exact match only
                hit = next((i for i, s2, g2 in pool if s2 == s), None)
            if hit: dups[r['id']] = hit; continue
            pool.append((r['id'], s, sh(s) if len(s) >= 30 else None))
        add.append(r)
    shutil.copy(S + '/db/real_raw.json', S + '/db/real_raw_v14_before_newpapers.json')
    json.dump(old + add, open(S + '/db/real_raw.json', 'w'), ensure_ascii=False)
    json.dump(dups, open(S + '/db/dups_new.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print('added', len(add), Counter(r['kind'] for r in add if r['kind'] in KINDS), '| dups', len(dups), Counter(r['kind'] for r in new if r['id'] in dups))
