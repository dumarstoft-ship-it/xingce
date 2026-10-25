# D01-math-1-v11  招聘会三个分会场：原有人数4:7:11；各新进场相同人数（无人离场）后A:B＝2:3；
# 再从C引导30人到A，A、B相等。求此时C分会场人数。
OPTS = {'A': 100, 'B': 110, 'C': 130, 'D': 160}
MOVE = 30

sols = []
for k in range(1, 301):               # 原有人数为4k、7k、11k
    a, b, c = 4 * k, 7 * k, 11 * k
    for y in range(0, 2001):          # 每个分会场新进场人数
        A, B, C = a + y, b + y, c + y
        if 3 * A != 2 * B:
            continue
        if A + MOVE == B and C - MOVE >= 0:
            sols.append((k, y, A + MOVE, B, C - MOVE))
assert len(sols) == 1, sols
k, y, A_fin, B_fin, C_fin = sols[0]
hits = [kk for kk, v in OPTS.items() if v == C_fin]
assert len(hits) == 1, hits

# 干扰项来源核对
assert C_fin + MOVE == OPTS['C']                # 忘了转出的30人
assert 11 * k == OPTS['B']                      # 答成C分会场原有人数
assert C_fin + 2 * MOVE == OPTS['D']            # 转移方向弄反（C反而多了30人）
print('k', k, 'each added', y, 'final A B C', A_fin, B_fin, C_fin)
print(hits[0])
