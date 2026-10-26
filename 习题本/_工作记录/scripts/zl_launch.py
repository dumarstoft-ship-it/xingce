import json, subprocess, os, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
raw = json.load(open(S + '/db/zl_raw.json'))
done = set(sys.argv[1:])
papers = sorted({r['paper'] for r in raw} - done)
lab = sorted({r['paper'] for r in raw if r.get('acc') is not None} - done)
order = lab + [p for p in papers if p not in lab]
for k in range(4):
    ps = order[k::4]
    env = dict(os.environ, ZLPART=f'_{k}')
    subprocess.Popen(['python3', S + '/scripts/zl_crop_all.py'] + ps, stdout=open(f'{S}/zl/crop_all_{k}.log', 'w'), stderr=subprocess.STDOUT, env=env, cwd=S, start_new_session=True)
    print(k, len(ps), ps[:6])
