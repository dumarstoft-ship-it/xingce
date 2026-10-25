# teacher T150（2015上海B）16排座位，首排16座、每排多1座，考生两两不能相邻，最多容纳几人
OPTS = {'A': 188, 'B': 192, 'C': 196, 'D': 200}
ROWS, FIRST = 16, 16

def max_nonadjacent(s):
    """一排s个座位最多坐几人（两两不相邻），动态规划"""
    take, skip = 0, 0
    for _ in range(s):
        take, skip = skip + 1, max(take, skip)
    return max(take, skip)

per_row = [max_nonadjacent(FIRST + i) for i in range(ROWS)]
total = sum(per_row)
print(per_row, total, '| 总座位/2 =', sum(FIRST + i for i in range(ROWS)) // 2)
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits
print(hits[0])
