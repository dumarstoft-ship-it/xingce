# T221（2023湖北选调）某天学习天数为200多天且是3的倍数，第二天的天数是5的倍数，第三天的天数是7的倍数。
# 问第几天（把这一天记为第1天）的天数是13的倍数。
OPTS = {'A': 9, 'B': 10, 'C': 11, 'D': 12}
xs = [x for x in range(200, 300) if x % 3 == 0 and (x + 1) % 5 == 0 and (x + 2) % 7 == 0]
assert len(xs) == 1, xs
x = xs[0]
k = next(k for k in range(1, 100) if (x + k - 1) % 13 == 0)     # 第k天的天数为 x+k-1
hits = [kk for kk, v in OPTS.items() if v == k]
assert len(hits) == 1, (k, hits)
print('day count =', x, 'k =', k, 'value =', x + k - 1)
print(hits[0])
