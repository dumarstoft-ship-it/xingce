# D01-math-h-v01  共享单车甲、乙两个停放点（下文a、b、A、B分别指甲、乙），两个“若……则……”
# 都是从现状出发的独立假设：若甲调35辆到乙，则乙是甲的3倍；若改为乙调40辆到甲，则甲是乙的2倍。
# 求甲点现有单车数。
OPTS = {'A': 45, 'B': 59, 'C': 80, 'D': 180}
X1, M1 = 35, 3   # 方案一：A→B 35辆，调后 B＝3×A
X2, M2 = 40, 2   # 方案二：B→A 40辆，调后 A＝2×B
N = 1500

# 穷举两点现有数量(a, b)，两个假设各自从“现有”出发，分别检验
sols = []
for a in range(0, N + 1):
    for b in range(0, N + 1):
        if a < X1 or b < X2:
            continue
        if b + X1 == M1 * (a - X1) and a + X2 == M2 * (b - X2):
            sols.append((a, b))
assert len(sols) == 1, sols
a, b = sols[0]
hits = [k for k, v in OPTS.items() if v == a]
assert len(hits) == 1, hits

# 干扰项来源核对
# (1) 误把两个假设当成先后发生：先甲→乙 35辆（乙＝3甲），再在此基础上乙→甲 40辆（甲＝2乙）
seq = []
for a0 in range(0, N + 1):
    for b0 in range(0, N + 1):
        a1, b1 = a0 - X1, b0 + X1
        if a1 < 0 or b1 != M1 * a1:
            continue
        a2, b2 = a1 + X2, b1 - X2
        if b2 >= 0 and a2 == M2 * b2:
            seq.append((a0, b0))
assert len(seq) == 1 and seq[0][0] == OPTS['B'], seq
assert a - X1 == OPTS['A']      # 算出第一种假设调后甲点的数量，忘了加回35
assert a + b == OPTS['D']       # 答成两点总数
print('A', a, 'B', b, 'total', a + b, '| sequential misread A', seq[0][0])
print(hits[0])
