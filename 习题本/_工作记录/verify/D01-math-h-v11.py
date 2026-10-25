# D01-math-h-v11  国防教育营宿舍：
# 每间住4人，有18人没有宿舍可住；每间住6人，有一间住了人但没住满，其余都正好住满。
# 求学生最多有多少人。
OPTS = {'A': 54, 'B': 58, 'C': 62, 'D': 66}

feasible = []
for rooms in range(1, 1001):
    people = 4 * rooms + 18                  # 每间4人，18人无房
    full, rest = divmod(people, 6)
    # 每间6人：恰好一间有人但未住满（1~5人），其余 rooms-1 间全部住满
    if full == rooms - 1 and 1 <= rest <= 5:
        feasible.append((rooms, people))
assert feasible, 'no solution'
best = max(p for _, p in feasible)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, hits

# 干扰项来源核对
assert [r for r in range(1, 100) if 6 * (r - 1) == 4 * r + 18] == [12]     # 当成“空出一间”
assert 4 * 12 + 18 == OPTS['D']
assert [r for r in range(1, 100) if 6 * r == 4 * r + 18] == [9]            # 当成全部住满
assert 4 * 9 + 18 == OPTS['A']
assert min(p for _, p in feasible) == OPTS['B']                            # 取了最少
print('feasible (rooms, people):', feasible)
print(hits[0])
