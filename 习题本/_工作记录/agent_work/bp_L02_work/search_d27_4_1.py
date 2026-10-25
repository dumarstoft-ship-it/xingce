import itertools, random
P = ['甲', '乙', '丙', '丁']
pairs = [frozenset(c) for c in itertools.combinations(P, 2)]


def single(x): return (f'{x}入选', lambda S: x in S)
def orr(x, y): return (f'{x}、{y}至少一人入选', lambda S: x in S or y in S)
def nor(x, y): return (f'{x}、{y}都没有入选', lambda S: x not in S and y not in S)
def imp(x, y): return (f'如果{x}入选，那么{y}也入选', lambda S: (x not in S) or (y in S))


res = []
for a in P:
    for (b, c) in itertools.permutations(P, 2):
        for (d, e) in itertools.combinations(P, 2):
            for (f, g) in itertools.permutations(P, 2):
                st = [single(a), orr(b, c), nor(d, e), imp(f, g)]
                counts = {S: sum(fn(S) for _, fn in st) for S in pairs}
                valid = [S for S in pairs if counts[S] == 2]
                if len(valid) != 1:
                    continue
                ans = valid[0]
                if ans in (frozenset(['乙', '丁']), frozenset(['甲', '丁'])):
                    continue
                contra = any(all(st[i][1](S) != st[j][1](S) for S in pairs) for i in range(4) for j in range(i + 1, 4))
                if contra:
                    continue
                res.append((''.join(sorted(ans)), [s for s, _ in st], {''.join(sorted(S)): counts[S] for S in pairs}))
print(len(res))
random.seed(1)
for r in random.sample(res, min(25, len(res))):
    print(r)
