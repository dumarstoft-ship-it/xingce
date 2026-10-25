# D01-math-2-v06 三次各发出"剩余的一半多10箱"，最后剩15箱，求原有
opts = {'A': 120, 'B': 190, 'C': 240, 'D': 260}
times, extra, final = 3, 10, 15

def forward(x):
    for _ in range(times):
        if x % 2:
            return None
        give = x // 2 + extra
        if give > x:
            return None
        x -= give
    return x

sols = [x for x in range(1, 100001) if forward(x) == final]
assert len(sols) == 1, sols
ans = sols[0]

# 干扰项的错误路径
y = final
for _ in range(times):
    y = y * 2 + extra                 # 倒推顺序弄反：先乘2再加10
assert y == opts['B']
y = final
for _ in range(times - 1):
    y = (y + extra) * 2               # 只倒推了两次
assert y == opts['A']
assert y * 2 == opts['C']             # 最后一步漏加10

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('original =', ans)
print(hits[0])
