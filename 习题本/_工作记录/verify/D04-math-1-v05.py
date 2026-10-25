# D04-math-1-v05  能效补贴封顶：一级25%最高2000元，二级10%最高800元；
# 甲款一级、标价12500元打八折；乙款二级、标价10000元打八五折
from fractions import Fraction as F

RULES = {'一级': (F(25, 100), 2000), '二级': (F(10, 100), 800)}
ITEMS = {'甲': ('一级', 12500, F(80, 100)), '乙': ('二级', 10000, F(85, 100))}


def pay(item, cap=True):
    level, tag, disc = ITEMS[item]
    final = tag * disc
    rate, top = RULES[level]
    sub = min(final * rate, top) if cap else final * rate
    return final - sub


pj, py = pay('甲'), pay('乙')
# 选项：(更便宜的款, 少付金额)
OPTS = {'A': ('甲', 150), 'B': ('甲', 200), 'C': ('乙', 300), 'D': ('乙', 350)}


def holds(o, j, y):
    who, x = o
    return (y - j == x) if who == '甲' else (j - y == x)


hits = [L for L, o in OPTS.items() if holds(o, pj, py)]
assert len(hits) == 1, hits

# 干扰项来源核对
assert holds(OPTS['A'], pay('甲', False), pay('乙', False))   # 都忽略封顶
assert holds(OPTS['D'], pay('甲', True), pay('乙', False))    # 只对甲款封顶
assert holds(OPTS['B'], pay('甲', False), pay('乙', True))    # 只对乙款封顶
# 两档封顶对应的最终售价门槛都是8000元，两款最终售价都超过它
assert all(top / rate == 8000 for rate, top in RULES.values())
assert all(tag * disc > 8000 for _, tag, disc in ITEMS.values())

print('pay 甲', pj, 'pay 乙', py)
print(hits[0])
