# T113 2023陕西：8歼击机选3、3预警机选2、2反潜机选1，逐架起飞；3架歼击机必须相邻，2架预警机不能相邻
from itertools import combinations, permutations

FIGHTERS = [('F', i) for i in range(8)]
AEW = [('E', i) for i in range(3)]
ASW = [('S', i) for i in range(2)]
OPTS = {'A': 504, 'B': 4032, 'C': 8064, 'D': 24192}

def valid(seq):
    fpos = [i for i, x in enumerate(seq) if x[0] == 'F']
    epos = [i for i, x in enumerate(seq) if x[0] == 'E']
    return fpos[-1] - fpos[0] == 2 and abs(epos[0] - epos[1]) != 1

cnt = 0
for f in combinations(FIGHTERS, 3):
    for e in combinations(AEW, 2):
        for s in combinations(ASW, 1):
            planes = f + e + s
            cnt += sum(1 for seq in permutations(planes) if valid(seq))
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('ways =', cnt)
print(hits[0])
