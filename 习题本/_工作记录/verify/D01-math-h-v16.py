# D01-math-h-v16 第一次4支毛笔、7刀宣纸、1瓶墨汁共190元；第二次5支毛笔、9刀宣纸、1瓶墨汁共240元；
# 求毛笔、宣纸、墨汁各1件共多少元。
# 独立求解：①按0.5元精度枚举所有正单价组合，确认"各1件"的总价只有一个值；
# ②用分数精确求出组合系数 α、β，使 α·第一式+β·第二式＝(1,1,1)，交叉验证；再复核干扰项的错误路径。
from fractions import Fraction as Fr

OPTS = {'A': 40, 'B': 50, 'C': 90, 'D': 140}
E1 = (4, 7, 1, 190)
E2 = (5, 9, 1, 240)

# ① 枚举（单位：0.5元）
sums = set()
count = 0
for p2 in range(1, 2 * 190):
    for n2 in range(1, 2 * 190):
        p, n = Fr(p2, 2), Fr(n2, 2)
        f = E1[3] - E1[0] * p - E1[1] * n
        if f <= 0: break
        if E2[0] * p + E2[1] * n + E2[2] * f != E2[3]: continue
        sums.add(p + n + f)
        count += 1
assert count > 1 and len(sums) == 1, (count, sums)      # 单价不唯一，但"各1件"唯一
ans = sums.pop()

# ② α·E1 + β·E2 = (1,1,1)：由毛笔、墨汁两列解出 α、β，再检验宣纸列
#    4α+5β=1, α+β=1  →  α=4, β=-3
beta = Fr(1 - E1[0], E2[0] - E1[0])
alpha = 1 - beta
assert all(alpha * E1[i] + beta * E2[i] == 1 for i in range(3))
assert alpha * E1[3] + beta * E2[3] == ans

# 干扰项的错误路径
diff = E2[3] - E1[3]                       # 两式相减：1支毛笔+2刀宣纸
assert diff == OPTS['B']                   # 把差额当答案
assert E1[3] - diff == OPTS['D']           # 只减一次差
assert E2[3] - 3 * diff == OPTS['C']       # 用第二次的总价减3倍差（倍数配错）

hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print('price combos found:', count, 'sum =', ans, 'alpha,beta =', alpha, beta)
print(hits[0])
