import subprocess
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
for k in range(4):
    subprocess.Popen(['python3', S + '/scripts/zl_jx_all.py', str(k), '4'], stdout=open(f'{S}/zl/jx_{k}.log', 'w'), stderr=subprocess.STDOUT, cwd=S, start_new_session=True)
print('launched')
