# 检查 teacher/bank_B2.json：JSON 可读、tid 齐全、选项/答案合法、验算脚本输出与答案一致、字数限制
import json, os, subprocess, sys, collections

BASE = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
bank = json.load(open(BASE + '/teacher/bank_B2.json', encoding='utf-8'))
want = [f'T{i:03d}' for i in range(38, 82)]
tids = [e['tid'] for e in bank]
errs = []
if tids != want:
    errs.append(f'tid 不齐/顺序不对：缺{sorted(set(want) - set(tids))} 多{sorted(set(tids) - set(want))}')
if len(set(tids)) != len(tids):
    errs.append('tid 重复')

keys = ['tid', 'keep', 'db_match', 'module', 'kaofa', 'method', 'source', 'stem', 'options', 'options_added',
        'answer', 'jiexi', 'learn', 'level', 'figure', 'verify', 'issues']
mods = collections.Counter()
for e in bank:
    t = e['tid']
    if list(e.keys()) != keys:
        errs.append(f'{t}: 字段不符 {list(e.keys())}')
    if not e['keep']:
        if not e['issues']:
            errs.append(f'{t}: 不收但未说明原因')
        continue
    mods[e['module']] += 1
    o = e['options']
    if not isinstance(o, dict) or sorted(o) != ['A', 'B', 'C', 'D'] or not all(str(v).strip() for v in o.values()):
        errs.append(f'{t}: 选项不全')
    if len(set(o.values())) != 4:
        errs.append(f'{t}: 选项重复')
    if e['answer'] not in ('A', 'B', 'C', 'D'):
        errs.append(f'{t}: 答案非法')
    if e['module'] not in [f'M{i:02d}' for i in range(1, 15)]:
        errs.append(f'{t}: 模块非法')
    if e['level'] not in ('基础', '中等', '难', '很难'):
        errs.append(f'{t}: level 非法')
    for k, lim in (('kaofa', 20), ('method', 20), ('jiexi', 300)):
        if not e[k] or len(e[k]) > lim:
            errs.append(f'{t}: {k} 长度 {len(e[k])} 超限 {lim}')
    if not e['learn'] or not e['stem']:
        errs.append(f'{t}: learn/stem 为空')
    for bad in ('公众号', '樱有尽有', '参考用时', '例1', '例2'):
        for k in ('stem', 'jiexi', 'learn'):
            if bad in e[k] or any(bad in str(v) for v in o.values()):
                errs.append(f'{t}: {k} 含禁用字样 {bad}')
    if e['figure'] is not None and e['figure'].get('type') not in ('svg', 'crop_needed'):
        errs.append(f'{t}: figure 非法')
    v = e['verify']
    if not v or not os.path.exists(v):
        errs.append(f'{t}: 验算脚本不存在')
        continue
    r = subprocess.run([sys.executable, v], capture_output=True, text=True, timeout=300)
    out = r.stdout.strip().splitlines()
    if r.returncode != 0 or not out or out[-1].strip() != e['answer'] or len(out) != 1:
        errs.append(f'{t}: 验算输出 {out!r} 与答案 {e["answer"]} 不一致 (rc={r.returncode}) {r.stderr[-300:]}')

keep = [e for e in bank if e['keep']]
print('总数', len(bank), '收入', len(keep), '不收', len(bank) - len(keep))
print('模块分布', dict(sorted(mods.items())))
print('难度分布', dict(collections.Counter(e['level'] for e in keep)))
print('db_match', {e['tid']: e['db_match'] for e in bank if e['db_match']})
print('jiexi 最长', max(len(e['jiexi']) for e in keep))
print('错误：' + ('无' if not errs else ''))
for x in errs:
    print('  ', x)
sys.exit(1 if errs else 0)
