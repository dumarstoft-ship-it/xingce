# teacher_T025  行数固定：每行7人余2人；每行8人则有一行少4人。共有多少人
OPTS = {'A': 42, 'B': 44, 'C': 48, 'D': 50}
sols = [(r, 7 * r + 2) for r in range(1, 200) if 7 * r + 2 == 8 * r - 4]
assert len(sols) == 1, sols
rows, total = sols[0]
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, (total, hits)
assert OPTS['A'] == 7 * rows            # 漏加余下的2人
assert OPTS['C'] == 8 * rows            # 漏减少的4人
print('行数 =', rows, ' 总人数 =', total)
print(hits[0])
