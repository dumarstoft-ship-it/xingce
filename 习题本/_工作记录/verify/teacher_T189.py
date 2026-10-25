# T189（2010浙江A）1600人，喜欢四项球类分别1180、1360、1250、1040人，四项都喜欢的至少几人。
# 下界：不喜欢各项的人至多互不重叠覆盖，四项都喜欢 >= 总数-各反面之和；再给出达到下界的具体构造并逐人核验。
TOTAL, LIKES = 1600, [1180, 1360, 1250, 1040]
OPTS = {'A': 20, 'B': 30, 'C': 40, 'D': 50}
bound = max(0, TOTAL - sum(TOTAL - x for x in LIKES))
# 构造：把各项"不喜欢"的人依次排在互不重叠的编号段上
dislike, start = [], 0
for x in LIKES:
    n = TOTAL - x
    dislike.append(set(range(start, start + n)))
    start += n
assert start <= TOTAL
for i, x in enumerate(LIKES):
    assert TOTAL - len(dislike[i]) == x
all_four = sum(1 for p in range(TOTAL) if all(p not in d for d in dislike))
assert all_four == bound
hits = [k for k, v in OPTS.items() if v == all_four]
assert len(hits) == 1, (all_four, hits)
print('min like-all-four =', all_four)
print(hits[0])
