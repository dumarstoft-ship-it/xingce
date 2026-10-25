# teacher_T037  2021河北-62：180只鸟分A、B、C三区；第1日A区飞出使B、C翻倍；第2日B区飞出使A、C翻倍；
#               第3日C区飞出使A、B翻倍，此时C=7/26·A。最初A区有多少只
OPTS = {'A': 103, 'B': 104, 'C': 105, 'D': 106}
TOTAL = 180

def simulate(a, b, c):
    a, b, c = a - b - c, 2 * b, 2 * c          # 第1日：A 分给 B、C 各自原有数量
    if a <= 0: return None
    b, a, c = b - a - c, 2 * a, 2 * c          # 第2日：B 分给 A、C
    if b <= 0: return None
    c, a, b = c - a - b, 2 * a, 2 * b          # 第3日：C 分给 A、B
    if c <= 0: return None
    return a, b, c

sols = []
for a0 in range(1, TOTAL + 1):
    for b0 in range(1, TOTAL - a0):
        c0 = TOTAL - a0 - b0
        if c0 < 1:
            continue
        end = simulate(a0, b0, c0)
        if end and 26 * end[2] == 7 * end[0]:
            sols.append((a0, b0, c0, end))
assert sols, sols
starts = {s[0] for s in sols}
assert len(starts) == 1, sols
ans = starts.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
# 解析里的捷径：只跟踪A区，三日后A=4(2A0-180)，须为26的倍数（C=7/26·A为整数）
assert [k for k, v in OPTS.items() if 4 * (2 * v - TOTAL) % 26 == 0] == hits
print('最初(A,B,C), 三日后 =', sols)
print(hits[0])
