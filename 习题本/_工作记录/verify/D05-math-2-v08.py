# D05-math-2-v08：8 支龙舟队两两对阵（4 场，不计场次先后），广州队与深圳队首轮不相遇。
# 枚举 8 队的全部排列，相邻两两成对，转成"无序对的集合"去重，得到全部对阵情况，再筛选。
from itertools import permutations

OPTIONS = {'A': 15, 'B': 75, 'C': 90, 'D': 105}

teams = ['广州', '深圳', '佛山', '东莞', '珠海', '中山', '江门', '肇庆']
draws = set()
for order in permutations(teams):
    draw = frozenset(frozenset(order[i:i + 2]) for i in range(0, 8, 2))
    draws.add(draw)

bad_pair = frozenset(['广州', '深圳'])
count = sum(1 for d in draws if bad_pair not in d)

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('all draws =', len(draws), 'valid =', count)
print(hits[0])
