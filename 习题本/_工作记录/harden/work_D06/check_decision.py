"""Validate harden/D06_decision.json against the packet."""
import json
from collections import Counter

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
pk = json.load(open(f'{S}/harden/D06_packet.json'))
d = json.load(open(f'{S}/harden/D06_decision.json'))

items = {(x.get('id') or x.get('vid')): x for x in pk['items']}
cand = {c['id']: c for c in pk['candidate_real']}
teach = {t['tid']: t for t in pk['teacher']}
teacher_db = {t['db_match']: t['tid'] for t in pk['teacher'] if t['db_match']}
groups = set(pk['groups'])
errs = []

rm = [r['key'] for r in d['remove']]
ar = [a['id'] for a in d['add_real']]
at = [a['tid'] for a in d['add_teacher']]
nv = d['new_variants']
print('remove', len(rm), '| add_real', len(ar), '| add_teacher', len(at), '| new_variants', len(nv))
if len(rm) != len(ar) + len(at) + len(nv):
    errs.append('count mismatch')
for k, c in Counter(rm + ar + at).items():
    if c > 1:
        errs.append(f'duplicate {k}')
for k in rm:
    if k not in items:
        errs.append(f'remove key not in items: {k}')
for r in d['remove']:
    if not r['why'].strip():
        errs.append(f'empty why {r["key"]}')
kept = [k for k in items if k not in rm]
for a in d['add_real']:
    i = a['id']
    if i in items:
        errs.append(f'add_real already in day: {i}')
    if i not in cand and i not in teacher_db:
        errs.append(f'add_real not in candidate_real nor teacher db_match: {i}')
    src = cand.get(i)
    if src and not src['has_official_jiexi'] and len(a['jiexi_note']) < 60:
        errs.append(f'{i}: no official jiexi but jiexi_note too thin')
    if a['group'] not in groups:
        errs.append(f'bad group {i}')
for a in d['add_teacher']:
    t = teach.get(a['tid'])
    if not t:
        errs.append(f'unknown tid {a["tid"]}')
    elif t['db_match']:
        errs.append(f'{a["tid"]} has db_match {t["db_match"]}; should go to add_real')
    if a['group'] not in groups:
        errs.append(f'bad group {a["tid"]}')
for i, v in enumerate(nv, 1):
    if v['group'] not in groups:
        errs.append(f'bad group NV{i}')
    if len(v['kaofa']) > 20:
        errs.append(f'NV{i} kaofa >20: {len(v["kaofa"])}')
    for f in ('idea', 'difficulty_hint'):
        if not v[f].strip():
            errs.append(f'NV{i} empty {f}')
# teacher items whose db_match is used must be via add_real
for tid in at:
    pass

# order coverage
seq = [(o['group'], k) for o in d['order'] for k in o['seq']]
keys_in_order = [k for _, k in seq]
expected = set(kept) | set(ar) | set(at) | {f'新改编#{i}' for i in range(1, len(nv) + 1)}
print('order length', len(keys_in_order), 'expected', len(expected))
if Counter(keys_in_order) != Counter(expected):
    errs.append(f'order mismatch: missing {expected - set(keys_in_order)}, extra {set(keys_in_order) - expected}')
# group consistency between order and declared groups
gmap = {k: items[k]['group'] for k in kept}
gmap.update({a['id']: a['group'] for a in d['add_real']})
gmap.update({a['tid']: a['group'] for a in d['add_teacher']})
gmap.update({f'新改编#{i}': v['group'] for i, v in enumerate(nv, 1)})
for g, k in seq:
    if gmap.get(k) != g:
        errs.append(f'group mismatch for {k}: order {g} vs declared {gmap.get(k)}')
# every group still present, and group order follows packet
present = Counter(g for g, _ in seq)
for g in pk['groups']:
    if not present[g]:
        errs.append(f'group vanished: {g}')
og = [o['group'] for o in d['order']]
if og != [g for g in pk['groups'] if g in og]:
    errs.append('order groups not in packet order')
print('final day size', len(keys_in_order))
for g in pk['groups']:
    print(f'  {present[g]}  {g}')
print('kept:', kept)
print('ERRORS:' if errs else 'ALL CHECKS PASSED', *errs, sep='\n')
