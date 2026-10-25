# T185（2023浙江C）80张抽奖券，20个不同数字各出现4次，每个数字对应一种礼品；每人抽1次。
# 最少多少人参加才能保证至少有3人领取的礼品相同。
KINDS, COPIES, NEED = 20, 4, 3
OPTS = {'A': 41, 'B': 42, 'C': 61, 'D': 62}
# 最不利：每种礼品最多被领 min(COPIES, NEED-1) 次而仍无3人相同
worst = sum(min(COPIES, NEED - 1) for _ in range(KINDS))
ans = worst + 1
assert ans <= KINDS * COPIES
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('worst case without 3 same =', worst)
print(hits[0])
