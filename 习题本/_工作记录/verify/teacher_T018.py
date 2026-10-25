# teacher_T018  某天学习天数为200多且是3的倍数，第二天是5的倍数，第三天是7的倍数。第几天的天数是13的倍数
OPTS = {'A': 8, 'B': 9, 'C': 10, 'D': 11}
cands = [n for n in range(200, 300) if n % 3 == 0 and (n + 1) % 5 == 0 and (n + 2) % 7 == 0]
assert len(cands) == 1, cands
n = cands[0]
k = next(k for k in range(1, 100) if (n + k - 1) % 13 == 0)     # 第k天的天数为 n+k-1
hits = [key for key, v in OPTS.items() if v == k]
assert len(hits) == 1, (k, hits)
assert OPTS['B'] == k - 1                    # 把"相差几天"当成"第几天"
print('第1天 =', n, ' 第', k, '天 =', n + k - 1)
print(hits[0])
