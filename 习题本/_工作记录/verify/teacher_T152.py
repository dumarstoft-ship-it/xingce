# teacher T152（2017河南选调）空心圆树形图，第10行空心圆个数
OPTS = {'A': 34, 'B': 21, 'C': 13, 'D': 8}
# 图中第1~6行的（空心, 实心）个数，用来确认生成规则
FIG = {1: (1, 0), 2: (0, 1), 3: (1, 1), 4: (1, 2), 5: (2, 3), 6: (3, 5)}

def nxt(white, black):
    # 规则（由图读出）：空心→下一行1个实心；实心→下一行1实心+1空心
    return black, black + white

rows = {1: FIG[1]}
for r in range(2, 11):
    rows[r] = nxt(*rows[r - 1])
assert all(rows[r] == FIG[r] for r in FIG), rows
print('第10行 (空心, 实心) =', rows[10])
hits = [k for k, v in OPTS.items() if v == rows[10][0]]
assert len(hits) == 1, hits
print(hits[0])
