# D01-math-1-v10  龙舟队：去年女:男＝1:4；今年女队员增加10人、男队员减少4人，女:男＝1:2。求今年共有队员多少人。
OPTS = {'A': 44, 'B': 54, 'C': 60, 'D': 66}

def solve(male_change):
    out = []
    for f in range(1, 1001):          # 去年女队员人数
        m = 4 * f
        f2, m2 = f + 10, m + male_change
        if m2 > 0 and m2 == 2 * f2:
            out.append((f, m, f2, m2))
    return out

sols = solve(-4)
assert len(sols) == 1, sols
f, m, f2, m2 = sols[0]
total = f2 + m2
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits

# 干扰项来源核对
assert f + m == OPTS['C']                       # 答成去年总人数
bad = solve(+4)                                 # 把“减少4人”当成增加4人
assert len(bad) == 1 and bad[0][2] + bad[0][3] == OPTS['B']
assert m2 == OPTS['A']                          # 只算今年男队员
# 倍数特性：今年总数是3的倍数、去年总数（今年−6）是5的倍数，四个选项中只有一个满足
assert [k for k, v in OPTS.items() if v % 3 == 0 and (v - 6) % 5 == 0] == hits
print('last year', f, m, 'this year', f2, m2, 'total', total)
print(hits[0])
