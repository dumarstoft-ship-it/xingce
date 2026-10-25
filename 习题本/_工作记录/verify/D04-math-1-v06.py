# D04-math-1-v06  甲店"打八折后再减30元"，乙店"先减50元再打九折"，标价>=100元才参加；
# 标价至少要超过多少元，在甲店买才比乙店便宜？（即：甲店更便宜 <=> 标价 > T，求 T）
# 以"分"为单位、全部乘10后用整数比较，避免浮点误差。


def jia10(pc):  # pc: 标价（分），返回 10*实付（分）
    return 8 * pc - 30000 if pc >= 10000 else 10 * pc


def yi10(pc):
    return 9 * (pc - 5000) if pc >= 10000 else 10 * pc


def yi10_wrong(pc):  # 漏乘0.9：0.9p-50
    return 9 * pc - 50000 if pc >= 10000 else 10 * pc


def jia10_wrong(pc):  # 甲店读成先减30再打八折
    return 8 * (pc - 3000) if pc >= 10000 else 10 * pc


GRID = range(0, 500001)  # 0~5000元，步长0.01元
cheaper = [jia10(pc) < yi10(pc) for pc in GRID]

OPTS = {'A': 100, 'B': 150, 'C': 200, 'D': 210}


def is_threshold(T, flags):
    t = T * 100
    return all(flags[pc] == (pc > t) for pc in GRID)


hits = [L for L, v in OPTS.items() if is_threshold(v, cheaper)]
assert len(hits) == 1, hits

# 干扰项来源核对
assert is_threshold(OPTS['C'], [jia10(pc) < yi10_wrong(pc) for pc in GRID])
assert is_threshold(OPTS['D'], [jia10_wrong(pc) < yi10(pc) for pc in GRID])
assert jia10(15000) == yi10(15000) == 10 * 9000   # 标价150元时两店都付90元（9000分）

print(hits[0])
