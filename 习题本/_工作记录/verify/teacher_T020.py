# teacher_T020  志愿者不到100人，男:女=11:7；补招女志愿者后变4:3。最多补招多少名女志愿者
OPTS = {'A': 5, 'B': 10, 'C': 15, 'D': 20}
added = []
for k in range(1, 100):
    male, female = 11 * k, 7 * k
    if male + female >= 100:
        continue
    for f in range(1, 200):
        if 3 * male == 4 * (female + f):
            added.append(f)
assert added, added
ans = max(added)
hits = [key for key, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
# 忽略"不到100人"时取男生88人得10
assert OPTS['B'] == next(f for f in range(1, 200) if 3 * 88 == 4 * (56 + f))
print('可能的补招人数 =', added)
print(hits[0])
