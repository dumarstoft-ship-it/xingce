# D04-math-1-v07  售价<=6000元的手机补贴15%、每件最高500元；>6000元不补贴；
# 实付不超过5600元，能选购的手机售价最高为多少？
# 以"分"为单位、全部乘100后用整数比较。

LIMIT = 600000       # 6000元（分）
CAP = 50000          # 500元（分）
BUDGET = 560000      # 5600元（分）


def pay100(pc):
    """100*实付（分）"""
    if pc <= LIMIT:
        return 100 * pc - min(15 * pc, 100 * CAP)
    return 100 * pc


GRID = range(0, 1000001)  # 0~10000元，步长0.01元
feasible = [pc for pc in GRID if pay100(pc) <= 100 * BUDGET]
best = max(feasible)

OPTS = {'A': 5600, 'B': 6000, 'C': 6100, 'D': 6588}
hits = [L for L, v in OPTS.items() if v * 100 == best]
assert len(hits) == 1, hits

# 干扰项来源核对
no_limit = max(pc for pc in GRID if 100 * pc - min(15 * pc, 100 * CAP) <= 100 * BUDGET)
assert no_limit == OPTS['C'] * 100                       # 忽略6000元上限
no_cap = max(pc for pc in GRID if 85 * pc <= 100 * BUDGET)
assert no_cap // 100 == OPTS['D']                        # 忽略封顶与上限，约6588元
assert pay100(600000) == 100 * 550000 and pay100(610000) == 100 * 610000  # 断崖：5500 vs 6100

print('best price (yuan)', best / 100)
print(hits[0])
