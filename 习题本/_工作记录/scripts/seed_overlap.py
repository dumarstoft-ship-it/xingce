"""Flag variants that reuse most of their seed real question's numbers (the student just did that question)."""
import json, glob, os, re, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
NUM = re.compile(r'\d+(?:\.\d+)?')

def nums(s):
    s = re.sub(r'\$[^$]*\$', lambda m: ' ' + ' '.join(NUM.findall(m.group(0))) + ' ', s or '')
    return {n for n in NUM.findall(s) if n not in ('0', '1', '2', '3', '4', '5', '10', '100')}

def main(pattern):
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    for f in sorted(glob.glob(f'{S}/gen/{pattern}')):
        if os.path.basename(f).startswith('real_'): continue
        for v in json.load(open(f)):
            seed = (v.get('seed') or '').split()[0] if v.get('seed') else ''
            if seed not in raw: continue
            rn = nums(re.sub(r'^\s*\d{1,3}', '', raw[seed].get('text', '')).split('\nA')[0])
            vn = nums(v.get('shared_stem', '') + ' ' + v['stem'])
            if len(rn) >= 2:
                ov = rn & vn
                if len(ov) >= max(2, 0.6 * len(rn)):
                    print(os.path.basename(f), v['vid'], seed, 'shared numbers:', sorted(ov), 'of', sorted(rn))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'D*.json')
