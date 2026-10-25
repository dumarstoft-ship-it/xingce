import json, sys, collections
H = sys.argv[1]
P = json.load(open(H + '/D02_packet.json'))
D = json.load(open(H + '/D02_decision.json'))
G = P['groups']
items = {(it.get('id') or it.get('vid')): it for it in P['items']}
cand = {c['id']: c for c in P['candidate_real']}
teach = {t['tid']: t for t in P['teacher']}
err = []
assert D['day'] == 2
nr, na, nt, nv = len(D['remove']), len(D['add_real']), len(D['add_teacher']), len(D['new_variants'])
print('remove', nr, '| add_real', na, '| add_teacher', nt, '| new_variants', nv, '| sum adds', na + nt + nv)
if nr != na + nt + nv: err.append('count mismatch')
rk = [r['key'] for r in D['remove']]
if len(set(rk)) != len(rk): err.append('dup remove')
for r in D['remove']:
    if r['key'] not in items: err.append('remove key not in day: ' + r['key'])
    if not r['why'].strip(): err.append('empty why ' + r['key'])
ids = [a['id'] for a in D['add_real']]
if len(set(ids)) != len(ids): err.append('dup add_real')
for a in D['add_real']:
    c = cand.get(a['id'])
    if not c: err.append('add_real not in candidate_real: ' + a['id']); continue
    if not c.get('answer'): err.append('no answer ' + a['id'])
    if not c.get('has_official_jiexi'): err.append('no official jiexi ' + a['id'])
    if a['group'] not in G: err.append('bad group ' + a['id'])
    if a['id'] in items: err.append('already in day ' + a['id'])
tids = [a['tid'] for a in D['add_teacher']]
if len(set(tids)) != len(tids): err.append('dup teacher')
for a in D['add_teacher']:
    t = teach.get(a['tid'])
    if not t: err.append('tid not in packet ' + a['tid']); continue
    if t.get('db_match'): err.append('teacher with db_match should be add_real: ' + a['tid'])
    if a['group'] not in G: err.append('bad group ' + a['tid'])
# teacher items whose db_match was added must carry a jiexi_note
dbm = {t['db_match']: t['tid'] for t in P['teacher'] if t.get('db_match')}
for a in D['add_real']:
    if a['id'] in dbm and not a['jiexi_note'].strip(): err.append('missing teacher note ' + a['id'])
for v in D['new_variants']:
    if v['group'] not in G: err.append('bad variant group')
    if len(v['kaofa']) > 20: err.append('kaofa too long: ' + v['kaofa'])
    for k in ('idea', 'difficulty_hint'):
        if not v[k].strip(): err.append('empty ' + k)
# resulting composition
removed = set(rk)
cnt = collections.Counter()
for k, it in items.items():
    if k not in removed: cnt[it['group']] += 1
for a in D['add_real'] + D['add_teacher'] + D['new_variants']:
    cnt[a['group']] += 1
total = sum(cnt.values())
print('total after =', total)
for gname in G: print(f'  {cnt[gname]:2d}  {gname}')
if total != 45: err.append('total != 45')
if any(cnt[gname] == 0 for gname in G): err.append('a group vanished')
print('kept:', [k for k in items if k not in removed])
print('keep_notes chars:', len(D['keep_notes']))
print('ERRORS:', err if err else 'none')
