# T218 余数方法演示例题（三小问），收入的是第(3)问：除以3余2、除以5余3、除以7余2、除以11余8的最小正整数。
# 同时核对原例(1)(2)两问的答案。
OPTS = {'A': 128, 'B': 233, 'C': 338, 'D': 443}


def smallest(conds):
    return next(n for n in range(1, 10 ** 6) if all(n % m == r for m, r in conds))


q1 = smallest([(3, 2), (5, 4), (7, 6)])
q2 = smallest([(3, 2), (5, 4), (7, 5)])
q3 = smallest([(3, 2), (5, 3), (7, 2), (11, 8)])
# 干扰项都满足前三个条件、只在"除以11余8"上出错
for k, v in OPTS.items():
    assert all(v % m == r for m, r in [(3, 2), (5, 3), (7, 2)]), k
hits = [k for k, v in OPTS.items() if v == q3]
assert len(hits) == 1, (q3, hits)
print('(1) =', q1, '(2) =', q2, '(3) =', q3)
print(hits[0])
