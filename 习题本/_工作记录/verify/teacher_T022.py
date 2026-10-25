# teacher_T022  2020深圳-20：93件不是甲送的，92件不是乙送的，91件不是丙送的，甲送了几件
OPTS = {'A': 44, 'B': 45, 'C': 46, 'D': 47}
NOT_J, NOT_Y, NOT_B = 93, 92, 91
sols = [(j, y, b) for j in range(0, 200) for y in range(0, 200) for b in range(0, 200)
        if y + b == NOT_J and j + b == NOT_Y and j + y == NOT_B]
assert len(sols) == 1, sols
ans = sols[0][0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('甲乙丙 =', sols[0])
print(hits[0])
