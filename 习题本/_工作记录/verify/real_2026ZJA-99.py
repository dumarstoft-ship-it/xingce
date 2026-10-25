# real 2026ZJA-99  诗句中两件事的逻辑关系，与"龙城飞将在"和"胡马度阴山"一致的是？
# 把每对 (X, Y) 的关系表示为允许出现的真值组合集合，再比较。
from itertools import product

def rel(f):
    return frozenset((x, y) for x, y in product([True, False], repeat=2) if f(x, y))

def imp(a, b):
    return (not a) or b

# 题干：但使龙城飞将在(X)，不教胡马度阴山(Y)：X → ¬Y
STEM = rel(lambda x, y: imp(x, not y))

# 每个选项可列出多种合理译法，任何一种译法都不能与题干相同才算排除
OPTS = {
    # 不破楼兰(¬X)终不还(¬Y)：¬X → ¬Y
    'A': [rel(lambda x, y: imp(not x, not y))],
    # 清如许(X)，为有源头活水来(Y)：Y → X（因果/充分），或读作 X → Y（必要）
    'B': [rel(lambda x, y: imp(y, x)), rel(lambda x, y: imp(x, y))],
    # 浮云遮望眼(X)，身在最高层(Y)：身在最高层，浮云就遮不住望眼：Y → ¬X
    'C': [rel(lambda x, y: imp(y, not x))],
    # 若非群玉山头见(¬X)，会向瑶台月下逢(Y)：¬X → Y
    'D': [rel(lambda x, y: imp(not x, y))],
}

def same(r1, r2):
    swapped = frozenset((y, x) for x, y in r2)
    return r1 == r2 or r1 == swapped

print('题干允许的组合', sorted(STEM), '→ 两者不能同真、可以同假')
hits = [k for k, rs in OPTS.items() if any(same(STEM, r) for r in rs)]
assert len(hits) == 1, hits
print(hits[0])
