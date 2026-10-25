"""Week 1 at 20 math questions a day: split each day's 45 (already 去水, ordered by 考法 group, easy -> hard) into
round 1 (20, this week) and the rest, deferred to the module's next round (db/math_deferred.json).
Every 考法 group keeps at least one question this week; the other slots go to the larger groups. Both rounds keep
the day's mix of real (incl. teacher) questions and new variants, and inside a group the picks are spread over
its difficulty range."""
import json, sys, collections
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
PER_DAY = 20

def key(it): return it.get('id') or it.get('tid') or it.get('vid')

def split(items, n=PER_DAY):
    groups = collections.OrderedDict()
    for it in items: groups.setdefault(it['group'], []).append(it)
    quota = {g: 1 for g in groups}
    extra = n - len(groups)
    if extra < 0: raise SystemExit('more groups than slots')
    rest = {g: len(v) - 1 for g, v in groups.items()}
    tot = sum(rest.values())
    share = {g: extra * r / tot for g, r in rest.items()} if tot else {}
    for g in groups: quota[g] += int(share.get(g, 0))
    left = n - sum(quota.values())
    for g in sorted(groups, key=lambda g: -(share.get(g, 0) - int(share.get(g, 0))))[:left]: quota[g] += 1
    # keep the day's real/variant mix in both rounds: real (and teacher) questions set the examiner's style,
    # the new variants deepen the same 考法; split the day's variant slots over the groups that have variants
    nvar = sum(1 for it in items if it['type'] == 'variant')
    vslots = round(n * nvar / len(items))
    vq = {g: 0 for g in groups}
    cap = {g: min(quota[g], sum(1 for it in v if it['type'] == 'variant')) for g, v in groups.items()}
    while vslots > 0 and any(vq[g] < cap[g] for g in groups):
        g = max((g for g in groups if vq[g] < cap[g]),
                key=lambda g: (sum(1 for it in groups[g] if it['type'] == 'variant') / (vq[g] + 1), -list(groups).index(g)))
        vq[g] += 1; vslots -= 1
    keep = []
    for g, v in groups.items():
        k = min(quota[g], len(v))
        base = [it for it in v if it['type'] != 'variant']; var = [it for it in v if it['type'] == 'variant']
        kv = min(vq[g], len(var)); kb = min(k - kv, len(base)); kv = k - kb  # a group short of one type takes the other
        pick = spread(base, kb) + spread(var, kv)
        keep += [key(it) for it in v if it in pick]
    return keep

def spread(v, k):
    if k <= 0: return []
    m = len(v)
    return [v[p] for p in sorted({int(i * m / k + m / (2 * k)) for i in range(k)})]

if __name__ == '__main__':
    sched = json.load(open(S + '/db/schedule.json'))['schedule']
    hd = json.load(open(S + '/db/math_harden.json'))
    deferred = {}
    for d in range(1, 8):
        items = json.load(open(f'{S}/out/final/D{d}.json'))['parts'][0]['items']
        keep = split(items)
        hd[str(d)]['round1'] = keep
        mod = sched[d - 1]['math']
        deferred.setdefault(mod, []).extend([{'key': key(it), 'type': it['type'], 'group': it['group'], 'from_day': d} for it in items if key(it) not in keep])
        print(d, mod, len(keep), 'deferred', len(items) - len(keep))
    json.dump(hd, open(S + '/db/math_harden.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(deferred, open(S + '/db/math_deferred.json', 'w'), ensure_ascii=False, indent=1)
