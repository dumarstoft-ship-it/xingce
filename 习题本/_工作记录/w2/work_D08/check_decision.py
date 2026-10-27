import json
P = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/w2/'
d = json.load(open(P + 'D08_decision.json'))
pk = json.load(open(P + 'D08_packet.json'))
real_ids = {c['id'] for c in pk['candidate_real']}
tmap = {t['tid']: t for t in pk['teacher']}
# known same-question equivalences (db_match, plus T021 == 2020GKD-68 found by reading)
equiv = {t['tid']: t['db_match'] for t in pk['teacher'] if t['db_match']}
equiv['T021'] = '2020GKD-68'
items = [it for g in d['groups'] for it in g['items']]
assert d['day'] == 8 and d['module'] == 'M02'
assert 4 <= len(d['groups']) <= 7, len(d['groups'])
assert len(items) == 30, len(items)
keys = []
nr = nt = nv = 0
for it in items:
    assert len(it) == 1
    (k, v), = it.items()
    if k == 'real':
        assert v in real_ids, v; nr += 1; keys.append(v)
    elif k == 'teacher':
        assert v in tmap, v; nt += 1; keys.append(equiv.get(v, v))
    elif k == 'variant':
        nv += 1; keys.append('V%d' % v)
    else:
        raise AssertionError(k)
assert len(keys) == len(set(keys)), 'duplicate item'
vn = sorted(int(k[1:]) for k in keys if k.startswith('V'))
assert vn == sorted(x['n'] for x in d['new_variants']), (vn, d['new_variants'])
titles = {g['title'] for g in d['groups']}
for x in d['new_variants']:
    assert x['group'] in titles, x['group']
    assert len(x['kaofa']) <= 20, (x['kaofa'], len(x['kaofa']))
    assert x['idea'] and x['difficulty_hint']
    # the variant must sit in the group it names
    g = [g for g in d['groups'] if {'variant': x['n']} in g['items']][0]
    assert g['title'] == x['group']
used = set(keys)
for r in d['reserve']:
    rr = equiv.get(r, r)
    assert rr in real_ids or r in tmap, r
    assert rr not in used, ('reserve item used today', r)
assert len(d['reserve']) == len(set(d['reserve']))
for k in d['jiexi_notes']:
    assert k in used, ('jiexi note for unused item', k)
for k, v in d['answer_checks'].items():
    assert k in real_ids, k
    assert v['answer'] in 'ABCD'
# official answers must agree with my checks where official exists
for c in pk['candidate_real']:
    if c['id'] in d['answer_checks'] and c['answer']:
        assert c['answer'] == d['answer_checks'][c['id']]['answer'], (c['id'], c['answer'], d['answer_checks'][c['id']])
# every used real item without an official answer has a check; every used real item w/o official jiexi has a full note
cmap = {c['id']: c for c in pk['candidate_real']}
for k in used:
    if k in cmap:
        c = cmap[k]
        if c['answer_source'] != 'official':
            assert k in d['answer_checks'], k
        if not c['has_official_jiexi']:
            assert k in d['jiexi_notes'], ('needs full jiexi', k)
print('groups:', [(g['title'][:4], len(g['items'])) for g in d['groups']])
print('real', nr, 'teacher', nt, 'variant', nv, 'total', len(items))
print('reserve', len(d['reserve']), 'jiexi_notes', len(d['jiexi_notes']), 'answer_checks', len(d['answer_checks']))
print('ALL CHECKS PASSED')
