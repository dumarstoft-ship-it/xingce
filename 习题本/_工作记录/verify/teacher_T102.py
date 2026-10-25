# T102 2016国考：10名英、法、日文编辑，小李会英、日文且是唯一会一种以上外语的人；会法文比会英文多4人，是会日文的2倍；求只会英文
OPTS = {'A': 2, 'B': 0, 'C': 3, 'D': 1}

sols = set()
for li_french in (0, 1):                  # 小李是否也会法文（题目未说明，两种都枚举）
    for e in range(0, 10):                # 只会英文
        for f in range(0, 10):            # 只会法文
            j = 9 - e - f                 # 只会日文（其余9人都只会一种）
            if j < 0:
                continue
            E, Fr, J = e + 1, f + li_french, j + 1
            if Fr == E + 4 and Fr == 2 * J:
                sols.add((li_french, e, f, j))
assert len({s[1] for s in sols}) == 1, sols
e = next(iter(sols))[1]
print('solutions (li_french, only_E, only_F, only_J):', sols)
print([k for k, v in OPTS.items() if v == e][0])
