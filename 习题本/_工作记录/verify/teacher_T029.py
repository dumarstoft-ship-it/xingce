# teacher_T029  2021国考-64：每家送10箱口罩7箱防护服，剩余口罩比防护服多20箱；每家送12口罩8防护服，缺8箱口罩11箱防护服。
#               按口罩:防护服=2:1、每家数量相同且无剩余，至少还要采购多少箱
OPTS = {'A': 54, 'B': 63, 'C': 75, 'D': 87}
sols = []
for n in range(1, 200):                      # 医院数
    M, S = 12 * n - 8, 8 * n - 11            # 口罩、防护服总箱数（由方案二）
    if S < 0:
        continue
    if (M - 10 * n) - (S - 7 * n) == 20:
        sols.append((n, M, S))
assert len(sols) == 1, sols
n, M, S = sols[0]
k = next(k for k in range(1, 1000) if 2 * k * n >= M and k * n >= S)   # 每家 2k 箱口罩、k 箱防护服
ans = 3 * k * n - M - S
hits = [key for key, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('医院', n, '口罩', M, '防护服', S, '每家', 2 * k, k, '采购', ans)
print(hits[0])
