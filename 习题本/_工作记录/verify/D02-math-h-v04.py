# D02-math-h-v04  1艘清淤船需300天；第1~5天1艘，第6~10天2艘，第11~15天3艘……每5天增加1艘，直到完工。
# 求第几天完工。
import math

OPTS = {'A': 50, 'B': 52, 'C': 53, 'D': 55}
W, K = 300, 5     # 总量（艘·天）、每段天数


def boats(day):
    return (day - 1) // K + 1


def cum(day):
    return sum(boats(d) for d in range(1, day + 1))


# 逐天累加，找第一次累计 >= W 的那一天
day = 0
while cum(day) < W:
    day += 1


def finishes_on(d):
    return d >= 1 and cum(d - 1) < W <= cum(d)


hits = [k for k, v in OPTS.items() if finishes_on(v)]
assert len(hits) == 1 and OPTS[hits[0]] == day, (hits, day)

# ---- 干扰项来源核对 ----
m = max(j for j in range(0, 100) if K * j * (j + 1) // 2 <= W)     # 完整的段数
rest = W - K * m * (m + 1) // 2
assert (m, rest) == (10, 25)
assert K * (m + 1) == OPTS['D']                      # 凑满第11段
assert K * m + rest // (m + 1) == OPTS['B']          # 零头 25/11≈2.3 天只算 2 天
assert K * m == OPTS['A']                            # 停在第10段末
assert K * m + math.ceil(rest / (m + 1)) == day

print('finish day', day)
print(hits[0])
