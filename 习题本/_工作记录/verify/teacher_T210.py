# T210 路灯1~100（右侧51~100），开关A、B、C分别控制2、3、5的倍数；全灭状态下依次按A、B、C，右侧亮几盏。
RIGHT, SWITCHES = range(51, 101), [2, 3, 5]
OPTS = {'A': 22, 'B': 23, 'C': 26, 'D': 28}
state = {i: False for i in range(1, 101)}
for m in SWITCHES:
    for i in state:
        if i % m == 0:
            state[i] = not state[i]
ans = sum(state[i] for i in RIGHT)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('lights on (right side) =', ans)
print(hits[0])
