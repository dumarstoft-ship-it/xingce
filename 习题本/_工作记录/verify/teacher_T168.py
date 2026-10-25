# teacher T168（2019青海）四基地每隔2、4、6、7天采购一次，7月1日都去了，7月有几天不用去
OPTS = {'A': 10, 'B': 11, 'C': 12, 'D': 13}
GAPS = {'甲': 2, '乙': 4, '丙': 6, '丁': 7}          # 每隔n天 -> 每(n+1)天去一次
DAYS = 31
visit = set()
for g in GAPS.values():
    visit |= set(range(1, DAYS + 1, g + 1))
free = DAYS - len(visit)
wrong = DAYS - len(set().union(*[set(range(1, DAYS + 1, g)) for g in GAPS.values()]))
print('要去的日子', sorted(visit), '| 不用去', free, '| 误把“每隔n天”当周期n:', wrong)
hits = [k for k, v in OPTS.items() if v == free]
assert len(hits) == 1, hits
print(hits[0])
