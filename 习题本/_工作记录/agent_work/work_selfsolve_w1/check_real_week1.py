# 检查 gen/real_week1_logic.json：可读、31 条齐全、答案合法、验算脚本可运行且输出与答案一致
import json, os, subprocess, sys, collections

ROOT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
out = json.load(open(ROOT + '/gen/real_week1_logic.json', encoding='utf-8'))
tasks = json.load(open(ROOT + '/tasks_in/selfsolve_week1.json', encoding='utf-8'))
T = {t['id']: t for t in tasks}
errs = []

assert isinstance(out, list)
ids = [x['id'] for x in out]
if len(out) != 31: errs.append(f'条数 {len(out)} != 31')
if len(set(ids)) != len(ids): errs.append('id 重复')
if set(ids) != set(T): errs.append(f'id 不一致：缺 {set(T) - set(ids)}，多 {set(ids) - set(T)}')

COMPUTE = lambda m: m.startswith('C') or m in ('L01', 'L02')
for x in out:
    keys = {'id', 'answer', 'jiexi', 'confidence', 'note', 'verify'}
    if set(x) != keys: errs.append(f"{x['id']} 字段 {set(x)}")
    if x['answer'] not in ('A', 'B', 'C', 'D'): errs.append(f"{x['id']} 答案 {x['answer']}")
    if x['confidence'] not in ('high', 'medium', 'low'): errs.append(f"{x['id']} confidence {x['confidence']}")
    if x['confidence'] != 'high' and not x['note']: errs.append(f"{x['id']} 非 high 却没有 note")
    if '参考用时' in x['jiexi']: errs.append(f"{x['id']} 含参考用时")
    if f"故正确答案为 {x['answer']}" not in x['jiexi']: errs.append(f"{x['id']} 解析结论与答案不符")
    m = T[x['id']]['module']
    if COMPUTE(m):
        v = x['verify']
        if not v or not os.path.isfile(v):
            errs.append(f"{x['id']} 缺验算脚本"); continue
        if os.path.basename(v) != f"real_{x['id']}.py": errs.append(f"{x['id']} 脚本命名 {v}")
        r = subprocess.run([sys.executable, '-I', v], capture_output=True, text=True, timeout=300)
        last = [l for l in r.stdout.splitlines() if l.strip()][-1:] or ['']
        if r.returncode != 0 or last[0].strip() != x['answer']:
            errs.append(f"{x['id']} 脚本 rc={r.returncode} 输出末行={last[0]!r} 答案={x['answer']} {r.stderr[-300:]}")
        else:
            print(f"{x['id']:12s} 脚本输出 {last[0]} == 答案 {x['answer']}")
    else:
        if x['verify'] is not None: errs.append(f"{x['id']} 论证题 verify 应为 null")
        if len(x['jiexi']) > 250: errs.append(f"{x['id']} 论证题解析 {len(x['jiexi'])} 字 > 250")

cnt = collections.Counter(x['confidence'] for x in out)
print('完成条数', len(out), '把握程度', dict(cnt))
diff = [(x['id'], T[x['id']]['answer_given'], x['answer']) for x in out if T[x['id']]['answer_given'] and T[x['id']]['answer_given'] != x['answer']]
same = [(x['id'], T[x['id']]['answer_given']) for x in out if T[x['id']]['answer_given'] and T[x['id']]['answer_given'] == x['answer']]
print('与 answer_given 一致', same, '不一致', diff)
print('非 high：', [(x['id'], x['confidence']) for x in out if x['confidence'] != 'high'])
print('错误' if errs else '全部通过', *errs, sep='\n')
