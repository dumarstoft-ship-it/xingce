# D01-math-2-v05 甲中心比乙中心多840剂疫苗，甲调给乙若干后乙反而比甲多160剂
opts = {'A': 340, 'B': 500, 'C': 680, 'D': 1000}
total, d_before, d_after = 3600, 840, 160

pairs = [(j, total - j) for j in range(total + 1) if j - (total - j) == d_before]
assert len(pairs) == 1
jia, yi = pairs[0]

sols = [m for m in range(1, jia + 1) if (yi + m) - (jia - m) == d_after]
assert len(sols) == 1, sols
m = sols[0]

# 干扰项的错误路径
assert d_before + d_after == opts['D']            # 忘了除以2
assert d_before - d_after == opts['C']            # 没看出"反超"
assert (d_before - d_after) // 2 == opts['A']     # 没看出"反超"且除以2

hits = [k for k, v in opts.items() if v == m]
assert len(hits) == 1, hits
print('jia, yi =', jia, yi, 'moved =', m, 'after:', jia - m, yi + m)
print(hits[0])
