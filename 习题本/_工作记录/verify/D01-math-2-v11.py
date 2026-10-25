# D01-math-2-v11 甲买5袋、乙买3袋、丙没买；丙拿出48元分给甲乙，使三人负担的米钱相同
from fractions import Fraction as Fr

opts = {'A': 30, 'B': 36, 'C': 42, 'D': 48}
bags = {'甲': 5, '乙': 3, '丙': 0}
pay_bing = 48

# 三人最终负担相同 => 每人负担 = 丙拿出的钱
each = Fr(pay_bing)
total_cost = each * 3
price = total_cost / sum(bags.values())          # 每袋米价
spent = {k: v * price for k, v in bags.items()}
back = {k: spent[k] - each for k in bags}        # 甲、乙应收回的钱
assert back['丙'] == -pay_bing
assert back['甲'] + back['乙'] == pay_bing and back['甲'] >= 0 and back['乙'] >= 0

# 另一条路：每人吃 8/3 袋，丙的钱只付给甲、乙"多出来"的部分
eat = Fr(sum(bags.values()), 3)
assert pay_bing == eat * price
surplus = {k: bags[k] - eat for k in ('甲', '乙')}
assert surplus['甲'] * price == back['甲'] and surplus['乙'] * price == back['乙']
ans = back['甲']

# 干扰项的错误路径
assert Fr(pay_bing * bags['甲'], bags['甲'] + bags['乙']) == opts['A']   # 按5:3分
assert (bags['甲'] - bags['乙']) * price == opts['B']                     # 甲比乙多买2袋折钱
assert pay_bing == opts['D']                                               # 以为钱全归甲

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('price per bag =', price, 'jia gets', back['甲'], 'yi gets', back['乙'])
print(hits[0])
