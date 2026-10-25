# D04-math-h-v18：超市引进 1500 盒新款月饼，定价 60 元/盒。
# 买断：进价 24 元/盒，卖不完的最多 300 盒可按 12 元/盒退给厂家，其余不能退；
# 代销：进价 30 元/盒，卖不完的按进价全部退回。求：选买断的利润不低于代销时，至少要卖出多少盒。
# 独立求解：逐一枚举卖出盒数 k（0～1500），按“可退盒数 = min(300, 剩余盒数)”计算买断利润，
# 与代销利润比较，找出买断不吃亏的最小 k；同时检查 k 以上全部成立（两段都覆盖），再与选项比对。

N, PRICE = 1500, 60
BUYOUT_COST, RETURN_CAP, RETURN_PRICE = 24, 300, 12
CONSIGN_COST = 30

OPTIONS = {'A': 1080, 'B': 420, 'C': 540, 'D': 1000}   # 轮转升序排列


def profit_buyout(k):
    left = N - k
    return PRICE * k - BUYOUT_COST * N + RETURN_PRICE * min(RETURN_CAP, left)


def profit_consign(k):
    return PRICE * k - CONSIGN_COST * N + CONSIGN_COST * (N - k)   # 剩余月饼按进价退回


ok = [k for k in range(N + 1) if profit_buyout(k) >= profit_consign(k)]
kmin = min(ok)
assert ok == list(range(kmin, N + 1)), 'solution set should be k >= kmin'
print('至少卖出', kmin, '盒，此时剩余', N - kmin, '盒；买断利润', profit_buyout(kmin), '代销利润', profit_consign(kmin))
print('剩余不足 300 盒的一段（k>1200）是否全部成立：', all(profit_buyout(k) >= profit_consign(k) for k in range(1201, N + 1)))
for k, v in OPTIONS.items():
    print(k, v, '买断', profit_buyout(v), '代销', profit_consign(v))

hits = [k for k, v in OPTIONS.items() if v == kmin]
assert len(hits) == 1, hits
print(hits[0])
