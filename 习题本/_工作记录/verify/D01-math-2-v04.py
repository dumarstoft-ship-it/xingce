# D01-math-2-v04 每间45人有30人没座位；每间50人恰好空出一间、其余坐满
opts = {'A': 300, 'B': 720, 'C': 750, 'D': 800}
s1, short = 45, 30
s2 = 50

sols = []
for n in range(2, 5001):                       # 培训室间数
    people = s1 * n + short                    # 方案一：n间坐满还有30人没座位
    if people == s2 * (n - 1):                 # 方案二：n-1间正好坐满，空出一间
        sols.append((n, people))
assert len(sols) == 1, sols
n, people = sols[0]

# 干扰项的错误路径
n_ignore = [k for k in range(1, 5001) if s1 * k + short == s2 * k]   # 忽略"空出一间"
assert len(n_ignore) == 1 and s2 * n_ignore[0] == opts['A']
assert s1 * n == opts['B']          # 漏加没座位的30人
assert s2 * n == opts['D']          # 求对间数后按n间×50计算

hits = [k for k, v in opts.items() if v == people]
assert len(hits) == 1, hits
print('rooms =', n, 'people =', people)
print(hits[0])
