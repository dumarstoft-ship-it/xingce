# make blind-review question files (no answers) from generated variant files
import json, glob, os, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def strip(pattern, out_q, out_key):
    vs = []
    for f in sorted(glob.glob(os.path.join(S, 'gen', pattern))):
        if os.path.basename(f).startswith('real_'): continue
        vs += json.load(open(f))
    q = [{k: v[k] for k in ('vid', 'group', 'shared_stem', 'stem', 'options', 'figure_svg') if k in v} for v in vs]
    json.dump(q, open(out_q, 'w'), ensure_ascii=False, indent=1)
    json.dump(vs, open(out_key, 'w'), ensure_ascii=False, indent=1)
    return len(vs)
if __name__ == '__main__':
    print(strip(sys.argv[1], sys.argv[2], sys.argv[3]))
