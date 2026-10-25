# teacher_T032  2024国考-67：甲30、乙24、丙20元/包；共240包、6000元；甲销量是乙2倍。丙卖了多少包
OPTS = {'A': 90, 'B': 75, 'C': 60, 'D': 45}
sols = []
for y in range(0, 241):
    j = 2 * y
    b = 240 - j - y
    if b < 0:
        continue
    if 30 * j + 24 * y + 20 * b == 6000:
        sols.append((j, y, b))
assert len(sols) == 1, sols
ans = sols[0][2]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('甲乙丙 =', sols[0])
print(hits[0])
