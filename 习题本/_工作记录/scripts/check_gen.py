"""Validate generated variant files and re-run their verification scripts independently."""
import json, glob, os, re, subprocess, sys
from collections import Counter
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def run_verify(path):
    p = path if path.startswith('/') else os.path.join(S, path)
    if not os.path.exists(p): return None, 'missing script'
    try:
        r = subprocess.run([sys.executable, '-I', p], capture_output=True, text=True, timeout=60, cwd=os.path.dirname(p))
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    out = (r.stdout or '').strip().split('\n')
    letters = re.findall(r'\b([A-D])\b', out[-1] if out else '')
    return (letters[-1] if letters else None), (r.stderr or '')[-200:]

def check(pattern):
    files = sorted(glob.glob(os.path.join(S, 'gen', pattern)))
    allv = []
    for f in files:
        try:
            vs = json.load(open(f))
        except Exception as e:
            print('BAD JSON', f, e); continue
        for v in vs: v['_file'] = os.path.basename(f)
        allv += vs
    probs = []
    vids = Counter(v.get('vid') for v in allv)
    for v in allv:
        vid = v.get('vid')
        if vids[vid] > 1: probs.append((vid, 'duplicate vid'))
        o = v.get('options') or {}
        if sorted(o) != ['A', 'B', 'C', 'D']: probs.append((vid, 'options keys ' + str(sorted(o))))
        if len(set(map(str, o.values()))) < 4: probs.append((vid, 'duplicate option text'))
        if v.get('answer') not in ('A', 'B', 'C', 'D'): probs.append((vid, 'bad answer'))
        if not v.get('stem') or not v.get('jiexi'): probs.append((vid, 'missing stem/jiexi'))
        if v.get('verify'):
            got, err = run_verify(v['verify'])
            if got != v.get('answer'): probs.append((vid, f'verify gave {got} vs key {v.get("answer")} {err.strip()[:80]}'))
    dist = Counter(v.get('answer') for v in allv)
    return allv, probs, dist

if __name__ == '__main__':
    allv, probs, dist = check(sys.argv[1])
    print('variants', len(allv), 'answers', dict(dist))
    for p in probs: print('PROBLEM', p)
    print('verified', sum(1 for v in allv if v.get('verify')), 'problems', len(probs))
