# D04-math-2-v07 停车费：正推张先生费用，再反推李女士最长时长（按秒枚举）
import math
def fee(sec):
    if sec <= 15 * 60:
        return 0
    f = 6
    if sec > 3600:
        f += 3 * math.ceil((sec - 3600) / 1800)
    return f
zhang = fee((2 * 60 + 40) * 60)
target = zhang + 6
ok = [s for s in range(0, 10 * 3600 + 1) if fee(s) == target]
tmax = max(ok)
assert fee(tmax + 1) != target
print('zhang fee =', zhang, 'li fee =', target, 'li range(min) =', (min(ok) - 1) / 60, '~', tmax / 60)
options = {'A': 3 * 60 + 40, 'B': 4 * 60, 'C': 4 * 60 + 30, 'D': 5 * 60}   # 分钟
hits = [k for k, v in options.items() if v * 60 == tmax]
assert len(hits) == 1, hits
print({k: fee(v * 60) for k, v in options.items()})
print(hits[0])
