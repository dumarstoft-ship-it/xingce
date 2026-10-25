# teacher_T030  鸡兔同笼：头20个，足62只
OPTS = {'A': (8, 12), 'B': (9, 11), 'C': (10, 10), 'D': (11, 9)}     # (鸡, 兔)
sols = [(c, 20 - c) for c in range(0, 21) if 2 * c + 4 * (20 - c) == 62]
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['D'] == ans[::-1]            # 假设全是鸡算出的11只其实是兔，错当成鸡
print('鸡, 兔 =', ans)
print(hits[0])
