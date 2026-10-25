# D05-math-2-v04：方格网中 A=(0,0) 到 B=(4,3)，只能向东(+x)或向北(+y)走，路口 P=(2,1) 施工不能通过。
# 深度优先搜索枚举所有走法，遇到 P 就剪掉。
OPTIONS = {'A': 17, 'B': 18, 'C': 26, 'D': 35}

B = (4, 3)
P = (2, 1)


def walks(x, y):
    if (x, y) == P:
        return 0
    if (x, y) == B:
        return 1
    total = 0
    if x < B[0]:
        total += walks(x + 1, y)   # 向东一段
    if y < B[1]:
        total += walks(x, y + 1)   # 向北一段
    return total


count = walks(0, 0)
hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('count =', count)
print(hits[0])
