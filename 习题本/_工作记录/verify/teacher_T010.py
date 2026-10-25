# teacher_T010  红:白=3:4，放入3个红球后变6:7，求原本红、白球数
OPTS = {'A': (3, 4), 'B': (18, 24), 'C': (21, 28), 'D': (24, 28)}
ADD = 3
sols = [(r, w) for r in range(1, 500) for w in range(1, 500)
        if 4 * r == 3 * w and 7 * (r + ADD) == 6 * w]
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['D'] == (ans[0] + ADD, ans[1])    # 答成放入后的数量
print('红, 白 =', ans)
print(hits[0])
