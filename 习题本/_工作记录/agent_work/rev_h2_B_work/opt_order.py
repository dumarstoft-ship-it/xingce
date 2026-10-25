import json, re, sys
d = json.load(open(sys.argv[1]))
tot = asc = desc = other = 0
others = []
for it in d:
    if it.get('section') and '数量' not in str(it.get('section')) and '数学' not in str(it.get('section')):
        continue
    t = it.get('text') or ''
    m = re.search(r'A[\.．、]\s*(\S+)\s+B[\.．、]\s*(\S+)\s+C[\.．、]\s*(\S+)\s+D[\.．、]\s*(\S+)', t)
    if not m:
        continue
    vals = []
    ok = True
    for g in m.groups():
        g2 = g.replace('%', '').replace('，', '').replace(',', '')
        if re.fullmatch(r'-?\d+(\.\d+)?', g2):
            vals.append(float(g2))
        else:
            ok = False
            break
    if not ok:
        continue
    tot += 1
    if vals == sorted(vals):
        asc += 1
    elif vals == sorted(vals, reverse=True):
        desc += 1
    else:
        other += 1
        others.append((it['id'], m.groups()))
print('numeric 4-option sets:', tot, 'ascending', asc, 'descending', desc, 'unsorted', other)
for o in others[:15]:
    print('  ', o)
