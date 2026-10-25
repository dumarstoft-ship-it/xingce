import sys; sys.path.insert(0, '..')
from lib import *
# 8人圆桌（0..7 俯视顺时针；面向圆心时 左手边=+1），男：甲乙丙丁；女：A B C D（分别为甲乙丙丁的妻子）
M = ['甲', '乙', '丙', '丁']; F = ['A', 'B', 'C', 'D']
sols = []
for pm in permutations([2, 4, 6]):                 # 男在偶数位，甲固定0
    for pf in permutations([1, 3, 5, 7]):
        st = dict(zip(M, (0,) + pm)); st.update(dict(zip(F, pf)))
        if any((st[f] - st[m]) % 8 in (1, 7) for m, f in zip(M, F)): continue   # 夫妻不相邻
        if st['B'] != (st['甲'] + 1) % 8: continue    # 甲的左手边是乙的妻子
        if (st['丙'] - st['甲']) % 8 != 4: continue    # 丙坐在甲的对面
        sols.append(st)
at = lambda st, i: {v: k for k, v in st.items()}[i % 8]
print('解数', len(sols))
for s in sols: print([at(s, i) for i in range(8)])
cands = {
    '丁的妻子坐在甲的右手边': lambda s: at(s, s['甲'] - 1) == 'D',
    '甲的妻子与乙相邻': lambda s: (s['A'] - s['乙']) % 8 in (1, 7),
    '丙的妻子坐在丁的对面': lambda s: (s['C'] - s['丁']) % 8 == 4,
    '乙坐在丁的左手边第二个位置': lambda s: s['乙'] == (s['丁'] + 2) % 8,
    '丁坐在甲的左手边第二个位置': lambda s: s['丁'] == (s['甲'] + 2) % 8,
    '甲的妻子坐在丙的左手边': lambda s: s['A'] == (s['丙'] + 1) % 8,
    '丁的妻子坐在丙的左手边': lambda s: s['D'] == (s['丙'] + 1) % 8,
    '乙的妻子与丙的妻子相对': lambda s: (s['B'] - s['C']) % 8 == 4,
}
for k, f in cands.items():
    print(k, sum(f(s) for s in sols), '/', len(sols))
