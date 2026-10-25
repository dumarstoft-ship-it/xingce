import json, collections
BASE = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/harden/'
P = json.load(open(BASE + 'D03_packet.json'))
D = json.load(open(BASE + 'D03_decision.json', encoding='utf-8'))
assert set(D) == {"day","remove","add_real","add_teacher","new_variants","keep_notes"}, set(D)
assert D['day'] == 3
groups = P['groups']
items = P['items']
key_of = lambda x: x.get('id') or x.get('vid')
day_keys = {key_of(x): x for x in items}
cand = {c['id']: c for c in P['candidate_real']}
teach = {t['tid']: t for t in P['teacher']}

rm = [r['key'] for r in D['remove']]
assert len(rm) == len(set(rm)), 'dup remove'
for k in rm: assert k in day_keys, ('unknown remove key', k)
nr, nt, nv = len(D['add_real']), len(D['add_teacher']), len(D['new_variants'])
print('remove', len(rm), '| add_real', nr, '| add_teacher', nt, '| new_variants', nv, '| sum', nr+nt+nv)
assert len(rm) == nr + nt + nv

for a in D['add_real']:
    assert a['id'] in cand, ('not in candidate_real', a['id'])
    assert a['id'] not in day_keys
    assert a['group'] in groups, a
    c = cand[a['id']]
    assert c['answer'], a['id']
    if not c['has_official_jiexi']:
        assert len(a['jiexi_note']) > 80, ('needs reliable jiexi', a['id'])
ids = [a['id'] for a in D['add_real']]
assert len(ids) == len(set(ids))

in_day_ids = {x.get('id') for x in items if x.get('id')}
for t in D['add_teacher']:
    assert t['tid'] in teach, t
    assert t['group'] in groups, t
    dm = teach[t['tid']]['db_match']
    assert not dm, ('teacher with db_match should go to add_real or be skipped', t['tid'], dm)
tids = [t['tid'] for t in D['add_teacher']]
assert len(tids) == len(set(tids))
# teacher items with db_match: must be in day already or in add_real
for tid, t in teach.items():
    if t['db_match'] and (t['db_match'] in ids):
        print('teacher', tid, '->', t['db_match'], 'added via add_real')
    elif t['db_match']:
        print('teacher', tid, '->', t['db_match'], 'in day already:', t['db_match'] in in_day_ids)

for v in D['new_variants']:
    assert v['group'] in groups, v
    assert len(v['kaofa']) <= 20, (v['kaofa'], len(v['kaofa']))
    assert v['idea'] and v['difficulty_hint']
    print('variant kaofa len', len(v['kaofa']), v['kaofa'])

# final composition per group
final = collections.Counter()
for x in items:
    if key_of(x) not in rm:
        final[x['group']] += 1
for a in D['add_real']: final[a['group']] += 1
for t in D['add_teacher']: final[t['group']] += 1
for v in D['new_variants']: final[v['group']] += 1
tot = sum(final.values())
print('final total', tot)
for g in groups:
    print(final[g], g[:12])
assert tot == 45
assert all(final[g] >= 1 for g in groups), 'a group vanished'
kept = [key_of(x) for x in items if key_of(x) not in rm]
print('kept:', kept)
print('keep_notes chars', len(D['keep_notes']))
print('OK')
