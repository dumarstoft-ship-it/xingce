# 独立校验 blueprints/M03.json：可读、结构、每天=45、真题不重不漏、种子/方向合法、自解与问题清单
import json, re, collections, sys
B = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
d = json.load(open(B + '/blueprints/M03.json', encoding='utf-8'))
task = json.load(open(B + '/tasks_in/M03.json', encoding='utf-8'))
ids = [q['id'] for q in task['real']]
ok = True
def bad(msg):
    global ok; ok = False; print('FAIL', msg)
assert set(d) == {'module', 'days', 'self_solved', 'issues'}, d.keys()
if d['module'] != 'M03': bad('module')
if [x['day'] for x in d['days']] != task['days']: bad(f"天数 {[x['day'] for x in d['days']]} != {task['days']}")
seen = []
num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五']
for day in d['days']:
    nr = sum(len(g['real']) for g in day['groups']); nv = sum(v['n'] for g in day['groups'] for v in g['variants'])
    print(f"第{day['day']}天：真题{nr} + 改编{nv} = {nr + nv}；组数{len(day['groups'])}；方向", dict(collections.Counter(v['direction'] for g in day['groups'] for v in g['variants'])))
    if nr + nv != 45: bad(f"第{day['day']}天合计{nr + nv}")
    for g in day['groups']:
        if not re.match(r'^考法(十[一二三四五]?|[一二三四五六七八九])：', g['title']): bad('标题 ' + g['title'])
        seen += g['real']
        for v in g['variants']:
            if set(v) != {'n', 'direction', 'seed', 'idea'} or v['n'] != 1: bad('variant字段 ' + str(v)[:60])
            if v['direction'] not in ('巩固', '深化', '拓展'): bad('方向 ' + v['direction'])
            if not (v['seed'] in ids or (v['seed'][:2] == '考法' and v['seed'][2:] in num)): bad('种子 ' + v['seed'])
            if not re.match(r'^〔\d+-\d+-\d+〕【', v['idea']) or '题干：' not in v['idea'] or '答案：' not in v['idea']: bad('idea格式 ' + v['idea'][:30])
c = collections.Counter(seen)
dup = [k for k, n in c.items() if n > 1]; miss = sorted(set(ids) - set(seen)); extra = sorted(set(seen) - set(ids))
print(f'真题：排入{len(seen)}道，去重{len(c)}道，题库{len(ids)}道；重复{dup}，遗漏{miss}，多出{extra}')
if dup or miss or extra: bad('真题不重不漏')
need_self = sorted(q['id'] for q in task['real'] if q['needs_self_solve'])
got_self = sorted(s['id'] for s in d['self_solved'])
print('自解：', [(s['id'], s['answer']) for s in d['self_solved']])
if got_self != need_self: bad(f'自解名单 {got_self} != {need_self}')
for s in d['self_solved']:
    if s['answer'] not in 'ABCD' or not s['note']: bad('自解字段 ' + s['id'])
pend = sorted(q['id'] for q in task['real'] if q['answer_pending_ocr'])
if set(pend) & set(got_self): bad('待识别题被自解')
print('问题清单：', len(d['issues']), '条 ->', [i['id'] for i in d['issues']])
for i in d['issues']:
    if set(i) != {'id', 'problem'} or i['id'] not in ids: bad('issue ' + str(i)[:40])
vid = [re.match(r'^〔([\d-]+)〕', v['idea']).group(1) for day in d['days'] for g in day['groups'] for v in g['variants']]
if len(vid) != len(set(vid)): bad('改编编号重复')
print('改编总数', len(vid), '；JSON 校验', '通过' if ok else '未通过')
sys.exit(0 if ok else 1)
