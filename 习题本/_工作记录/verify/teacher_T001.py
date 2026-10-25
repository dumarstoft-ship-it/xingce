# teacher_T001  网格最短路径：家在东北角、单位在西南角，只能向西或向南走（图：南北向街道5条、东西向街道4条）
from math import comb

V_STREETS, H_STREETS = 5, 4            # 南北向街道条数、东西向街道条数（见图）
W, S = V_STREETS - 1, H_STREETS - 1    # 需向西走的段数、向南走的段数
OPTS = {'A': 12, 'B': 35, 'C': 126, 'D': 128}

# 递推：到某路口的走法数 = 北邻路口走法数 + 东邻路口走法数（以家为原点，i 向西、j 向南）
f = [[0] * (S + 1) for _ in range(W + 1)]
for i in range(W + 1):
    for j in range(S + 1):
        f[i][j] = 1 if (i == 0 or j == 0) else f[i - 1][j] + f[i][j - 1]
ans = f[W][S]
assert ans == comb(W + S, S)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
# 干扰项来源
assert OPTS['A'] == W * S                                      # 西4段×南3段，乘法误用
assert OPTS['C'] == comb(V_STREETS + H_STREETS, H_STREETS)     # 把街道条数当段数：C(9,4)
assert OPTS['D'] == 2 ** (W + S)                               # 以为每步都有2种选择
print('paths =', ans)
print(hits[0])
