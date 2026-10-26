import json, subprocess, os
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
reg = [c for c, d, q, j in json.load(open(S + '/db/mock_papers.json'))]
for k in range(4):
    env = dict(os.environ, ZLPART=f'_m{k}')
    subprocess.Popen(['python3', S + '/scripts/zl_crop_all.py'] + reg[k::4], stdout=open(f'{S}/zl/crop_mock_{k}.log', 'w'), stderr=subprocess.STDOUT, env=env, cwd=S, start_new_session=True)
print('launched')
